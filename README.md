# Evolene

**:whale: Build process as code** Evolene runs a sequence of steps that build, test and in the end does a `docker push` on a  SemVer tagged Docker image like `tamarack:2.3.40_f2486d7`. All steps including unit and integration
tests are run inside Docker containers, eliminating most Jenkins plugins.

Evolene uses Convention Over Configuration. That means that Evolene is configure by following standard naming convensions rather then per project configuration.

## :exclamation: User Requirements

For our app to build using Evolene you need to have two files in your projects root directory.
A `Dockerfile`, and a Evolene meta-data file called `docker.conf`.

```bash

# 
# Name to use when tagging the image
# E.g: kth-nodejs -> "kthse/kth-nodejs:9.11.0_c25cca9"
#
IMAGE_NAME=tamarack

#
# Evolene tags docker images using https://semver.org/ notation, major.minor.path.
# 
# IMAGE_VERSION=major.minor
# The Patch is normally added by Evolene at build time using $BUILD_NUMBER
#

IMAGE_VERSION=2.3

# 
# You can override using $BUILD_NUMBER as patch number for SemVer by 
# explicitly adding it aswell.
#
# PATCH_VERSION=0

```

That is it, you will get notified by Evolene about all other things in console log and to the `SLACK_CHANNELS` when you need to know them.

Happy Coding!


## Evolene Features

* Verifies /docker.conf
* Verifies /Dockerfile
* Writes build information to file
* Repo security scanning for passwords and secrets
* Docker build
* SemVer versioning of Docker images
* Push to Docker Registry
* Slack integration for build information
* Audit of FROM images
* Contarinerized integration testing by running **docker-compose-integration-tests.yml**
* Contarinerized unit testing by running **docker-compose-unit-tests.yml**


# Build SemVer Docker Image 

## Overide the Name
Override the IMAGE_NAME in docker.conf for the image to build.

```bash
IMAGE_NAME='other-name'  $EVOLENE_DIRECTORY/run.sh
```

## Project Root

Build your project from an other directory.
If set the  $WORKSPACE set by Jenkins will be ignored.

```bash
PROJECT_ROOT='/other/jenkis/workspace/other-repo/'  $EVOLENE_DIRECTORY/run.sh
```

## Override Git Commit
Reuse a commit hash of the push that triggered the build.
If set the  $GIT_COMMIT set by Jenkins will be ignored.

```bash
GIT_COMMIT='abcdefhijkl1234456'  $EVOLENE_DIRECTORY/run.sh
```

## Specify SemVer path versoin
The patch version in the SemVer tag is the Jenkins $BUILD_NUMBER.
If set the $BUILD_NUMBER set by Jenkins will be ignored, and patch version
will always be tag tamarack:2.3.`40`. 

```bash
BUILD_NUMBER='40'  $EVOLENE_DIRECTORY/run.sh
```


# Build information to file

### Module
If BUILD_INFORMATION_OUTPUT_FILE ends with `.js` a module will be writen to the specified file.

```bash
BUILD_INFORMATION_OUTPUT_FILE='/info.js`'
```

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

```bash
BUILD_INFORMATION_OUTPUT_FILE='/config/info.json`'
```

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

# Slack Integration

## Slack web hook 

The Slack webhook endpoint where the `SLACK_CHANNELS` can be found.

```bash
SLACK_WEB_HOOK='https://hooks.slack.com/services/1234asdfasd/' $EVOLENE_DIRECTORY/run.sh
```

## Slack channels to post build information to

Comma separated list of channels to post messages to. Messages are build inforation,
failures an push information.

```bash
SLACK_CHANNELS='#pipeline-logs,#devops' $EVOLENE_DIRECTORY/run.sh
```

# Security scaning

By default files in your repo will be scanned for strings that looks like passwords or tokens. We use [RepoSupervisor](https://github.com/auth0/repo-supervisor/) for this.

When your project is buildt a warning will be sent to SLACK_CHANNELS with the files that contain suspisious files. If a file gives you a false possitive, you can create a file in the root of your repository and name it `.scanignore`. In the .scanignore file you can add catalogs or files that the security scan should ignore.

## .scanignore formatting

```bash
# Catalogs starting with, or specific files.
/node_modules/
/imported-data/personnumer.txt
```

# Docker Registries

## Private Docker Registry

Unless `PUSH_PUBLIC` is set to `true`, this registry will be used.
The host without protocol.

```bash
REGISTRY_HOST='private-docker-registry.mycompany.com' $EVOLENE_DIRECTORY/run.sh
```

## Private Docker Registry User
The private `REGISTRY_HOST`:s  BASIC_AUTH user who has the rights to read and push to the private registry.

```bash
REGISTRY_USER='myuser' $EVOLENE_DIRECTORY/run.sh
```

## Private Docker Registry User

The private `REGISTRY_HOST`:s  BASIC_AUTH users password.

```bash
REGISTRY_PASSWORD='qwerty123' $EVOLENE_DIRECTORY/run.sh
```

### Public repository

Set to `true` When you whant to push your image to `hub.docker.com/r/kthse`. This will push two tags,
the ususual SemVer with commit `tamarack:2.3.40_f2486d7`, but also and also a short tag with only SemVer `tamarack:2.3.40`. This is done to enable reuse of tags.

```bash
PUSH_PUBLIC='True' # True or False
```

# Misc 

## Skip dry run step

Normally Evolene does a `docker run IMAGE_ID` to see that the image is build correctly and can start.
Some images does not support this (os-images) and therefor exits causing the pipeline to exit. 

```bash
SKIP_DRY_RUN='True' # True or False
```

## Feature flag for building

Sometimes we add new features that are sort of in beta. If you would like to try these out allow
exprimental.

```bash
EXPERIMENTAL='True' # True or False
```

## Evolene versioning

Path to the directory of a Evolene dist version.
Used in Jenkin builds for shorter path when envoking the Evolene itself `$EVOLENE_DIRECTORY/run.sh`.
Also gives you a way of specifing what version of Evolene that is used.

```bash
EVOLENE_DIRECTORY='`/var/lib/jenkins/workspace/evolene/dist/evolene-1.6`'
```

# How to setup Evolene on Jenkins

## 1. Set up a build task that builds Evolene
Add an *Execute shell* Step and run.
```bash
/create_dist.sh
LATEST_DIST=$(ls -tp dist | grep -v / | head -1)
tar xvf dist/$LATEST_DIST -C dist
rm -rf dist/latest
mkdir dist/latest
tar xvf dist/$LATEST_DIST -C dist/latest --strip 1
chmod -R 700 dist/latest
```
This will create a executable Evolene dist in `/var/lib/jenkins/workspace/evolene/dist/evolene-1.6`.

## 2. Add default envs for builds on the Jenkins server.

We recommend that the following envs are available to each Jenkins job. The can be overridden by
env arguments per build as shown above.

EVOLENE_DIRECTORY
EVOLENE_SLACK_WEB_HOOK
REGISTRY_HOST
REGISTRY_PASSWORD
REGISTRY_USER

# 3. Test your setup
Test your setup by adding a Docker application that follows Evolene and run *Execute shell*
`$EVOLENE_DIRECTORY/run.sh`


![Example](https://gita.sys.kth.se/Infosys/evolene/blob/master/images/jenkins.png)

# How to develop and run Evolene on your local machine

## Run the code locally

```bash
python run.py docker run-pipeline
```

## Create a distribution

Note! The version of the dist is defined in `setup.py`

```bash
./create_dist.sh`
```

## Run unit tests

```bash
./run_tests.sh
```
