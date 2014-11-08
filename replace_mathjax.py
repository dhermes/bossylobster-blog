import argparse
import os
import re
import subprocess


# I have no idea why this works, but run
#    >>> re.escape(r'\\(stuff\\)')
#    '\\\\\\(stuff\\\\\\)'
INLINE_MATCHER = re.compile(
    '\\\\\\\\\\((?P<inline>.*?)\\\\\\\\\\)',
    flags=re.MULTILINE,
)
INLINE_REPLACE = '{{ get_katex("\g<inline>") }}'
MATH_MODE_MATCHER = re.compile(
    '\\\\\\\\\\[(?P<mathmode>.*?)\\\\\\\\\\]',
    flags=re.MULTILINE,
)
MATH_MODE_REPLACE = (
    '\n\n{{ get_katex("\g<mathmode>", blockquote=True) }}\n\n')


def replace_mathjax(str_val):
    after_inline = INLINE_MATCHER.sub(INLINE_REPLACE, str_val)
    after_math_mode = MATH_MODE_MATCHER.sub(MATH_MODE_REPLACE,
                                            after_inline)
    return after_math_mode


def make_template(markdown_name):
    name, ext = os.path.splitext(markdown_name)
    if ext != '.md':
        raise ValueError(markdown_name)
    markdown_path = os.path.join('content', markdown_name)
    with open(markdown_path, 'r') as fh:
        markdown_contents = fh.read()

    template_path = os.path.join('content', name + '.template')
    with open(template_path, 'w') as fh:
        fh.write(markdown_contents)
    subprocess.call(['git', 'add', template_path])
    print 'Added identical Markdown content to git.'

    template_contents = replace_mathjax(markdown_contents)
    with open(template_path, 'w') as fh:
        fh.write(template_contents)
    print 'Added KaTeX blocks but not staging.'


def main():
    description = ('Convert a markdown file to a Jinja2 template '
                   'with MathJax converted to KaTeX blocks.')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--markdown-name', dest='markdown_name',
        help='Name (not path) of file to be converted.')
    args = parser.parse_args()
    make_template(args.markdown_name)


if __name__ == '__main__':
    main()
