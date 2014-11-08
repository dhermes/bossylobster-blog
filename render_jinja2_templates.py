import binascii
import codecs
from Crypto.Hash import MD5
import glob
import json
import os
import re
import subprocess
import tempfile

from jinja2 import Environment, PackageLoader


ENV = Environment(loader=PackageLoader(__name__, 'content'))
NODE_SCRIPT_TEMPLATE = u"""\
katex = require('katex');
value = katex.renderToString("%s");
console.log(value);
"""
KATEX_BLOCK_TEMPLATE = u"""\
<div class="katex-elt"><blockquote>
%s
</blockquote></div>"""
TEMPLATE_HASHES_FILENAME = 'template_hashes.json'
with open(TEMPLATE_HASHES_FILENAME, 'r') as fh:
    TEMPLATE_HASHES = json.load(fh)


def escape_string(latex_str):
    return latex_str.replace('\\', r'\\')


def get_katex(latex_str, blockquote=False):
    escaped = escape_string(latex_str)
    script_content = NODE_SCRIPT_TEMPLATE % (escaped,)

    temp_script = tempfile.mktemp()
    with open(temp_script, 'w') as fh:
        fh.write(script_content)

    node_result = subprocess.check_output(['node', temp_script])
    result = node_result.strip().decode('utf8')
    if blockquote:
        return KATEX_BLOCK_TEMPLATE % (result,)
    else:
        return result


def get_templates():
    result = []
    for match in glob.glob('content/*.template'):
        directory, template_name = os.path.split(match)
        if directory != 'content':
            raise ValueError(match)

        template = ENV.get_template(template_name)
        result.append(template)

    return result


def get_md5_sum(filename):
    with open(filename, 'rb') as fh:
        hash = MD5.new(data=fh.read())
    digest_bytes = hash.digest()
    return binascii.hexlify(digest_bytes)


def write_template(template):
    name, ext = os.path.splitext(template.name)
    if ext != '.template':
        raise ValueError(template.name)

    md5_sum = get_md5_sum(template.filename)
    if md5_sum == TEMPLATE_HASHES.get(template.filename):
        print 'Already up-to-date:', template.filename
        return

    # This assumes we are running in the root of the repository.
    new_filename = 'content/%s.md' % (name,)
    print 'Writing', new_filename
    with codecs.open(new_filename, 'wb', 'utf-8') as fh:
        rendered_file = template.render(get_katex=get_katex)
        fh.write(rendered_file)
        # Make sure the file has a trailing newline.
        if rendered_file[-1] != '\n':
            fh.write('\n')

    TEMPLATE_HASHES[template.filename] = md5_sum
    with open(TEMPLATE_HASHES_FILENAME, 'w') as fh:
        json.dump(TEMPLATE_HASHES, fh, indent=2)


if __name__ == '__main__':
    for template in get_templates():
        write_template(template)
