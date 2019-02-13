__author__ = 'tinglev@kth.se'

import os
import sys
import logging
import re
from modules.pipelines.docker_deploy_pipeline import DockerDeployPipeline
from modules.pipelines.npm_pipeline import NpmPipeline
from modules.util import environment
from modules.util import file_util
from modules.util import process
import modules.util.log as log

def select_and_run_pipeline():
    logger = logging.getLogger(__name__)
    docker_conf = file_util.get_absolue_path('/docker.conf')
    has_docker_conf = os.path.isfile(docker_conf)
    npm_conf = file_util.get_absolue_path('/npm.conf')
    has_npm_conf = os.path.isfile(npm_conf)
    if has_docker_conf:
        pipeline = DockerDeployPipeline()
        pipeline.run_pipeline()
        return
    if has_npm_conf:
        pipeline = NpmPipeline()
        pipeline.run_pipeline()
        return
    logger.error('No suitable configuration file found for project')
    sys.exit(1)

def main():
    log.init_logging()
    evo_dir = environment.get_evolene_directory()
    if not evo_dir:
        logging.getLogger(__name__).fatal('Missing EVOLENE_DIRECTORY environment')
        sys.exit(1)
    os.chdir(evo_dir)
    select_and_run_pipeline()

if __name__ == '__main__':
    main()
