#!/usr/bin/env python

import json
import logging
import multiprocessing
import os
import signal
import time

from sys import argv
from subprocess import Popen, PIPE
from datetime import datetime



# script, host = argv

hlist = ['ip',
         'ip',
         'ip',
         'ip',
         ]

global pid

def make_logger(app):
    logging.basicConfig(format='%(asctime)s - %(name)s - ' \
                                  '%(levelname)s - %(message)s',
                    level=logging.ERROR,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    # handlers=[
                    #         logging.FileHandler(filename = app + '.log'),
                    #         logging.StreamHandler()
                    #         ],
                    filename= 'mesher.log'
                    # filename= 'mesher.log'

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

def check_pid(pid):
    print('checkpid')
    ps = 'ps awwffuxxx | grep {}'
    return os.system(ps.format(pid))


def run_diag(host, o_dict, tcp_pid=None):
    msg = '{} did not respond to pings, collectin data'
    logger.info(msg.format(host))
    dt_string = datetime.now().strftime("%H:%M:%S")
    o_dict['event_time'] = dt_string

    check_arp = ['arp', '-a']
    check_neigh = ['ip', 'neigh']
    check_host = ['ip', 'neigh', 'show', host]

    p = Popen(check_arp, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['arp_table'] = p.communicate()[0]

    p = Popen(check_neigh, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['ip_neighbors'] = p.communicate()[0]

    p = Popen(check_host, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    o_dict['ip_neigh_explicit'] = p.communicate()[0]

    "I think try key error, if except - go? have a check on pid? but how"
    "how to ger around an infintite loop on inserts? insert on run()"
    "if not - insert pid. "

    location = 'pcaps/{}_{}_dump.pcap'
    tcpdump = ['tcpdump', '-nni', 'eth1', '-c', '10000', '-s', '65535',
               '-w', location.format(host, dt_string)]
    p = Popen(tcpdump, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    rc = p.returncode
    time.sleep(90)
    kill = 'kill {}'
    os.system(kill.format(p.pid))

    o_dict['tcp_pid'] = p.pid
    o_dict['capture_name'] = location.format(host, dt_string)

    return o_dict




def run(host):
    o_dict = ping(host)
    """ ping return codes? IE should be fine to match against 0
    Success: code 0
    No reply: code 1
    Other errors: code 2 """

    if o_dict['ping_rc'] == 0:
        msg = 'Successful 5 count ping to {}'
        logger.info(msg.format(host))
        pass

    else:
        run_diag(host, o_dict,)
        msg = 'event detected\n{}'
        logger.error(msg.format(json.dumps(o_dict, indent=4)))
        print(msg.format(json.dumps(o_dict, indent=4)))
        #     "don't really need nice logging rn"
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
    pool = multiprocessing.Pool(processes=len(hlist))
    try:
        while True:
            pool.map_async(run, hlist).get(9999999)
    except KeyboardInterrupt:
        pool.terminate()
        print "killin tn lol"
        exit(0)
        pool.terminate()
        pool.join()
    except multiprocessing.TimeoutError as ex:
            print 'timeout'

    # run(host)
