import uuid
import json
import logging
import base64
import sys
import urllib

import requests
import arrow
import jsonschema
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types
import sqlalchemy.ext.mutable
import bs4

itunes_search_url = "https://itunes.apple.com/search"

apple_podcast_corpus = {}

search_results = []

recommendation_results = []

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

Base = sqlalchemy.orm.declarative_base()


class MutableDict(sqlalchemy.ext.mutable.Mutable, dict):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/mutable.html

    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return sqlalchemy.ext.mutable.Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


class JSONEncodedDict(sqlalchemy.types.TypeDecorator):
    # https://docs.sqlalchemy.org/en/14/core/custom_types.html#marshal-json-strings

    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict(255)

    """

    impl = sqlalchemy.types.VARCHAR

    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


json_type = MutableDict.as_mutable(JSONEncodedDict)


class PersonNode(Base):
    __tablename__ = "person_node"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)


class GroupNode(Base):
    __tablename__ = "group_node"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    apple_artist_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    apple_artist_name = sqlalchemy.Column(sqlalchemy.String)


class PodcastNode(Base):
    __tablename__ = "podcast_node"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    apple_podcast_name = sqlalchemy.Column(sqlalchemy.String)
    apple_podcast_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    apple_podcast_md5_derived_id = sqlalchemy.Column(sqlalchemy.String, unique=True)


class PodcastArtistEdge(Base):
    __tablename__ = "artist_to_podcast_edge"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    podcast_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('podcast_node.id'))
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('podcast_node.id'))

    first_seen_utc_timestamp = sqlalchemy.Column(sqlalchemy.DATETIME)
    last_seen_utc_timestamp = sqlalchemy.Column(sqlalchemy.DATETIME)


class RecommendationStackDocument(Base):
    __tablename__ = "recommendation_stack_document"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    recommendation_seen_time = sqlalchemy.Column(sqlalchemy.DATETIME)
    base_podcast_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('podcast_node.id'))
    recommendation_chosen_characteristic = sqlalchemy.Column(sqlalchemy.String)

    portal_to_recommendation = sqlalchemy.Column(sqlalchemy.String)

    parent_recommendation_stack = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('recommendation_stack_document.id'))


class SearchToPodcastRecommendationEdge(Base):
    __tablename__ = "search_to_podcast_recommendation_edge"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    from_recommendation_stack = sqlalchemy.Column(sqlalchemy.Integer,
                                                  sqlalchemy.ForeignKey('recommendation_stack_document.id'))
    to_podcast_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('podcast_node.id'))

    recommendation_order_position = sqlalchemy.Column(sqlalchemy.Integer)


class PodcastToPodcastRecommendationEdge(Base):
    __tablename__ = "podcast_to_podcast_recommendation_edge"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    from_podcast_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('podcast_node.id'))
    to_podcast_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('podcast_node.id'))
    recommendation_stack = sqlalchemy.Column(sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey('recommendation_stack_document.id'))
    stack_order_position = sqlalchemy.Column(sqlalchemy.Integer)


class PodcastiTunesTrackDocument(Base):
    __tablename__ = "podcast_track_document"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    podcast_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('podcast_node.id'))
    document_utc_timestamp = sqlalchemy.Column(sqlalchemy.DATETIME)
    document_json = sqlalchemy.Column(json_type)


def search_itunes_podcasts(search_term):

    # TODO fix search terms that include spaces. Currently returns no results

    itunes_search_parameters = {"entity": "podcast", "term": search_term}

    search_response = requests.get(itunes_search_url, params=itunes_search_parameters)

    if search_response.status_code == 200:
        # Validate response
        # TODO Fix inefficient loading of schema from file each time
        with open("schemas/itunes_search_podcast_results_schema.json") as result_schema_file:
            result_schema = json.load(result_schema_file)

        jsonschema.validate(search_response.json(), result_schema)

    return search_response


def _unfuq_itunes_web_embedded_dict_string(fuqd_string):
    """

    :param fuqd_string:
    :return:
    """
    unfuqd_json = {}
    unescaped_fuqd_string_json = json.loads(fuqd_string)

    for key in unescaped_fuqd_string_json.keys():
        dict_blob = unescaped_fuqd_string_json[key]
        unescaped_dict_blob = dict_blob.replace('\"', '"')
        unfuqd_json[key] = json.loads(unescaped_dict_blob)

    return unfuqd_json


def get_itunes_recommendations_for_podcast(itunes_trackview_url):

    # The following prefixes can be added to the end of the trackview url as a prefix to get
    # recommendations for the podcast
    recommendation_section_url_postfixes = [
        "#see-all/top-podcasts",
        "#see-all/more-by-artist",
        "#see-all/listeners-also-subscribed"
    ]

    apple_key_regex_to_corpus_category = {
        r'v1.catalog.us.artists': {
            "corpus_key": "podcasts_by_artist",
            "podcast_extractor": lambda d: d["d"][0]['relationships']['podcasts']['data']
        },
        r'v1.catalog.us.charts': {
            "corpus_key": "podcasts_by_genera",
            "podcast_extractor": lambda d: d["d"]['podcasts'][0]['data']
        },
        r'v1.catalog.us.podcasts': {
            "corpus_key": "podcast_by_subscriber",
            "podcast_extractor": lambda d: d["d"][0]['relationships']['listeners-also-subscribed']['data']
        }
    }

    trackview_response = requests.get(itunes_trackview_url)

    if trackview_response.status_code != 200:
        logging.warning("Response status code '{}' to GET of url '{}'. "
                        "Expected 200".format(trackview_response.status_code, itunes_trackview_url))
        return None, None

    trackview_soup_page = bs4.BeautifulSoup(trackview_response.text, "html.parser")

    embedded_podcast_media_elements = trackview_soup_page.select("script[id=shoebox-media-api-cache-amp-podcasts]")

    embedded_podcast_data = {}

    if len(embedded_podcast_media_elements) > 0:
        embedded_podcast_data = _unfuq_itunes_web_embedded_dict_string(embedded_podcast_media_elements[0].text)

    with open("../local/recdump.json", "w") as twitter_data_file:
        json.dump(embedded_podcast_data, twitter_data_file, indent=4, sort_keys=True)

    podcast_recommendations = {}

    for key in embedded_podcast_data.keys():

        mapped_category_name = None
        extractor_lambda = None
        for apple_key_name_regex, corpus_key in apple_key_regex_to_corpus_category.items():
            if key.find(apple_key_name_regex) > 0:
                mapped_category_name = corpus_key["corpus_key"]
                extractor_lambda = corpus_key["podcast_extractor"]

        if mapped_category_name is None:
            logging.warning("Could not match apple embedded string key '{}' to a corpus key regex".format(key))
            continue
        if mapped_category_name in podcast_recommendations.keys():
            logging.warning("corpus key '{}' already in recommendation list. This is unexpected. apple embedded string key '{}'. Skipping".format(mapped_category_name, key))
            continue

        podcast_recommendations[mapped_category_name] = []

        for recommended_podcast in extractor_lambda(embedded_podcast_data[key]):
            podcast_recommendations[mapped_category_name].append({
                "podcast_name": recommended_podcast["attributes"]["name"],
                "apple_podcast_id": recommended_podcast["id"],
                "genreNames": recommended_podcast["attributes"]["genreNames"],
                "apple_podcast_url": recommended_podcast["attributes"]["url"],
                "artist_name": recommended_podcast["attributes"]["artistName"]
            })

    return podcast_recommendations


def json_to_b64_str(dict_to_encode):
    return base64.b64encode(json.dumps(dict_to_encode).encode('ascii')).decode("ascii")


def update_podcasts_corpus_from_itunes_recommendation(recommendation_json):

    """
    Create an instances of a PodcastNode and a GroupNode database objects if they don't exist. The input JSON is
    formatted from the get_itunes_recommendations_for_podcast function.

    Basically a convenience method to wrap up all of the sql logic.

    example json:

    {
            "apple_podcast_id": "1222114325",
            "apple_podcast_url": "https://podcasts.apple.com/us/podcast/up-first/id1222114325",
            "artist_name": "NPR",
            "genreNames": [
                "Daily News",
                "Podcasts",
                "News"
            ],
            "podcast_name": "Up First"
        },

    :param recommendation_json:
    :return: the SQL databast ID of the podcast
    """

    session = Session()

    try:
        podcast = session.query(PodcastNode).filter(PodcastNode.apple_podcast_id == recommendation_json["apple_podcast_id"]).one()
    except sqlalchemy.orm.exc.NoResultFound:
        podcast = PodcastNode(apple_podcast_id=recommendation_json["apple_podcast_id"],
                              apple_podcast_name=recommendation_json["podcast_name"])
        session.add(podcast)
        session.commit()

    try:
        group = session.query(GroupNode).filter(GroupNode.apple_artist_name == recommendation_json["artist_name"]).one()
    except sqlalchemy.orm.exc.NoResultFound:
        group = GroupNode(apple_artist_name = recommendation_json["artist_name"])
        session.add(group)
        session.commit()

    try:
        podcast_artist_edge = session.query(PodcastArtistEdge).filter(PodcastArtistEdge.podcast_id == podcast.id).filter(PodcastArtistEdge.group_id == group.id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        podcast_artist_edge = PodcastArtistEdge(podcast_id=podcast.id, group_id=group.id,
                                                first_seen_utc_timestamp=arrow.now("UTC").datetime)
        session.add(podcast_artist_edge)
        session.commit()

    print("PodcastArtistEdge {} {}".format(podcast_artist_edge.podcast_id, podcast_artist_edge.group_id))

    return podcast.id

def update_podcasts_corpus_from_itunes_search(podcast_json):
    """
    Create an instance of a Podcast database object from the JSON returned by iTunes search query. Expected JSON
    format is described in schemas/itunes_search_podcast_results_schema/$defs/podcast-track

    :param podcast_json: podcast description in JSON formatting
    :return: Corpus ID of Podcast object. Not the same as the itunes ID for the podcast
    """

    session = Session()
    new_podcast_in_corpus = False

    try:
        if "artistId" in podcast_json.keys():
            artist_group = session.query(GroupNode).filter(GroupNode.apple_artist_id == podcast_json["artistId"]).one()
        else:
            logging.info("Podcast track '{}' does not have an artistID".format(podcast_json["trackId"]))
            artist_group = session.query(GroupNode).filter(
                GroupNode.apple_artist_name == podcast_json["artistName"]).one()
    except sqlalchemy.orm.exc.MultipleResultsFound:
        logging.error(
            "Multiple GroupNode objects found in database with apple_artist_id of {} or name {}. "
            "Expected one or none. Bailing".format(
                podcast_json.get("artistId", None), podcast_json.get("artistName", None)))
        return None
    except sqlalchemy.orm.exc.NoResultFound:
        # No such group in the db, create it
        artist_group = GroupNode(apple_artist_id=podcast_json.get("artistId", None),
                                 apple_artist_name=podcast_json["artistName"])
        session.add(artist_group)
        new_podcast_in_corpus = True
        session.commit()

    try:
        podcast = session.query(PodcastNode).filter(PodcastNode.apple_podcast_id == podcast_json["trackId"]).one()

    except sqlalchemy.orm.exc.MultipleResultsFound:
        logging.error(
            "Multiple Podcast objects found in database with apple_podcast_id of {}. "
            "Expected one or none. Bailing".format(
                podcast_json["trackId"]))
        return None, None
    except sqlalchemy.orm.exc.NoResultFound:
        # No such podcast in the db, create it
        podcast = PodcastNode(apple_podcast_name=podcast_json["trackName"], apple_podcast_id=podcast_json["trackId"])
        session.add(podcast)
        session.commit()

    # noinspection PyBroadException
    try:
        podcast_artist_edge = session.query(PodcastArtistEdge).filter(PodcastArtistEdge.podcast_id == podcast.id). \
            filter(PodcastArtistEdge.group_id == artist_group.id). \
            order_by(sqlalchemy.desc(PodcastArtistEdge.last_seen_utc_timestamp)).first()
        if podcast_artist_edge is None:
            podcast_artist_edge = PodcastArtistEdge(podcast_id=podcast.id, group_id=artist_group.id,
                                                    first_seen_utc_timestamp=arrow.now("UTC").datetime)
            session.add(podcast_artist_edge)
            session.commit()
    except Exception as e:
        logging.error("Exception trying to get PodcastArtistEdge "
                      "for podcast_id {} and group_id {} Exception is '{}'".format(podcast.id, artist_group.id, e))
        return None, None

    podcast_artist_edge.last_seen_utc_timestamp = arrow.now("UTC").datetime

    session.commit()

    # Put the track JSON document into the DB as a blob. For later reference
    track_document = PodcastiTunesTrackDocument(podcast_id=podcast.id,
                                                document_utc_timestamp=arrow.now("UTC").datetime,
                                                document_json=podcast_json)
    session.add(track_document)
    session.commit()

    return new_podcast_in_corpus, podcast.id


engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.ERROR)
my_session = Session()

Base.metadata.create_all(engine)

term = " ".join(sys.argv[1:])

# create a new recommendation stack for the search term
search_term_recommendation_stack = RecommendationStackDocument(recommendation_chosen_characteristic="Search term '{}'".format(term))
my_session.add(search_term_recommendation_stack)
my_session.commit()

run_id = uuid.uuid4()
run_time = arrow.now("UTC").datetime

# Get initial set of podcasts from a search term
itunes_search_response = search_itunes_podcasts(term)

podcast_ids = []

result_count = 1

for result in itunes_search_response.json()["results"]:
    # Add the podcasts to the corpus of podcasts
    podcast_is_new, podcast_corpus_id = update_podcasts_corpus_from_itunes_search(result)

    # create an edge from the initial search by term to the podcast
    # It's assumed the itunes_search_response returns results in oder of most-to-least recommended
    recommendation_edge = SearchToPodcastRecommendationEdge(from_recommendation_stack=search_term_recommendation_stack.id,
                                                            to_podcast_id=podcast_corpus_id,
                                                            recommendation_order_position=result_count)
    my_session.add(recommendation_edge)
    my_session.commit()

    if podcast_is_new:
        logging.info("ADDED '{}' as id {}".format(result["trackName"], podcast_corpus_id))
        podcast_ids.append(podcast_corpus_id)
    else:
        logging.info("UPDATED '{}' as id {}".format(result["trackName"], podcast_corpus_id))
    result_count += 1

# podcast_ids are the local database IDs not the apple IDs

limit = 5
count = 0

for podcast_id in podcast_ids:

    if count > limit:
        break
    count += 1

    podcast_track_document = my_session.query(PodcastiTunesTrackDocument). \
        filter(PodcastiTunesTrackDocument.podcast_id == podcast_id). \
        order_by(sqlalchemy.desc(PodcastiTunesTrackDocument.document_utc_timestamp)). \
        first()

    recommendations = {}
    if podcast_track_document is not None:
        recommendations = get_itunes_recommendations_for_podcast(podcast_track_document.document_json['trackViewUrl'])
    else:
        print("DOCUMENT IS NONE FOR {}".format(podcast_id))

    #print("RECOMMENDATIONS FOR {} ({})".format(podcast_track_document.document_json['collectionName'], podcast_track_document.document_json['artistName']))

    for recommendation_category in recommendations.keys():
        # The keys of the recommendations JSON are the category of recommendation. like 'by genera' or 'by subscriber'.
        # want to keep the category of recommendation as part of the data set

        category_recommendation_stack = RecommendationStackDocument(
            recommendation_chosen_characteristic="Apple itunes algorithm category '{}'".format(recommendation_category),
            parent_recommendation_stack=search_term_recommendation_stack.id,
            base_podcast_id=podcast_id
            )
        my_session.add(category_recommendation_stack)
        my_session.commit()

        for podcast_recommendation in recommendations[recommendation_category]:

            recommended_podcast_db_id = update_podcasts_corpus_from_itunes_recommendation(podcast_recommendation)

            p2p_recommendation_edge = PodcastToPodcastRecommendationEdge(from_podcast_id=podcast_id,
                                                                         to_podcast_id=recommended_podcast_db_id,
                                                                         recommendation_stack=category_recommendation_stack.id,
                                                                         stack_order_position=count)
            my_session.add(p2p_recommendation_edge)
            my_session.commit()

    #print(json.dumps(recommendations, indent=4, sort_keys=True))

    # Create a recommended edge
    #break

#sys.exit()

search_recommendation_edges = my_session.query(SearchToPodcastRecommendationEdge).\
    filter(SearchToPodcastRecommendationEdge.from_recommendation_stack == search_term_recommendation_stack.id);

for edge in search_recommendation_edges:

    podcast = my_session.query(PodcastiTunesTrackDocument).filter(PodcastiTunesTrackDocument.podcast_id == edge.to_podcast_id).order_by(sqlalchemy.desc(PodcastiTunesTrackDocument.document_utc_timestamp)).first()
    print("The #{} recommended podcast for {} {} ({})".format(edge.recommendation_order_position,
                                                              search_term_recommendation_stack.recommendation_chosen_characteristic,
                                                              podcast.document_json['collectionName'],
                                                              podcast.document_json['artistName']))
    recommended_podcasts_edges = my_session.query(PodcastToPodcastRecommendationEdge).filter(PodcastToPodcastRecommendationEdge.from_podcast_id == podcast.id)
    for recommended_podcast_edge in recommended_podcasts_edges:
        podcast = my_session.query(PodcastNode).filter(PodcastNode.id == recommended_podcast_edge.to_podcast_id).one()
        group_edge = my_session.query(PodcastArtistEdge).filter(PodcastArtistEdge.podcast_id == podcast.id).one()

        group = my_session.query(GroupNode).filter(GroupNode.id == group_edge.group_id).one()

        recommendation_stack = my_session.query(RecommendationStackDocument).filter(RecommendationStackDocument.id == recommended_podcast_edge.recommendation_stack).one()
        print("\t{} ({}) [{}]".format(podcast.apple_podcast_name, group.apple_artist_name, recommendation_stack.recommendation_chosen_characteristic))


sys.exit()
