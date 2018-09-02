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

"""Account for cases when Markdown and HTML don't play well together.

When HTML is embedded in Markdown, certain `elements`_ do not behave
very well. This is to account for issues when the KaTeX-generated
HTML contains characters that are valid Markdown (e.g. ``*`` and
``_``).

.. _elements: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#inline-html
"""

import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def fix_gcd_post():
    filename = os.path.join(
        BASE_DIR,
        "output",
        "2013",
        "09",
        "calculating-greatest-common-divisor.html",
    )
    with open(filename, "r") as file_obj:
        content = file_obj.read()
    modified = content.replace("p^{<em>}", "p^{*}")
    modified = modified.replace("p^{</em>}", "p^{*}")
    with open(filename, "w") as file_obj:
        file_obj.write(modified)


def fix_fibonacci_fun():
    filename = os.path.join(
        BASE_DIR, "output", "2013", "08", "some-fibonacci-fun-with-primes.html"
    )
    with open(filename, "r") as file_obj:
        content = file_obj.read()
    modified = content.replace('<em p_2="p^2">', "_")
    modified = modified.replace("</em>", "")
    with open(filename, "w") as file_obj:
        file_obj.write(modified)


def main():
    fix_gcd_post()
    fix_fibonacci_fun()


if __name__ == "__main__":
    main()
