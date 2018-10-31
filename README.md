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

# All environment variables for configuration:

### Overide the name
Override the IMAGE_NAME in docker.conf forthe image to build.

```bash
IMAGE_NAME='kth-azure-app'  $EVOLENE_DIRECTORY/run.sh
```

### Project root

Build your project from an other directory.

```bash
PROJECT_ROOT='/other/jenkis/workspace/app-name/'  $EVOLENE_DIRECTORY/run.sh
```

### Override gitcommit

Reuse a commit hash of the push that triggered the build (usually set by Jenkins)

```bash
GIT_COMMIT='abcdefhijkl1234456'  $EVOLENE_DIRECTORY/run.sh
```

### Ignore Jenins build number

The number of the current build (usually set by Jenkins)

```bash
BUILD_NUMBER='2'  $EVOLENE_DIRECTORY/run.sh
```

### Slack web hook 

The Slack webhook endpoint to use

```bash
SLACK_WEB_HOOK='https://api.slack.com/token1234/' $EVOLENE_DIRECTORY/run.sh
```

### Slack channels to post build information to

Comma separated list of channels to post messages to.

```bash
SLACK_CHANNELS='#pipeline-logs,#devops' $EVOLENE_DIRECTORY/run.sh
```

### Private Docker Registy.

Unless `PUSH_PUBLIC` is set to `true`, this registry will be used.
The host without protocol.

```bash
REGISTRY_HOST='registry.mycompany.com' $EVOLENE_DIRECTORY/run.sh
```

### Private Docker Registy User
The private REGISTRY_HOST:s  BASIC_AUTH user who has the rights to read and push to the private registry.

```bash
REGISTRY_USER='myuser' $EVOLENE_DIRECTORY/run.sh
```

### Private Docker Registy User

The private REGISTRY_HOST:s  BASIC_AUTH users password. 

```bash
REGISTRY_PASSWORD='qwerty123' $EVOLENE_DIRECTORY/run.sh
```

### Push the image to a public repository

Set to `true` When you whant to push your image to `hub.docker.com/r/kthse`. This will push two tags,
the ususual SemVer with commit `my-app:1.2.3_abcdefg`, but also and also a short tag with only SemVer `my-app:1.2.3`. This is done to enable reuse of tags.

```bash
PUSH_PUBLIC='True' # True or False
```

### Skip dry run step

Normally Evolene does a `docker run IMAGE_ID` to see that the image is build correctly and can start.
Some images does not support this (os-images) and therefor exits causing the pipeline to exit. 

```bash
SKIP_DRY_RUN='True' # True or False
```

### Feature flag for building

Sometimes we add new features that are sort of in beta. If you would like to try these out allow
exprimental.

```bash
EXPERIMENTAL='True' # True or False
```

### Feature flag for building

Path to the directory of a Evolene dist version.
Used in Jenkins for envoking the Evolene itself `$EVOLENE_DIRECTORY/run.sh`

```bash
EVOLENE_DIRECTORY='`/var/lib/jenkins/workspace/evolene/dist/evolene-1.6`'
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

