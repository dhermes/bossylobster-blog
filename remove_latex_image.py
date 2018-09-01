# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import subprocess
import sys


LATEX_IMG_NAMES_FILE = "latex_img_names.json"
with open(LATEX_IMG_NAMES_FILE, "r") as fh:
    IMAGE_NAMES = json.load(fh)


def remove_key_from_cache(image_id):
    matches = [
        key for key, value in IMAGE_NAMES.iteritems() if value == image_id
    ]
    if len(matches) != 1:
        raise ValueError((image_id, "Not found exactly once."))
    matching_key = matches[0]
    IMAGE_NAMES.pop(matching_key)
    with open(LATEX_IMG_NAMES_FILE, "w") as fh:
        json.dump(
            IMAGE_NAMES, fh, indent=2, sort_keys=True, separators=(",", ": ")
        )
        fh.write("\n")


def remove_image_file(image_id):
    filename = "content/latex_images/%d.png" % (image_id,)
    subprocess.call(["git", "rm", filename])


def remove_image(image_id):
    remove_key_from_cache(image_id)
    remove_image_file(image_id)


def main(argv):
    image_id = None
    if len(argv) == 2:
        try:
            image_id = int(argv[1])
        except (TypeError, ValueError):
            pass

    if image_id is None:
        print >>sys.stderr, "Usage:"
        print >>sys.stderr, "    remove_latex_image.py IMAGE_ID"
        sys.exit(1)

    remove_image(image_id)


if __name__ == "__main__":
    main(sys.argv)
