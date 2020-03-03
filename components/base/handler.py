#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import simplejson as json
from tornado.web import RequestHandler
from ipabase import easylog,IpaJsonEncoder,second2_str24h,object_method_time_usage


class BaseHandler(RequestHandler):
    def initialize(self, *args):
        self.requestid = None

    @object_method_time_usage
    def render_json(self, data, requestid=True, jsonstr=False, indent=False):
        self.set_header('Content-Type', 'application/json')
        if jsonstr:
            data = json.loads(data)
        if requestid:
            data['requestid'] = 'requestid:%s midware_finish:%s' % (self.requestid, second2_str24h(time.time())[11:])

        try:
            data = json.dumps(data, cls=IpaJsonEncoder, indent=indent)
        except Exception as e:
            easylog.exception("%s data:%s", e, data)
            data = {'error':'JSON格式错误(%s)' % e}
            if requestid:
                data['requestid'] = 'requestid:%s midware_finish:%s' % (self.requestid, second2_str24h(time.time())[11:])
            data = json.dumps(data, cls=IpaJsonEncoder)
        try:
            start_time = time.time()
            self.write(data)
            easylog.info('write data length:%.02fKB TIME USAGE:%.4fs', len(data)/1024.0, time.time()-start_time)
            start_time = time.time()
            def after_flush():
                easylog.info('flush finished TIME USAGE:%4fs', time.time()-start_time)
            self.flush(callback=after_flush)
        except Exception as e:
            easylog.doomsday('%s', e)

