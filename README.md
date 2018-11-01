# Evolene

**:whale: Build process as code** Evolene runs a sequence of steps that build, test and in the end does a `docker push` on a  SemVer tagged Docker image like `tamarack:2.3.40_f2486d7`. All steps including unit and integration
tests are run inside Docker containers, eliminating most Jenkins plugins.

Evolene uses Convention Over Configuration. That means that Evolene is configure by following standard naming convensions rather then per project configuration.

![Example](https://gita.sys.kth.se/Infosys/evolene/blob/master/images/jenkins.png)

## :exclamation: Usage Requirements

For your app to build using Evolene you need to have two files in your projects root directory.
A `Dockerfile`, and a Evolene meta-data file called `docker.conf`.

The example bellow will on the *40th* build on Jenkins create `tamarack:2.3.40_f2486d7`. Where `f2486d7` is the Git Commit of that exact code built.

```bash
#
# Name to use when tagging the image
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
# If this was set, the result whould be tamarack:2.3.0_f2486d7
#
# PATCH_VERSION=0

```

In Jenkins add a job that pulls your Git repository and runs this command inside *Execute shell*: `SLACK_CHANNELS='#my-dev-channel' $EVOLENE_DIRECTORY/run.sh` or if you have no Slack `$EVOLENE_DIRECTORY/run.sh`

*That is it!* Evolene will tell you will all other things in your Slack channels or in the Jenkins console log, when you build your app.

:boom: :tada: Happy Coding!

## :+1: Evolene Features

* No configuration, unless you want it
* You need no Jenkins knowledge (almost), works on Jenkins, exactly as on your dev machine
* Testing and full integration testing
* SemVer for the win
* Handles all the Docker stuff
* Slack integrations of course
* Scan for passwords in your code
* ... and more

## :hammer: Build SemVer Docker Image 

### Overide the Name
Override the IMAGE_NAME in docker.conf for the image to build.

```bash
IMAGE_NAME='other-name'  $EVOLENE_DIRECTORY/run.sh
```

### Project Root

Build your project from an other directory.
If set the  $WORKSPACE set by Jenkins will be ignored.

```bash
PROJECT_ROOT='/other/jenkis/workspace/other-repo/'  $EVOLENE_DIRECTORY/run.sh
```

### Override Git Commit
Reuse a commit hash of the push that triggered the build.
If set the  $GIT_COMMIT set by Jenkins will be ignored.

```bash
GIT_COMMIT='abcdefhijkl1234456'  $EVOLENE_DIRECTORY/run.sh
```

### Specify SemVer Patch Version
The patch version in the SemVer tag is the Jenkins $BUILD_NUMBER.
If set the $BUILD_NUMBER set by Jenkins will be ignored, and patch version
will always be tag tamarack:2.3.`40`.

Patch version can also be set in `docker.conf` with PATCH_VERSION=40

```bash
BUILD_NUMBER='40'  $EVOLENE_DIRECTORY/run.sh
```


## :page_facing_up: Build information to file

If you whould like to get build information writen to a file. Set `BUILD_INFORMATION_OUTPUT_FILE` to a relative path
in your repo. Depending on the file extension a different file type will be created. (overwritten if it already exists).

```bash
BUILD_INFORMATION_OUTPUT_FILE='/config/version.js`' $EVOLENE_DIRECTORY/run.sh
```

### Module

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

### Typescript

```bash
BUILD_INFORMATION_OUTPUT_FILE='/info.ts`'
```

```javascript
exports const buildInfo {
  "jenkinsBuildDate": "2018-10-31 12:49:14",
  "dockerVersion": "2.3.40_f2486d7",
  "jenkinsBuild": "40",
  "dockerName": "tamarack",
  "dockerImage": "kthregistryv2.sys.kth.se/tamarack:2.3.40_f2486d7",
  "gitCommit": "f2486d79abf3af26225aa1dbde0fddfcd702c7e6",
  "gitBranch": "origin/master"
}
```

### JSON

```bash
BUILD_INFORMATION_OUTPUT_FILE='/config/info.json`'
```

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

### Conf-file

```bash
BUILD_INFORMATION_OUTPUT_FILE='/info.conf`'
```

```bash
jenkinsBuildDate=2018-10-31 12:49:14,
dockerVersion=2.3.40_f2486d7,
jenkinsBuild=40,
dockerName=tamarack,
dockerImage=kthregistryv2.sys.kth.se/tamarack:2.3.40_f2486d7,
gitCommit=f2486d79abf3af26225aa1dbde0fddfcd702c7e6,
gitBranch=origin/master
```

## :bell: Testing

### Unit Testing

Add a file in the root of your project called  `docker-compose-unit-tests.yml`. This
file is then run 

Before unit tests are run, the image is built and it´s id is availeble to
the Docker Compose file via `$LOCAL_IMAGE_ID`.

One way is then to mount your test directly into the docker images and run your tests on
that very image.

On your local machine you can run the same test using `docker-compose --file docker-compose-unit-tests.yml up --abort-on-container-exit --always-recreate-deps`.

```yaml
version: '3'
services:
  web:
    build: .
    image: $LOCAL_IMAGE_ID
    # Mount and run tests.
    volumes:
      - ./tests:/tests
    command: npm test
```


### Integration Testing

Add a file in the root of your project called  `docker-compose-integration-tests.yml`.
Before integration tests are run, the image is built and it´s id is availeble to
the Docker Compose file via `$LOCAL_IMAGE_ID`.

One way is then to start up your service and from other container run queries against
our server.  

On your local machine you can run the same test using `docker-compose --file docker-compose-integration-tests.yml up --abort-on-container-exit --always-recreate-deps`.

```yaml
version: '3'

services:
  web:
    build: .
    image: $LOCAL_IMAGE_ID
    environment:
      DB_URL: "mongodb://db:4444"
      DB_USER: "admin"
    ports:
      - 80
    depends_on:
      - db

  db:
    image: mongodb:latest
    ports:
      - 4444

  # Run curl commands from integration-tests against http://web:80
  integration-tests:
    build: ./tests/integration-tests
    depends_on:
      - web
```

## :mega: Slack Integration

### Slack web hook

The Slack webhook endpoint where the `SLACK_CHANNELS` can be found.

```bash
SLACK_WEB_HOOK='https://hooks.slack.com/services/1234asdfasd/' $EVOLENE_DIRECTORY/run.sh
```

### Slack channels to post build information to

Comma separated list of channels to post messages to. Messages are build inforation,
failures an push information.

```bash
SLACK_CHANNELS='#pipeline-logs,#devops' $EVOLENE_DIRECTORY/run.sh
```

## :cop: Security scaning

By default files in your repo will be scanned for strings that looks like passwords or tokens. We use [RepoSupervisor](https://github.com/auth0/repo-supervisor/) for this.

When your project is built a warning will be sent to SLACK_CHANNELS with the files that contain suspisious files. If a file gives you a false possitive, you can create a file in the root of your repository and name it `.scanignore`. In the .scanignore file you can add catalogs or files that the security scan should ignore.

### .scanignore formatting

```bash
# Catalogs starting with, or specific files.
/node_modules/
/imported-data/personnumer.txt
```

## :whale: Docker Registries

### Private Docker Registry

Unless `PUSH_PUBLIC` is set to `true`, this registry will be used.
The host without protocol.

```bash
REGISTRY_HOST='private-docker-registry.mycompany.com' $EVOLENE_DIRECTORY/run.sh
```

### Private Docker Registry User
The private `REGISTRY_HOST`:s  BASIC_AUTH user who has the rights to read and push to the private registry.

```bash
REGISTRY_USER='myuser' $EVOLENE_DIRECTORY/run.sh
```

### Private Docker Registry User

The private `REGISTRY_HOST`:s  BASIC_AUTH users password.

```bash
REGISTRY_PASSWORD='qwerty123' $EVOLENE_DIRECTORY/run.sh
```

#### Public repository

Set to `true` When you whant to push your image to `hub.docker.com/r/kthse`. This will push two tags,
the ususual SemVer with commit `tamarack:2.3.40_f2486d7`, but also and also a short tag with only SemVer `tamarack:2.3.40`. This is done to enable reuse of tags.

```bash
PUSH_PUBLIC='True' # True or False
```

## Other envs

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

### Current Evolene running

Path to the directory of a Evolene dist version.
Used in Jenkin builds for shorter path when envoking the Evolene itself `$EVOLENE_DIRECTORY/run.sh`.
Also gives you a way of specifing what version of Evolene that is used.

```bash
EVOLENE_DIRECTORY='`/var/lib/jenkins/workspace/evolene/dist/evolene-1.6`'
```

## :clipboard: Setup Evolene on Jenkins


### 1. Add default envs for builds on the Jenkins server

We recommend that the following envs are available to each Jenkins job. The can be overridden by
env arguments per build as shown above.

```bash
EVOLENE_DIRECTORY='/var/lib/jenkins/workspace/evolene/dist/evolene-1.6'
SLACK_WEB_HOOK='https://hooks.slack.com/services/1234asdfasd/'
REGISTRY_HOST='private-docker-registry.mycompany.com'
REGISTRY_PASSWORD='very-secret-pwd'
REGISTRY_USER='jenkins-ci'
```
### 2. Set up a build task that builds Evolene
1. Add a new you that pulls the Evolene source 
2. Add a *Execute shell* step.
```bash
/create_dist.sh
LATEST_DIST=$(ls -tp dist | grep -v / | head -1)
tar xvf dist/$LATEST_DIST -C dist
rm -rf dist/latest
mkdir dist/latest
tar xvf dist/$LATEST_DIST -C dist/latest --strip 1
chmod -R 700 dist/latest
```
3. Run the Jenkins job. This will create a executable Evolene dist in `/var/lib/jenkins/workspace/evolene/dist/evolene-1.6`.


### 3. Test your setup
Test your setup by adding a Docker application that follows Evolene [Usage Requirements](https://gita.sys.kth.se/Infosys/evolene/blob/master/README.md#exclamation-user-requirements) and run a *Execute shell*.
`$EVOLENE_DIRECTORY/run.sh`

## :computer: Setup Evolene for development

### Run locally

```bash
python run.py docker run-pipeline
```

### Create a distribution

Note! The version of the dist is defined in `setup.py`

```bash
./create_dist.sh`
```

### Run unit tests

```bash
./run_tests.sh
```
