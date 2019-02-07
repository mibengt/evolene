__author__ = 'tinglev@kth.se'

from modules.util.data import Data
from modules.util.process import Process

def nvm_exec(data, cmd):
    conf_version = data[Data.NPM_CONF_NODE_VERSION]
    return Process.run_with_output(f'nvm exec --silent {conf_version} {cmd}')
