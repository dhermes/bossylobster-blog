import binascii
from Crypto.Hash import MD5
import glob
import json
import os
import re
import subprocess
import tempfile

from jinja2 import Environment, PackageLoader
from make_svg_from_latex import convert_equation


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

LATEX_IMG_TEMPLATE = '<img src="%s" alt="%s" class="latex-img"></img>'


def escape_string(latex_str):
    return latex_str.replace('\\', r'\\')


def utf8_to_html_entity(char_val):
    ordinal_val = ord(char_val)
    if ordinal_val < 127:
        return char_val
    return '&#%04d;' % (ordinal_val,)


def utf8_to_html_entities(str_val):
    chars = [utf8_to_html_entity(char_val) for char_val in str_val]
    return ''.join(chars)


def get_katex(latex_str, blockquote=False):
    escaped = escape_string(latex_str)
    script_content = NODE_SCRIPT_TEMPLATE % (escaped,)

    temp_script = tempfile.mktemp()
    with open(temp_script, 'w') as fh:
        fh.write(script_content)

    node_result = subprocess.check_output(['node', temp_script])
    result = node_result.strip().decode('utf8')
    result = utf8_to_html_entities(result)
    if blockquote:
        return KATEX_BLOCK_TEMPLATE % (result,)
    else:
        return result


def get_latex_img(latex_str, blockquote=False, standalone=False):
    png_path = convert_equation(latex_str, blockquote=blockquote,
                                standalone=standalone)
    png_uri = '/latex_images/%s' % (png_path,)
    result = LATEX_IMG_TEMPLATE % (png_uri, latex_str)
    if blockquote:
        return '<blockquote class="latex-img">%s</blockquote>' % (result,)
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
    # This assumes we are running in the root of the repository.
    new_filename = 'content/%s.md' % (name,)

    md5_sum = get_md5_sum(template.filename)
    if md5_sum == TEMPLATE_HASHES.get(template.filename):
        if os.path.exists(new_filename):
            print 'Already up-to-date:', template.filename
            return

    print 'Writing', new_filename
    with open(new_filename, 'wb') as fh:
        rendered_file = template.render(get_katex=get_katex,
                                        get_latex_img=get_latex_img)
        fh.write(rendered_file)
        # Make sure the file has a trailing newline.
        if rendered_file[-1] != '\n':
            fh.write('\n')

    TEMPLATE_HASHES[template.filename] = md5_sum
    with open(TEMPLATE_HASHES_FILENAME, 'w') as fh:
        json.dump(TEMPLATE_HASHES, fh, indent=2, sort_keys=True,
                  separators=(',', ': '))
        fh.write('\n')


if __name__ == '__main__':
    for template in get_templates():
        write_template(template)
