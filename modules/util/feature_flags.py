__author__ = 'tinglev@kth.se'

import logging
from modules.util import environment

LOG = logging.getLogger(__name__)

FEATURE_FLAG_ACR = 'FEATURE_ACR'

def use_feature_flag_acr():
    return use(FEATURE_FLAG_ACR)

def use(flag):
    value = environment.is_true(environment.get_env_with_default_value(flag, False))
    LOG.debug('Feature flag %s is "%s".', flag, value)
    return value
