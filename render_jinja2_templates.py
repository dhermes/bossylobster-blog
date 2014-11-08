import codecs
import glob
import os

from jinja2 import Environment, PackageLoader


ENV = Environment(loader=PackageLoader(__name__, 'content'))


def get_templates():
    result = []
    for match in glob.glob('content/*.template'):
        directory, template_name = os.path.split(match)
        if directory != 'content':
            raise ValueError(match)

        template = ENV.get_template(template_name)
        result.append(template)

    return result


def write_template(template):
    name, ext = os.path.splitext(template.name)
    if ext != '.template':
        raise ValueError(template.name)

    # This assumes we are running in the root of the repository.
    new_filename = 'content/%s.md' % (name,)
    print 'Writing', new_filename
    with codecs.open(new_filename, 'wb', 'utf-8') as fh:
        rendered_file = template.render()
        fh.write(rendered_file)
        # Make sure the file has a trailing newline.
        if rendered_file[-1] != '\n':
            fh.write('\n')


if __name__ == '__main__':
    for template in get_templates():
        write_template(template)
