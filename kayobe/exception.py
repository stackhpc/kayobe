# Copyright (c) 2018 StackHPC Ltd.
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

from kayobe import stats


class KayobeException(Exception):
    """Base class for kayobe exceptions."""


class Error(KayobeException):
    """Generic user error."""


class ContinueOnError(KayobeException):
    """Continue after some hosts are failed or unreachable."""

    def __init__(self, cmd: str, exit_code: int, stats: stats.Stats):
        super(ContinueOnError, self).__init__()
        self.cmd = cmd
        self.exit_code = exit_code
        self.stats = stats
