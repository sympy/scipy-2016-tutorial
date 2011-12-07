#!/usr/bin/env python

# This is a development server allowing to serve Sphinx documentation from
# localhost (by default on port 8000). Use this server if you want to test
# Sphinx extensions that require Ajax to work (Ajax usually doesn't work
# when using file:// protocol).

import os
import sys
import logging
import argparse
import traceback

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

class WebPageHandler(tornado.web.RequestHandler):
    """Render a web page from a file. """

    def get(self, file):
        try:
            with open(os.path.join('build/html', file), 'r') as f:
                self.write(f.read())
        except IOError:
            raise tornado.web.HTTPError(404)

def setup_logging():
    """Configure :mod:`logging` to log to the terminal. """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    tornado.options.enable_pretty_logging()

def runserver(port=8000):
    setup_logging()

    application = tornado.web.Application([
        (r"/$", tornado.web.RedirectHandler, {"url": "/index.html"}),
        (r"/mathjax/(.*)", tornado.web.StaticFileHandler, {"path": "mathjax"}),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "build/html"}),
    ])

    def on_start():
        logging.info("Started server at localhost:%s (pid=%s)" % (port, os.getpid()))

    io = tornado.ioloop.IOLoop.instance()
    io.add_callback(on_start)

    server = tornado.httpserver.HTTPServer(application)
    server.listen(port)

    try:
        io.start()
    except KeyboardInterrupt:
        print # SIGINT prints '^C' so lets make logs more readable
    except SystemExit:
        pass

    logging.info("Stopped server at localhost:%s (pid=%s)" % (port, os.getpid()))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8000)
    args = parser.parse_args()
    runserver(args.port)

if __name__ == '__main__':
    main()
