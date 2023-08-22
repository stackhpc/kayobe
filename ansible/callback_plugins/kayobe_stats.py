# Copyright (c) 2023 StackHPC Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: kayobe_stats
    type: notification
    short_description: Save Ansible statistics to a JSON file
    version_added: "2.0"
    options:
        kayobe_stats_path:
            description: path of the JSON statistics file.
            ini:
                - section: callback_kayobe_stats
                  key: kayobe_stats_path
            env:
                - name: ANSIBLE_KAYOBE_STATS_PATH
            default: "~/.ansible/kayobe_stats/kayobe_stats.json"
            type: path
    description:
        - This produces a JSON dump of statistics in a file.
'''

import json
import os

import kayobe.stats

from ansible.module_utils._text import to_bytes, to_text
from ansible.plugins.callback import CallbackBase
from ansible.utils.path import makedirs_safe


class CallbackModule(CallbackBase):
    '''
    This callback puts statistics into a file.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'kayobe_stats'
    CALLBACK_NEEDS_ENABLED = False

    def set_options(self, task_keys=None, var_options=None, direct=None):
        '''Override to set self.path '''

        super(CallbackModule, self).set_options(task_keys=task_keys,
                                                var_options=var_options,
                                                direct=direct)

        self.path = self.get_option('kayobe_stats_path')
        self.no_hosts_remaining = False

    def write_stats(self, buf):
        '''Write statistics to file.'''

        buf = to_bytes(buf)
        directory = os.path.dirname(self.path)
        try:
            makedirs_safe(directory)
        except (OSError, IOError) as e:
            self._display.error(u"Unable to access or create the configured "
                                 "directory (%s): %s" %
                                (to_text(directory), to_text(e)))
            raise

        try:
            path = to_bytes(self.path)
            with open(path, 'wb+') as fd:
                fd.write(buf)
        except (OSError, IOError) as e:
            self._display.error(u"Unable to write to %s's file: %s" %
                                (hostname, to_text(e)))
            raise

    def v2_playbook_on_no_hosts_remaining(self):
        # Catch the case when no hosts remain. This means that a play has ended
        # early.
        self.no_hosts_remaining = True

    def v2_playbook_on_stats(self, ansible_stats):
        hosts = sorted(ansible_stats.processed.keys())
        stats = kayobe.stats.Stats(no_hosts_remaining=self.no_hosts_remaining)
        for h in hosts:
            t = ansible_stats.summarize(h)
            if t['failures']:
                stats.num_failures += 1
                stats.failures.append(h)
            if t['unreachable']:
                stats.num_unreachable += 1
                stats.unreachable.append(h)
        self.write_stats(json.dumps(stats))
