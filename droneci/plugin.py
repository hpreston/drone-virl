# -*- coding: utf-8 -*-
"""
Drone CI Plugin Object that provides access to relevant
build state information as object dictionaries.  
"""

import os

class Plugin(object):
    def __init__(self, secrets = []):

        self.plugin = {}
        self.ci = {}
        self.drone = {}
        self.secrets = {}

        for envvar in os.environ.keys():
            if "CI_" in envvar:
                self.ci[envvar[3:]] = os.environ[envvar]
            elif "DRONE_" in envvar:
                self.drone[envvar[6:]] = os.environ[envvar]
            elif "PLUGIN_" in envvar:
                self.plugin[envvar[7:]] = os.environ[envvar]
            elif envvar in secrets:
                self.secrets[envvar] = os.environ[envvar]

        if "DEBUG" not in self.plugin.keys():
            self.plugin["DEBUG"] = False
