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

import glob
import errno
import os
import shutil
import subprocess

import nox
import psutil
import py.path


nox.options.error_on_external_run = True

DEFAULT_INTERPRETER = "3.12"
PRINT_SEP = "=" * 60
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "content")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CONF_FILE = os.path.join(BASE_DIR, "pelicanconf.py")
ALT_CONF_FILE = os.path.join(BASE_DIR, "pelicanconf_with_pagination.py")
DEBUG = "DEBUG" in os.environ
PORT = os.environ.get("PORT")


def get_path(*names):
    return os.path.join(BASE_DIR, *names)


def _render(session, env=None):
    # I will typically run this via
    #   PATH="${PATH}:${HOME}/.nodenv/versions/${VERSION}/bin" nox -s render
    # because I don't have a ``node`` executable on my default ``${PATH}``.
    if py.path.local.sysfind("node") is None:
        session.skip("`node` must be installed")
    if py.path.local.sysfind("npm") is None:
        session.skip("`npm` must be installed")

    session.run("npm", "install", external=True)
    script = get_path("render_jinja2_templates.py")
    session.run("python", script, env=env)


@nox.session(py=DEFAULT_INTERPRETER)
def render(session):
    """Render blog posts from templates.

    If the post has already been rendered, this will check the file hash against
    a stored mapping of hashes and do nothing if confirmed.
    """
    session.install("--requirement", "render-requirements.txt")
    _render(session)


@nox.session(py=DEFAULT_INTERPRETER)
def rerender(session):
    """Re-render blog posts from templates."""
    session.install("--requirement", "render-requirements.txt")
    _render(session, env={"FORCE_RENDER": "true"})


def _generate(
    session, pelican_opts, regenerate=False, conf_file=CONF_FILE, env=None
):
    args = [os.path.join(session.bin, "pelican")]
    if regenerate:
        args.append("-r")
    args.extend([INPUT_DIR, "-o", OUTPUT_DIR, "-s", conf_file])
    args.extend(pelican_opts)
    session.run(*args, env=env)


def get_pelican_opts():
    pelican_opts = []
    if DEBUG:
        pelican_opts.append("-D")
    return pelican_opts


@nox.session(py=DEFAULT_INTERPRETER)
def html(session):
    """(Re)-generate the web site."""
    pelican_opts = get_pelican_opts()
    session.install("--requirement", "html-requirements.txt")

    # 1. Render
    print("Rendering templates...")
    print(PRINT_SEP)
    _render(session)
    print(PRINT_SEP)
    # 2. Build HTML with paging.
    print("Making first pass with paging")
    print(PRINT_SEP)
    env = {"PYTHONPATH": get_path()}
    _generate(session, pelican_opts, conf_file=ALT_CONF_FILE, env=env)
    print(PRINT_SEP)
    # 3. Keep around the paged index files and nothing else.
    print("Storing paging index*.html files for re-use")
    print("    and removing paged output.")
    print(PRINT_SEP)
    index_files = glob.glob(os.path.join(OUTPUT_DIR, "index*.html"))
    for filename in index_files:
        session.run(shutil.move, filename, BASE_DIR)
    session.run(shutil.rmtree, OUTPUT_DIR, ignore_errors=True)
    print(PRINT_SEP)
    # 4. Build HTML without paging.
    print("Making second pass without paging")
    print(PRINT_SEP)
    _generate(session, pelican_opts, env=env)
    print(PRINT_SEP)
    # 5. Add back paging information.
    print("Putting back paging index*.html files")
    print(PRINT_SEP)
    session.run(os.remove, os.path.join(OUTPUT_DIR, "index.html"))
    index_files = glob.glob(os.path.join(BASE_DIR, "index*.html"))
    for filename in index_files:
        session.run(shutil.move, filename, OUTPUT_DIR)
    print(PRINT_SEP)
    # 6. Delete generated pages that are unused
    print("Removing unwanted pages")
    print(PRINT_SEP)
    session.run(remove_file, os.path.join(OUTPUT_DIR, "authors.html"))
    session.run(
        shutil.rmtree, os.path.join(OUTPUT_DIR, "author"), ignore_errors=True
    )
    session.run(remove_file, os.path.join(OUTPUT_DIR, "categories.html"))
    session.run(
        shutil.rmtree, os.path.join(OUTPUT_DIR, "category"), ignore_errors=True
    )
    session.run(remove_file, os.path.join(OUTPUT_DIR, "tags.html"))
    print(PRINT_SEP)
    # 7. Rewrite URL paths for the pagination feature.
    print("Rewriting paths for paging index*.html files.")
    print(PRINT_SEP)
    script = get_path("rewrite_custom_pagination.py")
    session.run("python", script)
    print(PRINT_SEP)


def remove_file(filename):
    try:
        os.remove(filename)
    except OSError as exc:
        # errno.ENOENT = no such file or directory
        if exc.errno != errno.ENOENT:
            raise


@nox.session(py=DEFAULT_INTERPRETER)
def regenerate(session):
    """Regenerate files upon modification.

    This runs a daemon that waits on file changes and updates generated
    content when files are updated.
    """
    pelican_opts = get_pelican_opts()
    session.install("--requirement", "html-requirements.txt")

    env = {"PYTHONPATH": get_path()}
    _generate(session, pelican_opts, regenerate=True, env=env)


@nox.session(py=DEFAULT_INTERPRETER)
def serve(session):
    """"Serve site at http://localhost:${PORT}'."""
    script = get_path("pelican_server.py")
    session.cd(OUTPUT_DIR)
    if PORT is None:
        session.run("python", script)
    else:
        session.run("python", script, PORT)


@nox.session(py=DEFAULT_INTERPRETER)
def serve_local(session):
    """Serve at http://192.168.XX.YY:8001."""
    script = get_path("get_local_ip.py")
    local_ip = session.run("python", script, silent=True)
    script = get_path("pelican_server.py")

    session.cd(OUTPUT_DIR)
    # ``root`` doesn't know about our virtualenv.
    py_exe = os.path.join(session.bin, "python")
    session.run(py_exe, script, "8001", local_ip.strip())


@nox.session(py=DEFAULT_INTERPRETER)
def dev_server(session):
    """Start / restart ``develop_server.sh``.

    Uses ``${PORT}`` environment variable.
    """
    script = get_path("develop_server.sh")
    if PORT is None:
        session.run(script, "restart")
    else:
        session.run(script, "restart", PORT)


def get_pelican_pid():
    try:
        with open(get_path("pelican.pid"), "r") as fh:
            return int(fh.read())
    except (OSError, ValueError):
        return None


def get_srv_pid():
    try:
        with open(get_path("srv.pid"), "r") as fh:
            return int(fh.read())
    except (OSError, ValueError):
        return None


@nox.session(py=False)
def stop_server(session):
    """Stop local server."""
    pelican_pid = session.run(get_pelican_pid)
    srv_pid = session.run(get_srv_pid)
    if pelican_pid is None:
        if srv_pid is None:
            session.error("`pelican.pid` and `srv.pid` files invalid")
        else:
            session.error("`pelican.pid` file invalid")
    if srv_pid is None:
        session.error("srv.pid` file invalid")

    pelican_proc = psutil.Process(pelican_pid)
    srv_proc = psutil.Process(srv_pid)
    session.run(pelican_proc.kill)
    session.run(srv_proc.kill)


@nox.session(py=DEFAULT_INTERPRETER)
def update_requirements(session):
    if py.path.local.sysfind("git") is None:
        session.skip("`git` must be installed")

    # Install all dependencies.
    session.install("pip-tools")

    # Update all of the requirements file(s).
    names = ("render", "html")
    for name in names:
        in_name = "{}-requirements.in".format(name)
        txt_name = "{}-requirements.txt".format(name)
        session.run("rm", "-f", txt_name, external=True)
        session.run(
            "pip-compile",
            "--generate-hashes",
            "--output-file",
            txt_name,
            in_name,
        )
        session.run("git", "add", txt_name, external=True)


@nox.session(python=DEFAULT_INTERPRETER)
def blacken(session):
    session.install("black")
    file_list_str = subprocess.check_output(["git", "ls-files", "*.py"])
    file_list = file_list_str.decode("ascii").strip().split("\n")
    session.run("black", "--line-length=79", *file_list)


@nox.session(py=False)
def clean(session):
    """Remove the generated files."""
    dir_paths = (
        OUTPUT_DIR,
        get_path("__pycache__"),
        get_path("node_modules"),
        get_path("pelican-plugins", "__pycache__"),
    )
    for dir_path in dir_paths:
        session.run(shutil.rmtree, dir_path, ignore_errors=True)
