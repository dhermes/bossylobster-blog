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

"""Markdown extension for inline HTML.

Inline HTML (e.g.
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#html)
does not play well with Markdown when it uses special characters like ``*``
and ``_``. For example:

.. code-block:: html

    <dd>Does *not* work **very** well. Use HTML <em>tags</em>.</dd>

may result in emphasized ``<em>not</em>`` rather than the literal ``*not*``.

This extension works around that by converting blocks of the form
``<html-literal>{hex_block}</html-literal>`` into raw HTML **after** the
Markdown has been processed. The ``hex_block`` content is just the literal
HTML, encoded as UTF-8 and then converted from bytes to hexadecimal
representations of each byte.

When creating this, I referenced some documentation for creating Markdown
extensions:

* https://python-markdown.github.io/extensions/api/#postprocessors for how to
  write a postprocessor
* https://python-markdown.github.io/extensions/api/#extendmarkdown for how
  to integrate my postprocessor into an extension
* https://python-markdown.github.io/extensions/api/#ordereddict for use of
  ``end_``, which makes the postprocessor run after all other registered
  postprocessors
"""


import binascii
import re

import markdown.extensions
import markdown.postprocessors


OPEN = "<html-literal>"
CLOSE = "</html-literal>"
# NOTE: *? is non-greedy
HTML_LITERAL_RE = re.compile(OPEN + "(.*?)" + CLOSE)


class PostProcessLiterals(markdown.postprocessors.Postprocessor):
    def run(self, text):
        result = text
        for hex_block in HTML_LITERAL_RE.findall(text):
            wrapped = OPEN + hex_block + CLOSE
            unwrapped = binascii.unhexlify(hex_block.encode("ascii")).decode(
                "utf-8"
            )
            result = result.replace(wrapped, unwrapped)
        return result


class ExpandLiteral(markdown.extensions.Extension):
    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add(
            "expand_html_literal", PostProcessLiterals(md), "_end"
        )
