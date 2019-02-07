__author__ = 'tinglev@kth.se'

import os
import sys
import logging
import re
from modules.pipelines.docker_deploy_pipeline import DockerDeployPipeline
from modules.pipelines.npm_pipeline import NpmPipeline
from modules.util.environment import Environment
from modules.util.file_util import FileUtil
from modules.util.process import Process
import modules.util.log as log

def select_and_run_pipeline():
    logger = logging.getLogger(__name__)
    docker_conf = FileUtil.get_absolue_path('/docker.conf')
    has_docker_conf = os.path.isfile(docker_conf)
    npm_conf = FileUtil.get_absolue_path('/npm.conf')
    has_npm_conf = os.path.isfile(npm_conf)
    if has_docker_conf:
        pipeline = DockerDeployPipeline()
        pipeline.run_pipeline()
        return
    if has_npm_conf:
        pipeline = NpmPipeline()
        pipeline.run_pipeline()
        return
    else:
        logger.error('No suitable configuration file found for project')

def verify_npm_cli_version():
    logger = logging.getLogger(__name__)
    result = Process.run_with_output('npm -v').replace("\n", "")
    pattern = r'6+\.[4-9]+\.[0-9]+'
    match = re.match(pattern, result)
    if not match:
        logger.fatal('npm is not installed with the correct version.'
                     'Installed version is "%s" and required is "%s"', result, pattern)
        sys.exit(1)

def main():
    log.init_logging()
    evo_dir = Environment.get_evolene_directory()
    if not evo_dir:
        logging.getLogger(__name__).fatal('Missing EVOLENE_DIRECTORY environment')
        sys.exit(1)
    os.chdir(evo_dir)
    #verify_npm_cli_version()
    select_and_run_pipeline()

if __name__ == '__main__':
    main()
