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
# Push image to registryv
#   - Env req: registry url and login
#   - Only push certain branches
# Send info to Slack
#   - Env req: Slack hook

# RMI:
# ----
# Remove all local images

import fire
from modules.pipelines.docker_deploy_pipeline import DockerDeployPipeline
import modules.util.log as log

if __name__ == '__main__':
    log.init_logging()
    fire.Fire({
        'docker': DockerDeployPipeline
        })
