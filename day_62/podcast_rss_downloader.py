import os.path
import logging
import sys
import posixpath
import urllib.parse

import feedparser
import requests
from google.cloud import storage as google_cloud_storage
from google.cloud import speech_v1p1beta1 as google_cloud_speech
import filetype
import pydub

audio_files_dir = "../local/day_62/audio_files/"
podcast_rss_url = "http://feeds.libsyn.com/124693/rss"
google_cloud_storage_bucket_name = "day_62"

logging.basicConfig(level=logging.INFO)

# Instantiates a client
storage_client = google_cloud_storage.Client()

# Creates the new bucket
google_cloud_storage_bucket = storage_client.bucket(google_cloud_storage_bucket_name)
google_cloud_storage_bucket_exists = False

try:
    google_cloud_storage_bucket_exists = google_cloud_storage_bucket.exists()
except Exception as e:
    logging.exception(f"Checking existence of google cloud bucket '{google_cloud_storage_bucket_name}' raised exception '{e}'")

if not google_cloud_storage_bucket_exists:
    logging.error(f"Google cloud bucket for audio uploads '{google_cloud_storage_bucket_name}' does not exist or can't be accessed. Exiting")
    sys.exit(-1)


def filename_from_string(original_filename_string, logger=logging.getLogger()):

    filename = '%s' % original_filename_string
    filename = filename.replace(" ", "_")

    if "." in filename:
        filename, filename_suffix = os.path.splitext(filename)
        filename_suffix = "."+filename_suffix
    else:
        filename_suffix = ""

    keep_characters = [":"]
    "".join(c for c in filename if c.isalnum() or c in keep_characters).rstrip()

    filename = filename+filename_suffix

    logger.debug(f"String '{original_filename_string}' reformatted to '{filename}' to be used as filename")

    return filename


def download_from_url_as_stream_to_file(url, local_filename, logger=logging.getLogger()):

    # NOTE the stream=True parameter below

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def convert_file_to_flac(input_file_path, logger=logging.getLogger()):

    file_type_guess = filetype.guess(input_file_path)

    if file_type_guess.extension == 'flac':
        return True, input_file_path

    successfully_converted = False
    flac_file_name = None

    if file_type_guess.extension == 'mp3':
        flac_file_name = os.path.splitext(input_file_path)[0] + ".flac"
        flac_audio = pydub.AudioSegment.from_mp3(input_file_path)
        flac_audio.export(flac_file_name, "flac")
        successfully_converted = True

    if successfully_converted:
        logger.info(f"Converted '{input_file_path}' to FLAC file '{flac_file_name}'")
        return True, flac_file_name

    return False, input_file_path


if not os.path.exists(audio_files_dir):
    logging.info(f"Creating audio files dir '{audio_files_dir}'")
    os.makedirs(audio_files_dir)


podcast_feed_data = feedparser.parse(podcast_rss_url)

logging.info(f"Feed title: {podcast_feed_data['feed']['title']}")

downloaded = 0
downloaded_limit = 1

download_errors = 0
download_errors_limit = 2

skip_existing_local_audio_files = True
audio_file_paths_to_upload_to_google_cloud_bucket = []

for entry in podcast_feed_data.entries:
    if downloaded >= downloaded_limit:
        break
    if download_errors >= download_errors_limit:
        logging.warning(f"Download loop exceeded number of processing errors of '{download_errors_limit}'. Exiting download loop")
        break

    logging.info(f"\tfeed entry title: {entry['title']}")

    for link in filter(lambda link_dict: link_dict.get("type", "").startswith("audio"), entry.get("links", [])):

        filename_from_title = filename_from_string(entry['title'])

        already_downloaded = False
        for existing_audio_file_name in os.listdir(audio_files_dir):
            if filename_from_title == existing_audio_file_name or filename_from_title == os.path.splitext(existing_audio_file_name)[0]:
                logging.info(f"\t\tSkipping download or entry '{filename_from_title}', already downloaded entry audio at file '{existing_audio_file_name}'.")
                already_downloaded = True

        if already_downloaded:
            continue

        audio_file_full_path = os.path.join(audio_files_dir, filename_from_title)

        try:
            download_from_url_as_stream_to_file(link['href'], audio_file_full_path)

            # Files downloaded don't always have an extension but Google speech-to-text requires them. Use
            # filetype module to guess the extension and then rename the file as appropriate

            _, file_extension = os.path.splitext(audio_file_full_path)

            if file_extension is None or file_extension == '':
                filetype_guess = filetype.guess(audio_file_full_path)
                file_extension = filetype_guess.extension
                os.rename(audio_file_full_path, audio_file_full_path + "." + file_extension)
                audio_file_full_path = audio_file_full_path + "." + file_extension

            """
            is_flac, audio_file_full_path = convert_file_to_flac(audio_file_full_path)

            if not is_flac:
                logging.info(f"Cloud not convert file '{audio_file_full_path} to FLAC. Skipping")
                continue
            """

            audio_file_paths_to_upload_to_google_cloud_bucket.append(audio_file_full_path)
            downloaded += 1
            logging.info(f"\t\tDownloaded '{link['href']}' to '{audio_file_full_path}'")

        except Exception as e:
            logging.warning(f"Downloading '{link['href']}' to '{audio_file_full_path}' raised exception '{e}'")
            download_errors += 1
            continue


audio_google_storage_blob_uris = []

for audio_file_path in audio_file_paths_to_upload_to_google_cloud_bucket:

    try:
        blob_name = os.path.basename(audio_file_path)
        audio_file_goolge_cloud_storage_blob = google_cloud_storage_bucket.blob(blob_name)
        audio_file_goolge_cloud_storage_blob.upload_from_filename(audio_file_path)
        logging.info(f"Uploaded '{audio_file_path}' as google cloud storage blob '{blob_name}' to bucket '{google_cloud_storage_bucket_name}'")
        gs_uri = "gs://"+google_cloud_storage_bucket_name+"/"+blob_name
        audio_google_storage_blob_uris.append(gs_uri)
    except Exception as e:
        logging.exception(f"Exception uploading '{audio_file_path}' as google cloud storage blob '{blob_name}' to bucket '{google_cloud_storage_bucket_name}'. Exception is '{e}'")
        continue


google_speech_client = google_cloud_speech.SpeechClient()

for audio_blob_uri in audio_google_storage_blob_uris:

    audio = google_cloud_speech.RecognitionAudio(uri=audio_blob_uri)

    speaker_diarization_config = {
        "enableSpeakerDiarization": True,
        "minSpeakerCount": 2,
        "maxSpeakerCount": 2,
        "speakerTag": 1
    }

    config = google_cloud_speech.RecognitionConfig(
        encoding=google_cloud_speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )

    transcript_google_storage_blob_name = os.path.splitext(posixpath.basename(urllib.parse.urlparse(audio_blob_uri).path))[0] + ".TRANSCRIPT.json"
    transcript_google_storage_blob_uri = f"gs://day_62/{transcript_google_storage_blob_name}"

    output_audio_config = google_cloud_speech.TranscriptOutputConfig(gcs_uri=transcript_google_storage_blob_uri)

    request = google_cloud_speech.LongRunningRecognizeRequest(config=config,
                                                              audio=audio,
                                                              output_config=output_audio_config)

    operation = google_speech_client.long_running_recognize(request=request)

    logging.info(f"Speech-to-text operation requested. Transcription will be in Google Storage Blob '{transcript_google_storage_blob_uri}'")

    """
    # get content as string
    results_string = blob.download_as_string()

    # get transcript exported in storage bucket
    storage_transcript = types.LongRunningRecognizeResponse.from_json(
        results_string, ignore_unknown_fields=True
    )

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in storage_transcript.results:
        # The first alternative is the most likely one for this portion.
        print(f"Transcript: {result.alternatives[0].transcript}")
        print(f"Confidence: {result.alternatives[0].confidence}")
"""



