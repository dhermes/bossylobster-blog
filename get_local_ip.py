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

import contextlib
import socket


def get_ipv4_address():
    # H/T: https://stackoverflow.com/a/166589/1068170
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with contextlib.closing(sock):
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]


if __name__ == "__main__":
    print(get_ipv4_address())
