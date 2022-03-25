import json
import hashlib
import base64

from sqlalchemy_json_type import json_type

import flask
import flask_restful
import flask_sqlalchemy
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types
import sqlalchemy.ext.mutable
import jsonschema
import arrow
import PIL.Image

app = flask.Flask(__name__)
api = flask_restful.Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = flask_sqlalchemy.SQLAlchemy(app)


class LabeledImageModel(db.Model):
    __tablename__ = "labeled_image"

    id = db.Column(db.Integer, primary_key=True)

    image_data = db.Column(db.LargeBinary)
    image_data_md5_hex_digest = db.Column(db.String(32))

    image_data_format = db.Column(db.String(32))

    readable_name = db.Column(db.String(1024))
    readable_description = db.Column(db.String(1024))

    details_document = sqlalchemy.Column(json_type)

    @property
    def serialized_json(self):
        return {
            'id': self.id,
            'readable_name': self.readable_name,
            'readable_description': self.readable_description,
            'image_data_md5_hex_digest': self.image_data_md5_hex_digest,
            'image_data_format': self.image_data_format,
            'details_document': self.details_document
        }


class IndexedLabelSetModel(db.Model):
    __tablename__ = "indexed_label_set"

    id = db.Column(db.Integer, primary_key=True)

    readable_name = db.Column(db.String(1024))
    readable_description = db.Column(db.String(1024))
    readable_source = db.Column(db.String(2048))

    data = sqlalchemy.Column(json_type)
    data_version = db.Column(db.String(1024))

    details_document = sqlalchemy.Column(json_type)

    @property
    def serialized_json(self):
        return {
            'name': self.readable_name,
            'source': self.readable_source,
            'version': self.data_version,
            'description': self.readable_description,
            'data': self.data,
        }


class LabeledImageLabelModel(db.Model):
    __tablename__ = "labeled_image_label"

    id = db.Column(db.Integer, primary_key=True)

    labeled_image_id = db.Column(db.Integer, db.ForeignKey('labeled_image.id'), nullable=False)
    indexed_label_set_id = db.Column(db.Integer, db.ForeignKey('indexed_label_set.id'), nullable=False)

    indexed_label_set_label_id = db.Column(db.String(80))


class LabeledImagesListAPIResource(flask_restful.Resource):

    def get(self):
        all_images = LabeledImageModel.query.all()
        return flask.jsonify([i.serialized_json for i in all_images])


class LabeledImageAPIResource(flask_restful.Resource):

    def get(self, image_id):
        img = LabeledImageModel.query.filter(LabeledImageModel.id == image_id).one_or_none()
        if img is None:
            response = flask.jsonify()
            response.status_code = 404
            return response

        return flask.jsonify(img.serialized_json)

    def post(self):
        up_loaded_file = flask.request.files['file']

        img = LabeledImageModel(image_data=base64.b64encode(up_loaded_file.read()),
                                image_data_md5_hex_digest=hashlib.md5(up_loaded_file.read()).hexdigest(),
                                image_data_format=PIL.Image.open(up_loaded_file).format,
                                readable_name=up_loaded_file.filename,
                                details_document={"source": "uploaded from webapp"})

        db.session.add(img)
        db.session.commit()

        response = flask.jsonify()
        response.status_code = 201
        response.headers['location'] = f'/api/labeled_image/{img.id}'
        response.autocorrect_location_header = False

        return response

    def put(self, image_id):
        pass


class LabeledImageLabelAPIResource(flask_restful.Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class LabeledImageImageAPIResource(flask_restful.Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class IndexedLabelSetAPIResource(flask_restful.Resource):

    def get(self, set_name, version=None):
        pass

    def post(self):
        print(len(flask.request.files))
        print(flask.request.files.keys())
        print('file' in flask.request.files.keys())

        if len(flask.request.files) >= 1 and 'file' in flask.request.files.keys():
            # JSON was uploaded as a file
            up_loaded_file = flask.request.files['file']

            label_set_json = json.loads(up_loaded_file.read())
        elif flask.request.is_json:
            label_set_json = flask.request.get_json()
        else:
            response = flask.jsonify({"message": "no data provided"})
            response.status_code = 406
            return response

        label_set_schema_file_path = "schemas/indexed_label_set_schema.json"
        with open("schemas/indexed_label_set_schema.json") as label_set_schema_file:
            label_set_schema = json.loads(label_set_schema_file.read())

        try:
            jsonschema.validate(label_set_json, label_set_schema)
        except Exception as e:
            response = flask.jsonify(
                {"message": f"JSON data failed to validate against schema {label_set_schema_file_path} with error {e}"})
            response.status_code = 406
            return response

        label_set = IndexedLabelSetModel(readable_name=label_set_json["indexed label set"]["name"],
                                         readable_description=label_set_json["indexed label set"]["description"],
                                         readable_source=label_set_json["indexed label set"]["source"],
                                         data_version=label_set_json["indexed label set"]["version"],
                                         data=label_set_json["indexed label set"]["data"])

        db.session.add(label_set)
        db.session.commit()

        response = flask.jsonify()
        response.status_code = 201
        response.headers['location'] = f'/api/indexed_label_sets/{label_set.readable_name}'
        response.autocorrect_location_header = False

        return response

    def put(self):
        pass


class IndexedLabelSetListAPIResource(flask_restful.Resource):

    def get(self):
        all_sets = IndexedLabelSetModel.query.all()
        return flask.jsonify([i.serialized_json for i in all_sets])


@app.route("/", methods=["GET"])
def app_index():
    return flask.render_template('index.jinja2')


@app.before_first_request
def setup():
    db.create_all()


api.add_resource(LabeledImagesListAPIResource, "/api/labeled_images/")
api.add_resource(LabeledImageAPIResource, "/api/labeled_image/<string:image_id>",
                                          "/api/labeled_image/")

api.add_resource(LabeledImageImageAPIResource, "/api/labeled_image/<string:image_id>/image")
api.add_resource(LabeledImageLabelAPIResource, "/api/labeled_image/<string:image_id>/labels",
                                               "/api/labeled_image/<string:image_id>/labels/<string:set_name>")

api.add_resource(IndexedLabelSetListAPIResource, "/api/indexed_label_sets/")
api.add_resource(IndexedLabelSetAPIResource, "/api/indexed_label_set/<string:set_name>/<string:data_version>",
                                             "/api/indexed_label_set/<string:set_name>",
                                             "/api/indexed_label_set/")

if __name__ == "__main__":
    app.run(debug=True)
