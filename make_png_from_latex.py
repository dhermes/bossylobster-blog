from __future__ import print_function

import base64
import json
import os
import shutil
import subprocess
import tempfile


STANDALONE_TEX_FILE_TEMPLATE = r"""\documentclass{article}
\usepackage{amsthm,amssymb,amsmath}
\pagestyle{empty}

\begin{document}
%s
\end{document}
"""
TEX_FILE_TEMPLATE = STANDALONE_TEX_FILE_TEMPLATE % (r'\[%s\]',)
SEPARATOR = '\n' + ('=' * 70) + '\n'
DEFAULT_DENSITY = '160x160'
BLOCKQUOTE_DENSITY = '200x200'
LATEX_IMG_NAMES_FILE = 'latex_img_names.json'
with open(LATEX_IMG_NAMES_FILE, 'r') as fh:
    IMAGE_NAMES = json.load(fh)


def get_image_name(latex_str, blockquote=False):
    if not isinstance(latex_str, bytes):
        latex_str = latex_str.encode('ascii')
    str_as_b64 = base64.b64encode(latex_str).decode('ascii')
    if blockquote:
        str_as_b64 += '_block'
    name_value = IMAGE_NAMES.get(str_as_b64)
    if name_value is not None:
        return name_value
    if IMAGE_NAMES:
        max_val = max(IMAGE_NAMES.values())
    else:
        max_val = -1
    new_name_value = max_val + 1

    # Save image names after updating.
    IMAGE_NAMES[str_as_b64] = new_name_value
    with open(LATEX_IMG_NAMES_FILE, 'w') as fh:
        json.dump(IMAGE_NAMES, fh, indent=2, sort_keys=True,
                  separators=(',', ': '))
        fh.write('\n')

    return new_name_value


def check_exists(latex_str, image_name):
    png_name = '%d.png' % (image_name,)
    final_path = os.path.join('content', 'latex_images', png_name)
    if os.path.exists(final_path):
        print('File exists: {}'.format(final_path))
        print('No need to convert')
        print('    {!r}'.format(latex_str))
        return png_name


def save_equation_to_file(temp_dir, latex_str, image_name, standalone=False):
    print(SEPARATOR)

    template = (STANDALONE_TEX_FILE_TEMPLATE
                if standalone else TEX_FILE_TEMPLATE)

    tex_file_path = os.path.join(temp_dir, '%d.tex' % (image_name,))

    with open(tex_file_path, 'w') as fh:
        fh.write(template % (latex_str,))
    print('Wrote {}'.format(tex_file_path))


def convert_tex_to_dvi(temp_dir, image_name):
    print(SEPARATOR)

    tex_file_path = os.path.join(temp_dir, '%d.tex' % (image_name,))
    latex_cmd = ['latex', '-output-directory', temp_dir,
                 tex_file_path]
    print('Calling')
    print(' '.join(latex_cmd))
    subprocess.call(latex_cmd)


def convert_dvi_to_ps(temp_dir, image_name):
    print(SEPARATOR)

    file_path_root = os.path.join(temp_dir, '%d' % (image_name,))
    dvi_file_path = file_path_root + '.dvi'
    ps_file_path = file_path_root + '.ps'
    dvi_cmd = ['dvips', '-E', dvi_file_path, '-o', ps_file_path]
    print('Calling')
    print(' '.join(dvi_cmd))
    subprocess.call(dvi_cmd)


def convert_ps_to_png_in_repo(temp_dir, image_name, blockquote=False):
    print(SEPARATOR)

    png_name = '%d.png' % (image_name,)
    density = BLOCKQUOTE_DENSITY if blockquote else DEFAULT_DENSITY

    ps_file_path = os.path.join(temp_dir, '%d.ps' % (image_name,))
    png_file_path = os.path.join(temp_dir, png_name)
    convert_cmd = ['convert', '-density', density,
                   ps_file_path, png_file_path]
    print('Calling')
    print(' '.join(convert_cmd))
    subprocess.call(convert_cmd)

    print(SEPARATOR)

    new_path = os.path.join('content', 'latex_images', png_name)
    print('Moving to content/latex_images/')
    shutil.move(png_file_path, new_path)

    print('Adding to git repo')
    subprocess.call(['git', 'add', new_path])

    return png_name


def convert_equation(latex_str, blockquote=False, standalone=False):
    image_name = get_image_name(latex_str, blockquote=blockquote)

    temp_dir = tempfile.mkdtemp()
    png_name = check_exists(latex_str, image_name)
    if png_name is not None:
        return png_name

    save_equation_to_file(temp_dir, latex_str, image_name,
                          standalone=standalone)
    convert_tex_to_dvi(temp_dir, image_name)
    convert_dvi_to_ps(temp_dir, image_name)

    return convert_ps_to_png_in_repo(temp_dir, image_name,
                                     blockquote=blockquote)
