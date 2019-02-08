__author__ = 'tinglev@kth.se'

from modules.util.data import Data
from modules.util.process import Process
from modules.util.environment import Environment

NVM_DIR = '$HOME/.nvm/nvm.sh'

def get_nvm_source():
    return f'. {NVM_DIR}'

def get_nvm_exec_base(data):
    nvm_source = get_nvm_source()
    conf_version = data[Data.NPM_CONF_NODE_VERSION]
    return (
        f'{nvm_source} && '
        f'nvm exec --silent {conf_version}'
    )

def get_npm_base(data):
    nvm_base = get_nvm_exec_base(data)
    project_path = Environment.get_project_root()
    return (
        f'{nvm_base} npm --prefix {project_path}'
    )

def run_npm_script(data, script_name):
    npm_base = get_npm_base(data)
    return Process.run_with_output(
        f'{npm_base} run-script {script_name}'
    ).replace('\n', '').strip()

def exec_npm_command(data, command):
    npm_base = get_npm_base(data)
    return Process.run_with_output(
        f'{npm_base} {command}'
    ).replace('\n', '').strip()

def exec_nvm_command(command):
    nvm_source = get_nvm_source()
    return Process.run_with_output(
        f'{nvm_source} && nvm {command}'
    ).strip()
