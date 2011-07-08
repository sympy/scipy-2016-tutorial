"""Compile Tikz graphics automatically. """

import os, hashlib, pexpect

from sphinx.util.compat import Directive

class TikzDirective(Directive):

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {}

    def run(self):
        uri = self.arguments[0]

        with open(uri) as f:
            digest = hashlib.sha1(f.read()).hexdigest()

        path = os.path.dirname(uri)
        name = os.path.basename(uri)

        _uri = os.path.join(path, "." + name)

        if os.path.exists(_uri):
            with open(_uri) as f:
                _digest = f.read()

            if _digest == digest:
                return []

        _path = os.path.join(path, os.path.splitext(name)[0])

        pexpect.run("pdflatex -halt-on-error -output-directory=%s %s" % (path, uri))

        pexpect.run("perl /usr/bin/pdfcrop %s.pdf" % _path)
        pexpect.run("mv %s-crop.pdf %s.pdf" % (_path, _path))
        pexpect.run("convert %s.pdf %s.png" % (_path, _path))

        pexpect.run("rm %s.aux" % _path)
        pexpect.run("rm %s.log" % _path)

        with open(_uri, "w") as f:
            f.write(digest)

        return []

def setup(app):
    app.add_directive('tikz', TikzDirective)

