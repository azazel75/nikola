# -*- coding: utf-8 -*-

# Copyright © 2012-2014 Roberto Alsina and others.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import io
import os

from nikola.plugin_categories import Task
from nikola import utils


class Redirect(Task):
    """Generate redirections"""

    name = "redirect"

    def gen_tasks(self):
        """Generate redirections tasks."""

        kw = {
            'redirections': self.site.config['REDIRECTIONS'],
            'output_folder': self.site.config['OUTPUT_FOLDER'],
        }

        yield self.group_task()
        if kw['redirections']:
            for src, dst in kw["redirections"]:
                src_path = os.path.join(kw["output_folder"], src)
                yield {
                    'basename': self.name,
                    'name': src_path,
                    'targets': [src_path],
                    'actions': [(create_redirect, (src_path, dst))],
                    'clean': True,
                    'uptodate': [utils.config_changed(kw)],
                }


def create_redirect(src, dst):
    utils.makedirs(os.path.dirname(src))
    with io.open(src, "w+", encoding="utf8") as fd:
        fd.write('<!DOCTYPE html><head><title>Redirecting...</title>'
                 '<meta name="robots" content="noindex">'
                 '<meta http-equiv="refresh" content="0; '
                 'url={0}"></head><body><p>Page moved <a href="{0}">here</a></p></body>'.format(dst))
