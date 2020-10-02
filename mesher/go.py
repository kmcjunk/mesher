#!#!/usr/bin/env python

import socket
import fcntl
import struct

from subprocess import Popen, PIPE

hlist = ['idhavea.beer', 'google.com', 'myspace.com', 'idhavea.beer']
host = 'idhavea.beer'
# host = 'google.com'

# command = f'ping -c 1 {host}'
#
# output = subprocess.call(command)
# print(output)

""" Find my own IP / dont work"""
# def get_ip_address(ifname):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     return socket.inet_ntoa(fcntl.ioctl(
#         s.fileno(),
#         0x8915,  # SIOCGIFADDR
#         struct.pack('256s', ifname[:15])
#     )[20:24])
#
# get_ip_address('en0')

while True:
    for i in hlist:
        print(i)
        
for host in hlist:
    command = ['ping', '-c', '5', host]
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    # return code 2 = cant connect
    """ ping return codes? IE should be fine to match against 0
    Success: code 0
    No reply: code 1
    Other errors: code 2 """
    if rc == 0:
        print(f'ping successful on {host}')
    else:
        print(f"couldn't connect to {host}")
        print(rc, output.decode('utf-8'))


#
# def ping():
#     try:
#         output = subprocess.check_output(command, shell=True)
#
#     except:
#         return False
#
#     return True
#
# print(ping())
