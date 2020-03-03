
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tornado
import tornado.web
from ipabase import easylog, read_json_conf
from tornado.options import define, options

class Application(tornado.web.Application):
    def __init__(self, handler_map, opts, service_conf):
        settings = dict(
                debug = opts.debug,
                xsrf_cookies = False,
                autoescape = None,
                compress_response = True
                )
        tornado.web.Application.__init__(self, handler_map, **settings)
        self.local_cache = {}
        self.service_conf = service_conf


def start_httpserver(handler_map, opts):
    service_conf = read_json_conf(opts.conf_file)
    if not service_conf:
        easylog.error('Failed to get the config file:%s', opts.conf_file)
        return

    app = Application(handler_map, opts, service_conf)
    app.listen(opts.port)
    tornado.ioloop.IOLoop.current().start()
