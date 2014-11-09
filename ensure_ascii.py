# Temp script to make sure only ascii text is used in blog
# posts.

import glob


for filename in glob.glob('content/*md'):
    with open(filename, 'r') as fh:
        content = fh.read()
    unicode_content = content.decode('utf8')
    if content != unicode_content:
        raise ValueError(('utf diff', filename))
    max_char = max(map(ord, unicode_content))
    if max_char > 127:
        raise ValueError(('max char', filename))
