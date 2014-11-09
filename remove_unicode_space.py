# One off script to remove u'\u200b' from markdown files.
# It's unclear if they are due to the Atom feed, due to my
# actual content in blogger or due to the pelican-import
# tool.

import glob

REMAP_CHARS = {
    u'\u200b': '',  # ZERO WIDTH SPACE CHAR
    u'\u00a0': '',  # NO BREAK SPACE CHAR
    u'\u2013': '&ndash;',  # EN DASH
    u'\u2014': '&mdash;',  # EM DASH
    u'\u2019': '\'',  # RIGHT SINGLE QUOTE
    u'\u201c': '"',  # LEFT DOUBLE QUOTE
    u'\u201d': '"',  # RIGHT DOUBLE QUOTE
    u'\u2212': '-',  # MINUS SIGN
}


for filename in glob.glob('content/*.md'):
    with open(filename, 'r') as fh:
        content = fh.read()
    content_as_unicode = content.decode('utf8')
    reduced_content = content_as_unicode

    for char, new_char in REMAP_CHARS.iteritems():
        reduced_content = reduced_content.replace(char, new_char)
    if reduced_content != content_as_unicode:
        print 'Over-writing', filename
        with open(filename, 'w') as fh:
            fh.write(reduced_content.decode('ascii'))
