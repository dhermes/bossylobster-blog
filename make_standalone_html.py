#!/usr/bin/env python

"""Command line tool to assist with staging posts during edit.

Staging HTML from output/ as a standalone HTML file will not
work since most CSS/JS assets are relative links. This simply
re-writes all relative links as absolute links relative to
the live site (blog.bossylobster.com).

For example, while working on "constantly-seek-criticism.html",
running

$ ./make_standalone_html.py --year 2014 --month 12 \
> --filename constantly-seek-criticism.html

resulted in the creation of $GIT_ROOT/constantly-seek-criticism.html
which was then uploaded to Google Drive to be served as HTML.
"""

import argparse
import os

from BeautifulSoup import BeautifulSoup


PUBLIC_ROOT = 'https://blog.bossylobster.com'
BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'output')


def make_tag_checker(attr_name):

    def check_tag(tag):
        if not tag.has_key(attr_name):
            return False

        actual_attr_val = tag[attr_name]
        # Only accept relative URI, but not protocol relative.
        if not actual_attr_val.startswith('/'):
            return False

        return (not actual_attr_val.startswith('//'))

    return check_tag


def replace_in_html_string(html, attr_name, attr_val):
    old_text = '%s="%s"' % (attr_name, attr_val)
    new_attr_val = PUBLIC_ROOT + attr_val
    new_text = '%s="%s"' % (attr_name, new_attr_val)
    return html.replace(old_text, new_text)


def replace_attributes(html, soup, attr_name):
    matches = soup.findAll(make_tag_checker(attr_name))
    for match in matches:
        attr_val = match[attr_name]
        html = replace_in_html_string(html, attr_name, attr_val)
        # Update the mutable BeautifulSoup instance as well.
        match[attr_name] = PUBLIC_ROOT + match[attr_name]

    # Return new string since immutable.
    return html


def load_soup(year, month, filename):
    path = os.path.join(BASE_PATH, str(year), str(month), filename)
    with open(path, 'r') as fh:
        html = fh.read()
    return html, BeautifulSoup(html)


def update_links(year, month, filename):
    html, soup = load_soup(year, month, filename)
    html = replace_attributes(html, soup, 'href')
    html = replace_attributes(html, soup, 'src')

    return html


def write_cleaned_html(year, month, filename):
    new_html = update_links(year, month, filename)
    new_file = os.path.abspath(os.path.join(BASE_PATH, '..', filename))
    with open(new_file, 'w') as fh:
        fh.write(new_html)
        if new_html[-1] != '\n':
            fh.write('\n')


def get_parser():
    parser = argparse.ArgumentParser(
        description=('Format compiled post HTML to be standalone by '
                     're-writing relative links.'))
    parser.add_argument('--year', type=int, required=True,
                        help='Year post was published.')
    parser.add_argument('--month', type=int, required=True,
                        help='Month post was published.')
    parser.add_argument('--filename', required=True,
                        help='Name of the post within the year/month.')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    write_cleaned_html(args.year, args.month, args.filename)


if __name__ == '__main__':
    main()
