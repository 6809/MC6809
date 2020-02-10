#!/usr/bin/env python

"""
    DragonPy - CPU control http server
    ==================================

    TODO: Use bottle!

    :copyleft: 2013-2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.

    Based on:
        * ApplyPy by James Tauber (MIT license)
        * XRoar emulator by Ciaran Anscomb (GPL license)
    more info, see README
"""


import json
import logging
import re
import select
import threading
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer


log = logging.getLogger("MC6809")


class ControlHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server, cpu):
        log.error("ControlHandler %s %s %s", request, client_address, server)
        self.cpu = cpu

        self.get_urls = {
            r"/disassemble/(\s+)/$": self.get_disassemble,
            r"/memory/(\s+)(-(\s+))?/$": self.get_memory,
            r"/memory/(\s+)(-(\s+))?/raw/$": self.get_memory_raw,
            r"/status/$": self.get_status,
            r"/$": self.get_index,
        }

        self.post_urls = {
            r"/memory/(\s+)(-(\s+))?/$": self.post_memory,
            r"/memory/(\s+)(-(\s+))?/raw/$": self.post_memory_raw,
            r"/quit/$": self.post_quit,
            r"/reset/$": self.post_reset,
            r"/debug/$": self.post_debug,
        }

        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def log_message(self, format, *args):
        msg = f"{self.client_address[0]} - - [{self.log_date_time_string()}] {format % args}\n"
        log.critical(msg)

    def dispatch(self, urls):
        for r, f in list(urls.items()):
            m = re.match(r, self.path)
            if m is not None:
                log.critical("call %s", f.__name__)
                try:
                    f(m)
                except Exception as err:
                    txt = traceback.format_exc()
                    self.response_500(f"Error call {f.__name__!r}: {err}", txt)
                return
        else:
            self.response_404(f"url {self.path!r} doesn't match any urls")

    def response(self, s, status_code=200):
        log.critical("send %s response", status_code)
        self.send_response(status_code)
        self.send_header("Content-Length", str(len(s)))
        self.end_headers()
        self.wfile.write(s)

    def response_html(self, headline, text=""):
        html = (
            "<!DOCTYPE html><html><body>"
            "<h1>%s</h1>"
            "%s"
            "</body></html>"
        ) % (headline, text)
        self.response(html)

    def response_404(self, txt):
        log.error(txt)
        html = (
            "<!DOCTYPE html><html><body>"
            "<h1>DragonPy - 6809 CPU control server</h1>"
            "<h2>404 - Error:</h2>"
            "<p>%s</p>"
            "</body></html>"
        ) % txt
        self.response(html, status_code=404)

    def response_500(self, err, tb_txt):
        log.error(err, tb_txt)
        html = (
            "<!DOCTYPE html><html><body>"
            "<h1>DragonPy - 6809 CPU control server</h1>"
            "<h2>500 - Error:</h2>"
            "<p>%s</p>"
            "<pre>%s</pre>"
            "</body></html>"
        ) % (err, tb_txt)
        self.response(html, status_code=500)

    def do_GET(self):
        log.critical("do_GET(): %r", self.path)
        self.dispatch(self.get_urls)

    def do_POST(self):
        log.critical("do_POST(): %r", self.path)
        self.dispatch(self.post_urls)

    def get_index(self, m):
        self.response_html(
            headline="DragonPy - 6809 CPU control server",
            text=(
                "<p>Example urls:"
                "<ul>"
                '<li>CPU status:<a href="/status/">/status/</a></li>'
                '<li>6809 interrupt vectors memory dump:'
                '<a href="/memory/fff0-ffff/">/memory/fff0-ffff/</a></li>'
                '</ul>'
                '<form action="/quit/" method="post">'
                '<input type="submit" value="Quit CPU">'
                '</form>'
            ))

    def get_disassemble(self, m):
        addr = int(m.group(1))
        r = []
        n = 20
        while n > 0:
            dis, length = self.disassemble.disasm(addr)
            r.append(dis)
            addr += length
            n -= 1
        self.response(json.dumps(r))

    def get_memory_raw(self, m):
        addr = int(m.group(1))
        e = m.group(3)
        if e is not None:
            end = int(e)
        else:
            end = addr
        self.response("".join(chr(self.cpu.read_byte(x)) for x in range(addr, end + 1)))

    def get_memory(self, m):
        addr = int(m.group(1), 16)
        e = m.group(3)
        if e is not None:
            end = int(e, 16)
        else:
            end = addr
        self.response(json.dumps(list(map(self.cpu.read_byte, list(range(addr, end + 1))))))

    def get_status(self, m):
        data = {
            "cpu": self.cpu.get_info,
            "cc": self.cpu.get_cc_info(),
            "pc": self.cpu.program_counter.get(),
            "cycle_count": self.cpu.cycles,
        }
        log.critical("status dict: %s", repr(data))
        json_string = json.dumps(data)
        self.response(json_string)

    def post_memory(self, m):
        addr = int(m.group(1))
        e = m.group(3)
        if e is not None:
            end = int(e)
        else:
            end = addr
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        for i, a in enumerate(range(addr, end + 1)):
            self.cpu.write_byte(a, data[i])
        self.response("")

    def post_memory_raw(self, m):
        addr = int(m.group(1))
        e = m.group(3)
        if e is not None:
            end = int(e)
        else:
            end = addr
        data = self.rfile.read(int(self.headers["Content-Length"]))
        for i, a in enumerate(range(addr, end + 1)):
            self.cpu.write_byte(a, data[i])
        self.response("")

    def post_debug(self, m):
        handler = logging.StreamHandler()
        handler.level = 5
        log.handlers = (handler,)
        log.critical("Activate full debug logging in %s!", __file__)
        self.response("")

    def post_quit(self, m):
        log.critical("Quit CPU from controller server.")
        self.cpu.quit()
        self.response_html(headline="CPU running")

    def post_reset(self, m):
        self.cpu.reset()
        self.response_html(headline="CPU reset")


class ControlHandlerFactory:
    def __init__(self, cpu):
        self.cpu = cpu

    def __call__(self, request, client_address, server):
        return ControlHandler(request, client_address, server, self.cpu)


def control_server_thread(cpu, cfg, control_server):
    # FIXME: Refactor this!
    timeout = 1

    sockets = [control_server]
    rs, _, _ = select.select(sockets, [], [], timeout)
    for s in rs:
        if s is control_server:
            control_server._handle_request_noblock()
        else:
            pass

    if cpu.running:
        threading.Timer(interval=0.5,
                        function=control_server_thread,
                        args=(cpu, cfg, control_server)
                        ).start()
    else:
        log.critical("Quit control server thread, because CPU doesn't run.")


class CPUControlServerMixin:
    def __init__(self, *args, **kwargs):
        control_handler = ControlHandlerFactory(self)
        server_address = (self.cfg.CPU_CONTROL_ADDR, self.cfg.CPU_CONTROL_PORT)
        try:
            control_server = HTTPServer(server_address, control_handler)
        except BaseException:
            self.running = False
            raise
        url = "http://%s:%s" % server_address
        log.error("Start http control server on: %s", url)

        control_server_thread(self, self.cfg, control_server)
