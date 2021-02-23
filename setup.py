#!/bin/env python3
import distutils.cmd
import os
import re

import fc2
from setuptools import setup


class DeployCommand(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self) -> None:
        function_compute_arn = os.getenv("FUNCTION_COMPUTE_ARN")
        assert function_compute_arn
        match_pattern = r"^acs:fc:([^:]*):(\d+):services/([^.]*)\..*/functions/(.*)$"
        service_site, account_id, service_name, function_name = re.match(match_pattern, function_compute_arn).groups()

        client = fc2.Client(
            endpoint=f"http://{account_id}.{service_site}.fc.aliyuncs.com",
            accessKeyID=os.getenv("ACCESS_KEY_ID"),
            accessKeySecret=os.getenv("SECRET_ACCESS_KEY"),
            Timeout=300,
        )
        client.update_function(service_name, function_name, codeDir="dist")


setup(cmdclass={"deploy": DeployCommand})
