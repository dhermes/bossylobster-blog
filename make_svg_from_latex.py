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
LATEX_EQUATION_NUMBERS_FILE = 'latex_equation_numbers.json'
with open(LATEX_EQUATION_NUMBERS_FILE, 'r') as fh:
    EQUATION_NUMBERS = json.load(fh)


def get_equation_number(latex_str, blockquote=False):
    str_as_b64 = base64.b64encode(latex_str)
    if blockquote:
        str_as_b64 += '_block'
    name_value = EQUATION_NUMBERS.get(str_as_b64)
    if name_value is not None:
        return name_value
    if EQUATION_NUMBERS:
        max_val = max(EQUATION_NUMBERS.values())
    else:
        max_val = -1
    new_name_value = max_val + 1

    # Save image names after updating.
    EQUATION_NUMBERS[str_as_b64] = new_name_value
    with open(LATEX_EQUATION_NUMBERS_FILE, 'w') as fh:
        json.dump(EQUATION_NUMBERS, fh, indent=2, sort_keys=True,
                  separators=(',', ': '))
        fh.write('\n')

    return new_name_value


def check_exists(latex_str, equation_number):
    svg_name = '%d.svg' % (equation_number,)
    final_path = os.path.join('content', 'latex_images', svg_name)
    if os.path.exists(final_path):
        print 'File exists:', final_path
        print 'No need to convert'
        print '    %r' % (latex_str,)
        return svg_name


def save_equation_to_file(temp_dir, latex_str, equation_number,
                          standalone=False):
    print SEPARATOR

    template = (STANDALONE_TEX_FILE_TEMPLATE
                if standalone else TEX_FILE_TEMPLATE)

    tex_file_path = os.path.join(temp_dir, '%d.tex' % (equation_number,))

    with open(tex_file_path, 'w') as fh:
        fh.write(template % (latex_str,))
    print 'Wrote', tex_file_path


def convert_tex_to_pdf(temp_dir, equation_number):
    print SEPARATOR

    tex_file_path = os.path.join(temp_dir, '%d.tex' % (equation_number,))
    latex_cmd = ['pdflatex', '-output-directory', temp_dir,
                 tex_file_path]
    print 'Calling'
    print ' '.join(latex_cmd)
    subprocess.call(latex_cmd)


def convert_pdf_to_svg_in_repo(temp_dir, equation_number, blockquote=False):
    print SEPARATOR

    svg_name = '%d.svg' % (equation_number,)

    pdf_file_path = os.path.join(temp_dir, '%d.pdf' % (equation_number,))
    cropped_pdf_file_path = os.path.join(temp_dir,
                                         '%d_crop.pdf' % (equation_number,))
    crop_cmd = ['pdfcrop', pdf_file_path, cropped_pdf_file_path]
    print 'Calling'
    print ' '.join(crop_cmd)
    subprocess.call(crop_cmd)

    svg_file_path = os.path.join(temp_dir, svg_name)
    convert_cmd = ['pdftocairo', '-svg', cropped_pdf_file_path, svg_file_path]
    print 'Calling'
    print ' '.join(convert_cmd)
    subprocess.call(convert_cmd)

    print SEPARATOR

    new_path = os.path.join('content', 'latex_images', svg_name)
    print 'Moving to content/latex_images/'
    shutil.move(svg_file_path, new_path)

    print 'Adding to git repo'
    subprocess.call(['git', 'add', new_path])

    return svg_name


def convert_equation(latex_str, blockquote=False, standalone=False):
    equation_number = get_equation_number(latex_str, blockquote=blockquote)

    temp_dir = tempfile.mkdtemp()
    svg_name = check_exists(latex_str, equation_number)
    if svg_name is not None:
        return svg_name

    save_equation_to_file(temp_dir, latex_str, equation_number,
                          standalone=standalone)
    convert_tex_to_pdf(temp_dir, equation_number)

    return convert_pdf_to_svg_in_repo(temp_dir, equation_number,
                                      blockquote=blockquote)
