import os
import time

from flask import abort, Flask, request
import rq

import lib


app = lib.app = Flask(__name__)

if lib.DEBUG:
    methods = ['POST', 'GET']
else:
    methods = ['POST']


lib.login_to_redis()
lib.login_to_cloudflare()
q = rq.Queue(connection=lib.redis)


@lib.check_and_route('/register', methods=methods)
def register():
    name = lib.get_param('name')
    ip = lib.get_param('ip')
    port = lib.get_param('port')
    # print ("Received register from %s:%s" % (ip, port))
    if int(port) != 443:
        #print "Ignoring peers on ports other than 443"
        return "OK"
    else:
        if ip == "23.243.192.92":
            q.enqueue(lib.register, name, ip)
            print ("Enqueued %s:%s" % (ip, port))
        return "OK"

@lib.check_and_route('/unregister', methods=methods)
def unregister():
    name = lib.get_param('name')
    q.enqueue(lib.unregister, name)
    return "OK"
