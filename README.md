# Evolene - Build process as code.

**Features:**
* Verifies **docker.conf**
* Verifies **Dockerfile**
* Writes build information to a js-module file (i.e: /config/version.js)
* Repo security scanning for passwords and secrets
* Docker build
* SemVer versioning of Docker images
* Push to Docker Registry
* Slack integration for build information
* Audit of FROM images
* Contarinerized integration testing by running **docker-compose-integration-tests.yml**
* Contarinerized unit testing by running **docker-compose-unit-tests.yml**

## How to use on Jenkins
Do use Evolene on Jenkins simply [add a build step](https://build.sys.kth.se/view/team-pipeline/job/kth-azure-app/configure) that executes run.sh. Evolene uses Convention Over Configuration. That means that Evolene is configure by following standard naming convensions rather then per project configuration.

![KTH on Azure](https://gita.sys.kth.se/Infosys/evolene/blob/master/images/jenkins.png)

Default configuration
```bash
SLACK_CHANNELS='#team-studadm-build' BUILD_INFORMATION_OUTPUT_FILE='/config/version.js' $EVOLENE_DIRECTORY/run.sh
```

Latest feature:
```bash
SLACK_CHANNELS='#team-studadm-build,#pipeline-logs' DEBUG=True EXPERIMENTAL=True $EVOLENE_DIRECTORY/run.sh
```
# Security scaning
By default files in your repo will be scanned for strings that looks like passwords or tokens. We use [RepoSupervisor](https://github.com/auth0/repo-supervisor/) for this.

When your project is buildt a warning will be sent to SLACK_CHANNELS with the files that contain suspisious files. If a file gives you a false possitive, you can create a file in the root of your repository and name it `.scanignore`. In the .scanignore file you can add catalogs or files that the security scan should ignore.

### .scanignore formatting
```bash
# Catalogs starting with, or specific files.
/node_modules/
/imported-data/personnumer.txt
```

# Build information to file

### Module
If BUILD_INFORMATION_OUTPUT_FILE ends with `.js` a module will be writen to the specified file.

```javascript
module.exports = {
  "jenkinsBuildDate": "2018-10-31 12:49:14",
  "dockerVersion": "2.3.40_f2486d7",
  "jenkinsBuild": "40",
  "dockerName": "tamarack",
  "dockerImage": "kthregistryv2.sys.kth.se/tamarack:2.3.40_f2486d7",
  "gitCommit": "f2486d79abf3af26225aa1dbde0fddfcd702c7e6",
  "gitBranch": "origin/master"
}
```

If BUILD_INFORMATION_OUTPUT_FILE ends with `.json` a module will be writen to the specified file.

### JSON
```json
{
  "jenkinsBuildDate": "2018-10-31 12:49:14",
  "dockerVersion": "2.3.40_f2486d7",
  "jenkinsBuild": "40",
  "dockerName": "tamarack",
  "dockerImage": "kthregistryv2.sys.kth.se/tamarack:2.3.40_f2486d7",
  "gitCommit": "f2486d79abf3af26225aa1dbde0fddfcd702c7e6",
  "gitBranch": "origin/master"
}
```

## All environment variables for configuration:

```
IMAGE_NAME                    - The name of the image to build (ex: 'kth-azure-app')
PROJECT_ROOT                  - The path to the root of the project to build (ex: '/Users/projects/kth-azure-app')
GIT_COMMIT                    - The commit hash of the push that triggered the build (usually set by Jenkins)
BUILD_NUMBER                  - The number of the current build (usually set by Jenkins)
SLACK_WEB_HOOK                - The Slack webhook endpoint to use
SLACK_CHANNELS                - Comma separated list of channels to post messages to (ex: '#pipeline-logs,#zermatt')
REGISTRY_HOST                 - The host (without protocol) of the Docker registry to use (ex: 'kthregistryv2.sys.kth.se')
REGISTRY_USER                 - Registry user
REGISTRY_PASSWORD             - Registry password
PUSH_PUBLIC                   - Push the image to hub.docker.com/r/kthse
SKIP_DRY_RUN                  - Skip the step where the new image is tested by running 'docker run image_id'
BUILD_INFORMATION_OUTPUT_FILE - Print build info  file 
EVOLENE_DIRECTORY             - The working directory of evolene (used on jenkins to work properly)
EXPERIMENTAL                  - Feature toogle for latest features
```

# How to develop and run Evolene on your local machine

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

Changes to this project are automatically sent to https://build.sys.kth.se

