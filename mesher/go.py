#!#!/usr/bin/env python

import json
import logging

from sys import argv
from subprocess import Popen, PIPE
from datetime import datetime

# host = 'idhavea.beer'
# hlist = ['idhavea.beer', 'google.com', 'myspace.com', 'idhavea.beer']


script, host = argv

def make_logger(app):
    logging.basicConfig(format='%(asctime)s - %(name)s - ' \
                                  '%(levelname)s - %(message)s',
                    level=logging.ERROR,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    # handlers=[
                    #         logging.FileHandler(filename = app + '.log'),
                    #         logging.StreamHandler()
                    #         ],
                    filename= app + '.log'
                    )
    logger = logging.getLogger(app)
    return logger


def ping(host):
    msg = 'pinging {}'
    logger.info(msg.format(host))
    command = ['ping', '-c', '5', host]
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    o_dict = {}
    o_dict['ping_rc'] = rc
    o_dict['ping_output'] = output
    o_dict['ping_error'] = err
    o_dict['destination'] = host
    return o_dict

def run_diag(host, o_dict):
    msg = '{} did not respond to pings, collectin data'
    logger.info(msg.format(host))
    dt_string = datetime.now().strftime("%H:%M:%S")

    check_arp = ['arp', '-a']
    check_neigh = ['ip', 'neigh']
    check_host = ['ip', 'neigh', 'show', host]
    location = '/root/pcaps/{}_dump.pcap'
    tcpdump = ['tcpdump', '-nni', 'eth1', '-c', '10000', '-s', '65535',
               '-w', location.format(dt_string)]

    p = Popen(check_arp, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['arp_table'] = p.communicate()[0]

    p = Popen(check_neigh, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['ip_neighbors'] = p.communicate()[0]

    p = Popen(check_host, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['ip_neigh_explicit'] = p.communicate()[0]

    p = Popen(tcpdump, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['capture_name'] = location.format(dt_string)

    o_dict['event_time'] = dt_string

    return o_dict




def run(host):
    hlist = []
    hlist.append(host)
    while True:
        for host in hlist:
            o_dict = ping(host)
            """ ping return codes? IE should be fine to match against 0
            Success: code 0
            No reply: code 1
            Other errors: code 2 """

            if o_dict['ping_rc'] == 0:
                msg = 'Successful 5 count ping to {}'
                logger.info(msg.format(host))
                logger.error('fake error emssage, it worked')
                continue

            else:
                run_diag(host, o_dict)
                msg = 'event detected\n{}'
                logger.error(msg.format(json.dumps(o_dict, indent=4)))
                print(msg.format(json.dumps(o_dict, indent=4)))
                "don't really need nice logging rn"
                # for k,v in o_dict.items():
                #     msg = ('{}:\n{}')
                #
                #     if not v:
                #         v = 'Null'
                #
                #     if isinstance(v, str):
                #         logger.error(msg.format(k,v.decode('utf-8')))
                #
                #     else:
                #         logger.error(msg.format(k,v))

if __name__ == "__main__":
    logger = make_logger('mesher')
    print('Logging to ./mesher.log')
    run(host)
