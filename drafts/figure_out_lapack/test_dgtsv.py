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

import numpy as np


def main():
    lower_diag = np.diag([-1, -2, -1, -1], k=-1)
    diag = np.diag([2, 2, 3, 3, 1], k=0)
    upper_diag = np.diag([-1, -1, -1, -2], k=1)
    A = np.array(lower_diag + diag + upper_diag, dtype=np.float64)

    b_rhs = np.array([[1, 2, 3, 2, 1]], dtype=np.float64).T

    x_lhs = np.linalg.solve(A, b_rhs)

    print(A)
    print(b_rhs)
    print(x_lhs)


if __name__ == "__main__":
    main()
