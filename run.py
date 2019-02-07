# Build:
# ------
# Read docker.conf
#   - Exists
#   - Content
# Calculate final image version
#   - Env req: Buildnr
#   - Env req: Hashcommit
# Check Dockerfile
# Build to local registry
#   - Build
#   - Verify
# Dry run image
# Run tests on image
# Tag image
# Get size of image
# Push image to registryv2
#   - Env req: registry url and login
#   - Only push certain branches
# Send info to Slack
#   - Env req: Slack hook

# RMI:
# ----
# Remove all local images

import os
import sys
import logging
from modules.pipelines.docker_deploy_pipeline import DockerDeployPipeline
from modules.pipelines.npm_pipeline import NpmPipeline
from modules.util.environment import Environment
from modules.util.file_util import FileUtil
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
    elif has_npm_conf:
        pipeline = NpmPipeline()
        pipeline.run_pipeline()
    else:
        logger.error('No suitable configuration file found for project')

def main():
    log.init_logging()
    evo_dir = Environment.get_evolene_directory()
    if not evo_dir:
        logging.getLogger(__name__).fatal('Missing EVOLENE_DIRECTORY environment')
        sys.exit(1)
    os.chdir(evo_dir)
    select_and_run_pipeline()

if __name__ == '__main__':
    main()
