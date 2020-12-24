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
        function_trigger_url = os.getenv("FUNCTION_TRIGGER_URL")
        match_pattern = "(https?://[^/]*)/[^/]*/proxy/([^/]*)/([^/]*)"
        endpoint, service_name, function_name = re.match(match_pattern, function_trigger_url).groups()

        client = fc2.Client(
            endpoint=endpoint,
            accessKeyID=os.getenv("ACCESS_KEY_ID"),
            accessKeySecret=os.getenv("ACCESS_KEY_SECRET"),
            Timeout=300,
        )
        client.update_function(service_name, function_name, codeDir="dist")


setup(cmdclass={"deploy": DeployCommand})
