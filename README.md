# Evolene
## Pipeline functionality for building, testing and pushing Docker images.

A Python rewrite of https://gita.sys.kth.se/Infosys/zermatt

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

Environment variables for configuration:

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
```

Changes to this project are automatically sent to https://build.sys.kth.se

