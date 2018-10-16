# Evolene - Standradized building on Jenkins

Jenkins build as code.

Features:
* Verifies **docker.conf**
* Verifies **Dockerfile**
* Repo security scanning for passwords and secrets
* Docker build
* SemVer versioning of Docker images
* Push to Docker Registry
* Slack integration for build information
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

All environment variables for configuration:

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
BUILD_INFORMATION_OUTPUT_FILE - Print build info to js-module file 
EVOLENE_DIRECTORY             - The working directory of evolene (used on jenkins to work properly)
EXPERIMENTAL                  - Feature toogle for latest features
```

Changes to this project are automatically sent to https://build.sys.kth.se

# Enable integration tests with docker-compose-integration-tests.yml
## docker-compose-integration-tests.yml
Creating a file named ```docker-compose-integration-tests.yml``` in the root of the project tells Jenkins to run integration tests.
The following is an example file from the [lms-sync-users](https://github.com/KTH/lms-sync-users) app:
```
version: '3.2'

services:
  web:
    build: .
    image: $LOCAL_IMAGE_ID

    volumes:
      - ./test:/test
      - ./node_modules:/node_modules
    tty: true
    command: npm run test:docker-integration
    environment:
      - CANVAS_API_URL
      - CANVAS_API_KEY
      - AZURE_HOST
      - AZURE_SHARED_ACCESS_KEY_NAME
      - AZURE_SHARED_ACCESS_KEY
```
The last block, environment, defines which environment variables should be passed into the docker container.

With this file in place, Jenkins will try to run the integration tests. But for the tests to run successfully, the credentials has to be setup in Jenkins.

## Jenkins credentials
Add credentials by going to the [Credentials](https://build.sys.kth.se/credentials/store/system/domain/_/) page in Jenkins, and create the credentials that should be passed into the docker container as ```Secret text```. In this example, one secret text should be created for each of the following:
- CANVAS_API_URL
- CANVAS_API_KEY
- AZURE_HOST
- AZURE_SHARED_ACCESS_KEY_NAME
- AZURE_SHARED_ACCESS_KEY

_However, this is not enough to actually tell Jenkins to pass the credentials into the build as environment variables._

## Binding credentials to environment variables in Jenkins
Go to the Jenkins project page, and choose configure ([lms-sync-users in this example](https://build.sys.kth.se/job/lms-sync-users/configure)).

Under the ```Build Environment```, check the option ```Use secret text(s) or file(s)```. This will show a new block, named ```Bindings```.

Add a ```Secret text``` binding for each of the above specified environment variables.

Now everything should be setup for the integration tests to run successfully. Time to get some pop corn 🍿
