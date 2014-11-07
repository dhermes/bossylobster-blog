import datetime
import glob
import os


DATE_STRING_FORMAT = '%Y-%m-%d'


for post_filename in glob.glob('content/*md'):
    directory, post_filename = os.path.split(post_filename)
    if directory != 'content':
        raise ValueError((directory, post_filename))

    year, month, day, the_rest = post_filename.split('-', 3)
    date_stamp = '%s-%s-%s' % (year, month, day)
    try:
        date = datetime.datetime.strptime(date_stamp, DATE_STRING_FORMAT)
    except ValueError:
        print 'Parsing date failed for', post_filename
        raise
