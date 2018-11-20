#!/usr/bin/python

import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
message = 'whoami' # message to sign
key = RSA.importKey(open('cascade_private_unencrypted.pem').read())
h = SHA512.new(message)
signer = PKCS1_v1_5.new(key)
signature = signer.sign(h)

print base64.b64encode(signature)
