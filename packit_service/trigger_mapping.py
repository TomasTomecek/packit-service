# MIT License
#
# Copyright (c) 2018-2019 Red Hat, Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Dict

from deprecated import deprecated

from packit.config import JobConfigTriggerType, JobConfig, JobType
from packit_service.service.events import TheJobTriggerType

MAP_JOB_TRIGGER_TO_JOB_CONFIG_TRIGGER_TYPE: Dict[
    TheJobTriggerType, JobConfigTriggerType
] = {
    TheJobTriggerType.commit: JobConfigTriggerType.commit,
    TheJobTriggerType.release: JobConfigTriggerType.release,
    TheJobTriggerType.pull_request: JobConfigTriggerType.pull_request,
    TheJobTriggerType.push: JobConfigTriggerType.commit,
    TheJobTriggerType.pr_comment: JobConfigTriggerType.pull_request,
    TheJobTriggerType.copr_start: JobConfigTriggerType.pull_request,
    TheJobTriggerType.copr_end: JobConfigTriggerType.pull_request,
    TheJobTriggerType.testing_farm_results: JobConfigTriggerType.pull_request,
    TheJobTriggerType.issue_comment: JobConfigTriggerType.release,
}


@deprecated(
    reason="Should be avoided since it is hardcoded. "
    "We can use info from database instead for events without the real trigger "
    "(e.g. copr/koji/tests results)."
)
def is_trigger_matching_job_config(
    trigger: TheJobTriggerType, job_config: JobConfig
) -> bool:
    """
    Check that the event trigger matches the one from config.

    We can have multiple events for one config.
    e.g. Both pr_comment and pull_request are compatible
         with the pull_request config in the config
    """
    config_trigger = MAP_JOB_TRIGGER_TO_JOB_CONFIG_TRIGGER_TYPE.get(trigger)
    return bool(config_trigger and job_config.trigger == config_trigger)


def are_job_types_same(first: JobType, second: JobType) -> bool:
    """
    We need to treat `build` alias in a special way.
    """
    return first == second or {first, second} == {JobType.build, JobType.copr_build}
