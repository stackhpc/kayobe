# Copyright (c) 2024 StackHPC Ltd.
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

import io
import unittest
from unittest import mock

from kayobe.stats import Stats


class TestCase(unittest.TestCase):

    def test_defaults(self):
        s = Stats()
        self.assertEqual(s.num_failures, 0)
        self.assertEqual(s.num_unreachable, 0)
        self.assertEqual(s.failures, [])
        self.assertEqual(s.unreachable, [])
        self.assertFalse(s.no_hosts_remaining)

    @mock.patch("kayobe.stats.open")
    def test_from_json(self, mock_open):
        json_file = io.StringIO("""{
            "num_failures": 1,
            "num_unreachable": 2,
            "failures": ["foo"],
            "unreachable": ["bar", "baz"],
            "no_hosts_remaining": true
        }""")
        mock_open.return_value.__enter__.return_value = json_file
        s = Stats.from_json("/path/to/json")
        mock_open.assert_called_once_with("/path/to/json")
        self.assertEqual(s.num_failures, 1)
        self.assertEqual(s.num_unreachable, 2)
        self.assertEqual(s.failures, ["foo"])
        self.assertEqual(s.unreachable, ["bar", "baz"])
        self.assertTrue(s.no_hosts_remaining)

    def test_completed_without_failures(self):
        s = Stats()
        self.assertTrue(s.completed_without_failures())

        s = Stats(num_unreachable=42)
        self.assertTrue(s.completed_without_failures())

        s = Stats(num_unreachable=42, no_hosts_remaining=True)
        self.assertFalse(s.completed_without_failures())

        s = Stats(num_failures=42)
        self.assertFalse(s.completed_without_failures())

        s = Stats(num_failures=42, no_hosts_remaining=True)
        self.assertFalse(s.completed_without_failures())
