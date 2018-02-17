# -*- coding: utf-8 -*-

#
#  Copyright 2014, Jérôme Colin, Jérôme Kerdreux, Philippe Tanguy,
#  Telecom Bretagne.
#
#  This file is part of xAAL.
#
#  xAAL is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  xAAL is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with xAAL. If not, see <http://www.gnu.org/licenses/>.
#

import os
import uuid
import re

import pysodium

import logging
import logging.config

import sys
from configobj import ConfigObj

from . import config

XAAL_ADDR_PATTERN = '^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'
XAAL_DEVTYPE_PATTERN = '^[a-zA-Z][a-zA-Z0-9_-]*.[a-zA-Z][a-zA-Z0-9_-]*$'

def get_cfg_filename(name, cfg_dir=config.conf_dir):
    filename = '%s.ini' % name
    if not os.path.isdir(cfg_dir):
        print("Your configuration directory doesn't exist: [%s]" % cfg_dir)
    return os.path.join(cfg_dir, filename)

        
def load_cfg_file(filename):
    """ load .ini file and return it as dict"""
    if os.path.isfile(filename):
        return ConfigObj(filename,indent_type='  ')
    return None


def load_cfg(app_name):
    filename = get_cfg_filename(app_name)
    return load_cfg_file(filename)


def load_cfg_or_die(app_name):
    cfg = load_cfg(app_name)
    if not cfg:
        print("Unable to load config file %s" % get_cfg_filename(app_name))
        sys.exit(-1)
    return cfg

"""
def get_cfg_addr(app_name):
    cfg_file = get_cfg_file(app_name)
    cfg = load_cfg_file(cfg_file)

    if cfg is None:
        cfg = new_cfg(cfg_file, app_name)

    addr = cfg.get(app_name, 'xaaladdr')
    return addr
"""


def new_cfg(filename, app_name):
    cfg = ConfigParser()
    cfg.add_section(app_name)
    cfg.set(app_name, 'xaaladdr', get_random_uuid())
    f = open(filename, 'w')
    cfg.write(f)
    return cfg


def get_random_uuid():
    return str(uuid.uuid1())


def is_valid_addr(val):
    if re.match(XAAL_ADDR_PATTERN,val):
        return True
    return False


def is_valid_devtype(val):
    if re.match(XAAL_DEVTYPE_PATTERN,val):
        return True
    return False


def get_logger(name, level, filename=None):
    """ It creates logger if doesn't exist.
    - Default handler is in the console with DEBUG level.
    - A second handler (Rotating file handler) is created if a
      filename is specified with INFO level
    """
    logger = logging.getLogger(name)

    # define handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.root.addHandler(console_handler)

    if filename:
        file_handler = logging.handlers.RotatingFileHandler(filename, 'a', 10000, 1, 'utf8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.root.addHandler(file_handler)

    # Level manage by the root logger
    logger.root.setLevel(level)

    return logger


def pass2key(passphrase):
    """Generate key from passphrase using libsodium
    crypto_pwhash_scryptsalsa208sha256 func
    salt: buffer of zeros
    opslimit: crypto_pwhash_scryptsalsa208sha256_OPSLIMIT_INTERACTIVE
    memlimit: crypto_pwhash_scryptsalsa208sha256_MEMLIMIT_INTERACTIVE
    """
    buf = passphrase.encode('utf-8')
    KEY_BYTES = pysodium.crypto_pwhash_scryptsalsa208sha256_SALTBYTES #32 
    # this should be:
    # salt = bytes(KEY_BYTES)
    # but due to bytes() stupid stuff in py2 we need this awfull stuff
    salt = ('\00' * KEY_BYTES).encode('utf-8')
    opslimit = pysodium.crypto_pwhash_scryptsalsa208sha256_OPSLIMIT_INTERACTIVE
    memlimit = pysodium.crypto_pwhash_scryptsalsa208sha256_MEMLIMIT_INTERACTIVE
    key = pysodium.crypto_pwhash_scryptsalsa208sha256(KEY_BYTES, buf, salt, opslimit, memlimit)
    return key


def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance
