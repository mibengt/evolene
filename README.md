# Evolene
## Pipeline functionality for building, testing and pushing Docker images.

Jenkins build as code.

Features:
* Repo security scanning for passwords and secrets
* Docker build
* SemVer versioning of Docker images
* Push to Docker Registry
* Slack integration for build information

## How to use

Default configuration
```bash
SLACK_CHANNELS="#team-studadm" $EVOLENE_DIRECTORY/run.sh
```

Latest feature:
```bash
SLACK_CHANNELS="#team-pipeline-build,#pipeline-logs" DEBUG=True EXPERIMENTAL=True $EVOLENE_DIRECTORY/run.sh
```


# For developers

To run: 
```bash
python run.py docker run-pipeline
```

To create dist:
```bash
./create_dist.sh
```
The version of the dist is defined in `setup.py`

To run tests:
```bash
./run_tests.sh
```

All environment variables for configuration:

```
IMAGE_NAME          - The name of the image to build (ex: 'kth-azure-app')
PROJECT_ROOT        - The path to the root of the project to build (ex: '/Users/projects/kth-azure-app')
GIT_COMMIT          - The commit hash of the push that triggered the build (usually set by Jenkins)
BUILD_NUMBER        - The number of the current build (usually set by Jenkins)
SLACK_WEB_HOOK      - The Slack webhook endpoint to use
SLACK_CHANNELS      - Comma separated list of channels to post messages to (ex: '#pipeline-logs,#zermatt')
REGISTRY_HOST       - The host (without protocol) of the Docker registry to use (ex: 'kthregistryv2.sys.kth.se')
REGISTRY_USER       - Registry user
REGISTRY_PASSWORD   - Registry password
EVOLENE_DIRECTORY   - The working directory of evolene (used on jenkins to work properly)
EXPERIMENTAL        - Feature toogle for latest features
```

Changes to this project are automatically sent to https://build.sys.kth.se

