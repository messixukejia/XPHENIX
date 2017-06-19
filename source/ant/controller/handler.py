# coding = utf-8

import BaseHTTPServer

from ant.common.log import *
from ant.controller.mime_type import *

import os
import urlparse

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server,
            dispatcher, merger):

        self.dispatcher = dispatcher
        self.merger = merger

        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request,
                client_address, server)

    def _debug_print_context(self):
        log_debug('======================Handle Request======================')
        log_debug('client_address={}'.format(self.client_address))
        log_debug('command={}'.format(self.command))
        log_debug('path={}'.format(self.path))
        log_debug('parsed_path={}'.format(urlparse.urlparse(self.path)))
        log_debug('request_version={}'.format(self.request_version))
        log_debug('headers={}'.format(self.headers))
        log_debug('==========================================================')

    def do_GET(self):
        self._debug_print_context()

        if self.do_default_filter(): return

        '''
        try:
            parsed_path = urlparse.urlparse(self.path).path
            self.dispatcher.dispatch(parsed_path)
            resp_text = self.dispatcher.conclude_response()
            self.send_resp_header(len(resp_text))
            self.write_context(resp_text)
        except Exception as e:
            log_error("handle url error: {}".format(str(e)))
        '''

        parsed_path = urlparse.urlparse(self.path).path
        self.dispatcher.dispatch(parsed_path)
        resp_text = self.dispatcher.conclude_response()
        self.send_resp_header(len(resp_text))
        self.write_context(resp_text)
    
    def do_POST(self):
        pass
    
    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass
    
    def do_OPTIONS(self):
        pass
    
    def do_HEAD(self):
        pass
    
    def do_TRACE(self):
        pass
    
    def do_CONNECT(self):
        pass

    def send_resp_header(self, obj_length):

        self.send_response(200)
        mime_type = self.get_mime_type()

        self.send_header('Content-type', mime_type + '; charset=UTF-8')
        self.send_header('Content-length', str(obj_length))
        self.end_headers()

        log_debug('response {} with mime type {}.'.format(self.path, mime_type))
    
    def write_context(self, response_str):
        self.wfile.write(response_str)

    def get_mime_type(self):

        parsed_path = urlparse.urlparse(self.path).path
        path, ext = os.path.splitext(parsed_path)

        if not ext:
            return MIME_TYPE_DEFAULT
        
        mime_type = MIME_TYPE_DICT.get(ext, '')

        if mime_type:
            return mime_type
        else:
            return MIME_TYPE_DEFAULT

    def do_default_filter(self):

        if self.path == '/favicon.ico':
            return True
        
        return False
