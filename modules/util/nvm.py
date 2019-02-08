__author__ = 'tinglev@kth.se'

from modules.util.data import Data
from modules.util.process import Process
from modules.util.environment import Environment

def exec_npm_command(data, command):
    conf_version = data[Data.NPM_CONF_NODE_VERSION]
    project_path = Environment.get_project_root()
    return Process.run_with_output(
        f'. /var/lib/jenkins/.nvm/nvm.sh && '
        f'nvm exec --silent {conf_version} '
        f'npm --prefix {project_path} {command}'
    ).strip()

def exec_nvm_command(command):
    return Process.run_with_output(
        f'. /var/lib/jenkins/.nvm/nvm.sh && nvm {command}'
    ).strip()
