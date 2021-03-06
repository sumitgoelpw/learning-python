#!/usr/bin/env python
"""Lookup hostname and ping status on multiple IPs fast and easy.

I used to get a long list of IP addresses to work on, but by looking at the IP
addresses, it was hard for me to determine what systems were we talking about
precisely. So I created this script to give me two things, first, check if IP
address is pingable or not and second to lookup the hostname. I can put all the
IP addresses in a file, one IP address per line, and then run the script with
the -f option and filename to provide the information I needed to figure out my
next step.

The script is known to work with Python 2.
"""

__author__ = 'Sumit Goel'

import sys
import subprocess
import socket
import argparse
import multiprocessing
import fileinput


def usage():
    """Print the usage."""
    print 'Usage: {0} [ -i ip-address ] [ -f filename ]'.format(__file__)


def lookup(ipaddr):
    """Check if the IP/Hostname pingable and lookup the DNS name."""
    ipaddr = ipaddr.lstrip()
    ipaddr = ipaddr.rstrip()
    ipaddr = ipaddr.replace(' ', '')

    response = subprocess.call('ping -c 1 {0}'.format(ipaddr),
                               shell=True,
                               stdout=open('/dev/null', 'w'),
                               stderr=subprocess.STDOUT)

    if response == 0:
        try:
            out = socket.gethostbyaddr(ipaddr)
            print '{0}: Alive, Hostname: {1}'.format(ipaddr, out[0])
        except socket.herror as error:
            print '{0}: Alive, Hostname: {1}'.format(ipaddr, error)
    elif response == 2:
        print '{0}: NO RESPONSE'.format(ipaddr)
    elif response == 68:
        print '{0}: COULD NOT RESOLVE ADDRESS'.format(ipaddr)
    else:
        print '{0}: May be DEAD, Unspecified Error'.format(ipaddr)


def main():
    """Execute the logic."""
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)
    else:
        parser = argparse.ArgumentParser(description='Program checks if IP \
                address is ping-able or not and lookup the hostname.')
        parser.add_argument('-i', metavar='IP Address', dest='ipaddr',
                            help='Specify the IP address')
        parser.add_argument('-f', metavar='Filename', dest='filename',
                            help='Specify the file name and file path \
                            containing the list of IP addresses and ensure \
                            that the IP addresses are listed in one column or \
                            per line')
        try:
            args = parser.parse_args()
        except argparse.ArgumentError, error:
            print 'Error:', str(error)

        if args.ipaddr:
            try:
                socket.inet_aton(args.ipaddr)
            except socket.error, error:
                print 'Error:', str(error)
                sys.exit(1)

            lookup(args.ipaddr)

        if args.filename:
            iplist = fileinput.input(args.filename)
            if __name__ == '__main__':
                psize = multiprocessing.cpu_count()
                parallel = multiprocessing.Pool(processes=psize)
                parallel.map(lookup, iplist)
                parallel.close()
                parallel.join()


if __name__ == '__main__':
    main()

#
# eof
