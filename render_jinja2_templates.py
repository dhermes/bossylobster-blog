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

import binascii
import glob
import hashlib
import json
import os
import re
import subprocess
import tempfile

import jinja2
import py.path


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FORCE_RENDER = "FORCE_RENDER" in os.environ
TEMPLATES_DIR = os.path.join(BASE_DIR, "templated_content")
ENV = jinja2.Environment(
    loader=jinja2.PackageLoader(__name__, "templated_content")
)
KATEX_PATH = os.path.join(BASE_DIR, "node_modules", "katex")
NODE_SCRIPT_TEMPLATE_INLINE = u"""\
katex = require(%(katex_path)s);
value = katex.renderToString("%%s");
console.log(value);
""" % {
    "katex_path": json.dumps(KATEX_PATH)
}
NODE_SCRIPT_TEMPLATE_MATH_MODE = u"""\
katex = require(%(katex_path)s);
value = katex.renderToString("%%s", {displayMode: true});
console.log(value);
""" % {
    "katex_path": json.dumps(KATEX_PATH)
}
KATEX_BLOCK_TEMPLATE = u"""\
<div class="katex-elt"><blockquote>
%s
</blockquote></div>"""
TEMPLATE_HASHES_FILENAME = os.path.join(TEMPLATES_DIR, "template_hashes.json")
with open(TEMPLATE_HASHES_FILENAME, "r") as fh:
    TEMPLATE_HASHES = json.load(fh)

RENDERED_DIR = os.path.join(BASE_DIR, "content")


def escape_string(latex_str):
    return latex_str.replace("\\", r"\\")


def utf8_to_html_entity(char_val):
    ordinal_val = ord(char_val)
    if ordinal_val < 127:
        return char_val
    return "&#%04d;" % (ordinal_val,)


def utf8_to_html_entities(str_val):
    chars = [utf8_to_html_entity(char_val) for char_val in str_val]
    return "".join(chars)


def get_katex(latex_str, blockquote=False):
    escaped = escape_string(latex_str)
    if blockquote:
        script_content = NODE_SCRIPT_TEMPLATE_MATH_MODE % (escaped,)
    else:
        script_content = NODE_SCRIPT_TEMPLATE_INLINE % (escaped,)

    temp_script = tempfile.mktemp()
    with open(temp_script, "w") as fh:
        fh.write(script_content)

    if py.path.local.sysfind("node") is None:
        raise RuntimeError("`node` must be installed")

    node_result = subprocess.check_output(["node", temp_script])
    result = node_result.strip().decode("utf-8")
    result = utf8_to_html_entities(result)
    as_hex = binascii.hexlify(result.encode("utf-8")).decode("ascii")
    wrapped_element = "<html-literal>{}</html-literal>".format(as_hex)
    if blockquote:
        return KATEX_BLOCK_TEMPLATE % (wrapped_element,)
    else:
        return wrapped_element


def verify_template(filename):
    with open(filename, "r") as file_obj:
        content = file_obj.read()
    # Don't allow templated content to be on the boundary of a
    # parenthetical expression.
    if "({{" in content:
        raise ValueError("Invalid content", filename)
    if "}})" in content:
        raise ValueError("Invalid content", filename)


def get_templates():
    result = []
    for match in glob.glob(os.path.join(TEMPLATES_DIR, "*.template")):
        _, template_name = os.path.split(match)
        template = ENV.get_template(template_name)
        verify_template(template.filename)
        result.append(template)

    return result


def get_md5_sum(filename):
    with open(filename, "rb") as fh:
        hash_ = hashlib.md5()
        hash_.update(fh.read())
    digest_bytes = hash_.digest()
    return binascii.hexlify(digest_bytes).decode("ascii")


def write_template(template):
    name, ext = os.path.splitext(template.name)
    if ext != ".template":
        raise ValueError(template.name)
    # This assumes we are running in the root of the repository.
    new_filename = os.path.join(RENDERED_DIR, "{}.md".format(name))

    md5_sum = get_md5_sum(template.filename)
    relative_filename = os.path.relpath(template.filename, BASE_DIR)
    if not FORCE_RENDER and md5_sum == TEMPLATE_HASHES.get(relative_filename):
        if os.path.exists(new_filename):
            print("Already up-to-date: {}".format(relative_filename))
            return

    print("Writing {}".format(new_filename))
    if not os.path.isdir(RENDERED_DIR):
        os.mkdir(RENDERED_DIR)
    with open(new_filename, "w") as fh:
        rendered_file = template.render(get_katex=get_katex)
        fh.write(rendered_file)
        # Make sure the file has a trailing newline.
        if rendered_file[-1] != "\n":
            fh.write("\n")

    TEMPLATE_HASHES[relative_filename] = md5_sum
    with open(TEMPLATE_HASHES_FILENAME, "w") as fh:
        json.dump(
            TEMPLATE_HASHES,
            fh,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        )
        fh.write("\n")


if __name__ == "__main__":
    for template in get_templates():
        write_template(template)
