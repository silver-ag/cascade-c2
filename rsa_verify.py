#!/usr/bin/python

import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA

key = RSA.importKey(open('cascade_public.pem').read())
h = SHA512.new('') # signed message
verifier = PKCS1_v1_5.new(key)
file = open("testmessage.txt", "r") # file containing signature
if verifier.verify(h, base64.b64decode('YwZmcZ/pLTyUJCnaJm76R2FTVzJbh7Rv8XDUWsjpYkSGtI/CmrzFsvvE/nRdiq77nutJQruGmQJhZWyhEG9pbzWT89KyiBTQwe0dmBeeNZyukIxZp6wt3oJP3oz4aZ09Bm5vOF5MEp+KXDxAk5lXp2zQLDkIXvu46eMPjKhsLWb9sWTRKj+4XqC5pxSrC3x7l3ovGOink2c3n/gb43ZL40rqP58+oj/XvhyBmNJn7bEdsXtrl2FJyrOOF/x+ZtRILR0nbHyvsz6Y9bc7HxQGMTQKYSI/v4Ykpd8MSkAqtUaZLHvsj0lMdM0l+IQJjONgZv4X87nn/auDGDnYLuS6yA==')):
  print "The signature is authentic."
else:
  print "The signature is not authentic."
file.close()
