#!/usr/bin/env python

# H/T: http://stackoverflow.com/a/10350424/1068170
import socket
import subprocess
import re


PATTERN = re.compile(
    r'inet\s*\w*\S*:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')


def get_ipv4_address():
    proc = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
    ifconfig_resp, stderr = proc.communicate()
    if stderr is not None:
        raise ValueError('ifconfig failed')
    inet_addrs = [match for match in PATTERN.findall(ifconfig_resp)
                  if not match.startswith('127.')]
    if len(inet_addrs) != 1:
        raise ValueError(('Non-unique result', inet_addrs))
    return inet_addrs[0]


if __name__ == '__main__':
    print get_ipv4_address()
