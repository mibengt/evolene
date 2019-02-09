__author__ = 'tinglev'

from modules.util import process
from modules.util.environment import Environment
from modules.util.exceptions import PipelineException
from modules.util import pipeline_data

def build(labels=None):
    build_cmd = 'docker build --quiet'
    root = Environment.get_project_root()
    if labels:
        for label in labels:
            build_cmd = f'{build_cmd} --label {label}'
    return process.run_with_output(f'{build_cmd} {root}')

def grep_image_id(image_id):
    try:
        return process.run_with_output(f'docker images | grep {image_id}')
    except PipelineException:
        # An exception here means that the grep failed and that the image is missing
        return None

def get_container_status(container_id):
    return process.run_with_output(f'docker inspect --format=\'{{{{.State.Status}}}}\' '
                                   f'{container_id}')

def run(image_id):
    return process.run_with_output(f'docker run -d {image_id}').rstrip()

def stop_and_remove_container(container_id):
    return process.run_with_output(f'docker rm -f {container_id}')

def tag_image(image_id, tag):
    return process.run_with_output(f'docker tag {image_id} {tag}')

def push(registry_image_name):
    return process.run_with_output(f'docker push {registry_image_name}')

def inspect_image(image_id):
    return process.run_with_output(f'docker image inspect {image_id}')

def pull(image_name):
    return process.run_with_output(f'docker pull {image_name}')

def run_unit_test_compose(compose_test_file, data):
    return run_test(compose_test_file, data)

def run_integration_tests(compose_test_file, data):
    return run_test(compose_test_file, data)

def run_test(compose_test_file, data):
    image_id = data[pipeline_data.LOCAL_IMAGE_ID]
    cmd = (f'LOCAL_IMAGE_ID={image_id} '
           f'docker-compose --file {compose_test_file} up '
           f'--abort-on-container-exit '
           f'--always-recreate-deps')
    return process.run_with_output(cmd)
