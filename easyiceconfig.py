#
#  Copyright (C) 1997-2015 JDE Developers Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#  Authors :
#       Victor Arribas Raigadas <v.arribas.urjc@gmail.com>
#
__author__ = 'varribas'

import sys, os
import re
import Ice


ENV_PATH_NAME = "ICE_CONFIG_PATH"
JDEROBOT_PATHS = "/usr/local/share/jderobot/conf"


def findConfigFile(filename):
    paths = "."
    env_paths = os.getenv(ENV_PATH_NAME)
    if env_paths:
        paths = paths+":"+env_paths
    if JDEROBOT_PATHS:
        paths = paths+":"+JDEROBOT_PATHS

    for path in paths.split(":"):
        file_path = os.path.join(path, filename)
        if os.path.exists(file_path):
            return file_path

    return None


def loadIceConfig(filename, properties = Ice.createProperties()):
    filepath = findConfigFile(filename)
    if (filepath):
        properties.load(filepath)
    else:
        msg = "IceConfig file '%s' could not being found" % (filename)
        raise ValueError(msg)

    return properties


def initializeProperties(args, properties = Ice.createProperties()):
    properties.parseIceCommandLineOptions(args)
    iceconfigfiles = properties.getProperty("Ice.Config")
    if (iceconfigfiles):
        for iceconfig in iceconfigfiles.split(","):
            loadIceConfig(iceconfig, properties)

    properties.parseCommandLineOptions("", args)

    return properties


def initialize(args):
    id = Ice.InitializationData();
    id.properties = initializeProperties(args)
    ic = Ice.initialize(None, id)

    return ic


def createProperties(args):
    return initializeProperties(args)
