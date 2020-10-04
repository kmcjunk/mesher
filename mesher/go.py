#!#!/usr/bin/env python

import json
from sys import argv

from subprocess import Popen, PIPE
from datetime import datetime

# host = 'idhavea.beer'
# hlist = ['idhavea.beer', 'google.com', 'myspace.com', 'idhavea.beer']


script, host = argv

def make_logger(app):
    logger = logging.getLogger(app)
    logging.basicConfig(format='%(asctime)s - %(name)s - ' \
                                  '%(levelname)s - %(message)s',
                    level=logging.ERROR,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    handlers=[
                            logging.FileHandler('%s.log') % app,
                            logging.StreamHandler()
                            ]
                    )
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
    check_arp = ['arp', '-a']
    check_neigh = ['ip', 'neigh']
    check_host = ['ip', 'neigh', 'show', host]

    p = Popen(check_arp, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['arp_table'] = p.communicate()[0]

    p = Popen(check_neigh, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['ip_neighbors'] = p.communicate()[0]

    p = Popen(check_host, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['ip_neigh_explicit'] = p.communicate()[0]

    return o_dict




def run(host):
    logger = make_logger('mesher')
    hlist = []
    hlist.append(host)
    for host in hlist:
        o_dict = ping(host)
        """ ping return codes? IE should be fine to match against 0
        Success: code 0
        No reply: code 1
        Other errors: code 2 """

        if o_dict['ping_rc'] == 0:
            msg = 'Successful 5 count ping to {}'
            print(msg.format(host))
            continue

        else:
            run_diag(host, o_dict)
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            msg = '// {} {}'
            logger.error(msg.format(dt_string, 'WE GOT A PROBLEM, ITS PACKET LOSS\n'))
            for k,v in o_dict.items():
                msg = ('{}:\n{}')
                if not v:
                    v = 'Null'
                if isinstance(v, str):
                    print(msg.format(k,v.decode('utf-8')))

                else:
                    print(msg.format(k,v))

if __name__ == "__main__":
    run(host)
