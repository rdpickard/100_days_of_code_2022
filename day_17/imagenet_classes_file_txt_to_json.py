import re
import json
import os
import sys

# Small utility to convert imagenet label index file marked up as text into json. Base txt file of labels is here
# https://gist.github.com/yrevar/942d3a0ac09ec9e5eb3a

imagenet_classes_file_name = "imagenet_classes.txt"

if not os.path.exists(imagenet_classes_file_name):
    print(f"Can't find imagesnet class txt file at expected name '{imagenet_classes_file_name}'")
    sys.exit(-1)

with open(imagenet_classes_file_name) as imagenet_file:
    imagenet_file_lines = imagenet_file.readlines()

imagenet_json = {}
for imagenet_file_line in imagenet_file_lines:

    if re.match(r"\s\d+:\s'.*'", imagenet_file_line) is None:
        continue

    index, tags_string = imagenet_file_line.split(":", 2)

    if "," in tags_string:
        tags = [tag.strip() for tag in re.match(r"\s'(.*)'", tags_string).groups()[0].split(",")]
    else:
        tags = [f"{tags_string}"]
    imagenet_json[f"{index.strip()}"] = tags

print(json.dumps(imagenet_json, indent=4, sort_keys=True))