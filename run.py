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
import fire
from modules.pipelines.docker_deploy_pipeline import DockerDeployPipeline
from modules.util.environment import Environment
import modules.util.log as log

if __name__ == '__main__':
    log.init_logging()
    evo_dir = Environment.get_evolene_directory()
    if not evo_dir:
        logging.getLogger(__name__).fatal('Missing EVOLENE_DIRECTORY environment')
        sys.exit(1)
    os.chdir(evo_dir)
    fire.Fire({
        'docker': DockerDeployPipeline
        })
