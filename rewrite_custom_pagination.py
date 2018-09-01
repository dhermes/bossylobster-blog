# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Manually handling pagination since it is broken in Pelican:
#     https://github.com/getpelican/pelican/issues/1223

import os
import re
import shutil

from pelicanconf import SITEURL


PAGE_DIR = os.path.join("output", "page")
MATCHER = re.compile(r"^index(?P<page>\d+).html$")


def make_page_dir():
    if not os.path.isdir(PAGE_DIR):
        os.mkdir(PAGE_DIR)


def rewrite_links(page_num, filename=None):
    filename = filename or os.path.join(PAGE_DIR, "%d.html" % (page_num,))
    with open(filename, "r") as fh:
        content = fh.read()

    prev_link = 'href="%s/index%d.html"' % (SITEURL, page_num - 1)
    if content.count(prev_link) > 1:
        raise ValueError(
            ("Link occurred more than once.", prev_link, filename)
        )

    next_link = 'href="%s/index%d.html"' % (SITEURL, page_num + 1)
    if content.count(next_link) > 1:
        raise ValueError(
            ("Link occurred more than once.", next_link, filename)
        )

    prev_link_new = 'href="%s/page/%d"' % (SITEURL, page_num - 1)
    content = content.replace(prev_link, prev_link_new)
    next_link_new = 'href="%s/page/%d"' % (SITEURL, page_num + 1)
    content = content.replace(next_link, next_link_new)
    with open(filename, "w") as fh:
        fh.write(content)


def move_page(page_num):
    old_page = os.path.join("output", "index%d.html" % (page_num,))
    new_page = os.path.join(PAGE_DIR, "%d.html" % (page_num,))
    make_page_dir()
    shutil.move(old_page, new_page)
    print("Moved {} to {}".format(old_page, new_page))
    rewrite_links(page_num, filename=new_page)


def main():
    # Assumes this is being run from the root of the repository.
    for filename in os.listdir("output"):
        match = MATCHER.match(filename)
        if match is not None:
            page_num = int(match.group("page"))
            move_page(page_num)
        elif filename == "index.html":
            filename = os.path.join("output", "index.html")
            rewrite_links(1, filename=filename)


if __name__ == "__main__":
    main()
