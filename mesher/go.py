#!#!/usr/bin/env python

import json
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

def ping(host):
    command = ['ping', '-t', '3', '-c', '5', host]
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    o_dict = {}
    o_dict['return_code'] = rc
    o_dict['output'] = output
    o_dict['error'] = err
    return o_dict

def run_diag(host):
    print('checking shit')
    check_arp = ['arp', '-a']
    check_neigh = ['ip', 'neigh']
    check_host = ['ip', 'neigh', 'show', host]

    # check_list = [check_arp, check_neigh, check_host]

    p = Popen(check_arp, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['arp_table'] = p.communicate()[0]

    p = Popen(check_neigh, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['ip_neighbors'] = p.communicate()[0]

    p = Popen(check_host, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['ip_neigh_explicit'] = p.communicate()[0]


    return o_dict


for host in hlist:
    o_dict = ping(host)
    print(o_dict)
    """ ping return codes? IE should be fine to match against 0
    Success: code 0
    No reply: code 1
    Other errors: code 2 """

    if o_dict['return_code'] == 0:
        continue

    else:
        print(o_dict['output'])
        run_diag(host)
        print(json.dumps(o_dict, indent=4))



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
