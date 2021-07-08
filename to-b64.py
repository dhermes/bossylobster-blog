import base64
import binascii
import sys

v0 = sys.argv[1]
v1 = binascii.unhexlify(v0)
v2 = base64.b64encode(v1)
v3 = v2.decode("ascii")
print(v3)
