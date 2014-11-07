# Temporary file re-writer to make slugs match
# original titles and make dates reflect the
# posting of the blog post, not the last edit.

import os
import glob
import subprocess


OLD_AUTHOR_LINE = 'Author: Danny Hermes (noreply@blogger.com)'
NEW_AUTHOR_LINE = 'author: Danny Hermes (dhermes@bossylobster.com)'


for relative_path in glob.glob('content/*md'):
    directory, post_filename = os.path.split(relative_path)
    if directory != 'content':
        raise ValueError(relative_path)
    year, month, day, title = post_filename.split('-', 3)

    slug, file_ext = os.path.splitext(title)
    if file_ext != '.md':
        raise ValueError(relative_path)

    date_stamp = '%s-%s-%s' % (year, month, day)

    with open(relative_path, 'r') as fh:
        post_contents = fh.read()

    post_lines = post_contents.split('\n')
    if post_lines[5].strip() != '':
        raise ValueError(relative_path)

    if post_lines[2] != OLD_AUTHOR_LINE:
        raise ValueError(relative_path)
    post_lines[2] = NEW_AUTHOR_LINE

    if not post_lines[4].startswith('Slug: '):
        raise ValueError(relative_path)
    post_lines[4] = 'slug: %s' % (slug,)

    split_tags = post_lines[3].split('Tags:', 1)
    if len(split_tags) == 1 or split_tags[0] != '':
        raise ValueError(relative_path)
    post_lines[3] = 'tags:%s' % (split_tags[1],)

    if not post_lines[1].startswith('Date: '):
        raise ValueError(relative_path)
    post_lines[1] = 'date: %s' % (date_stamp,)

    with open(relative_path, 'w') as fh:
        fh.write('\n'.join(post_lines))
    print 'Adding', relative_path
    subprocess.call(['git', 'add', relative_path])
