__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util import pipeline_data
from modules.util.slack import Slack

class CelebrateStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.BUILD_NUMBER]

    def get_required_data_keys(self):
        return [pipeline_data.IMAGE_NAME]

    def run_step(self, data):
        self.do_we_have_a_reason_to_party(data)
        return data

    def do_we_have_a_reason_to_party(self, data):
        message = self.get_party_message(data)
        if message:
            Slack.send_to_slack(self.get_party_message(data), icon=":parrot_party:")
            
    def get_party_message(self, data):
        
        if int(Environment.get_build_number()) == 100:
            return "<!here> :clap: Get :clap: your  :clap: self  :clap:  a  :clap: coffee  :clap: break. This was the 100th build of {}!\nhttps://www.youtube.com/watch?v=eCzhNPSXpfI".format(data[pipeline_data.IMAGE_NAME])

        if int(Environment.get_build_number()) == 200:
            return "<!here> :parrot_party: :parrot_party: :parrot_party: {} build number 200! You are worth some :champagne:\nhttps://www.youtube.com/watch?v=eCzhNPSXpfI".format(data[pipeline_data.IMAGE_NAME])

        if int(Environment.get_build_number()) == 300:
            return "<!here> :parrot_party: :parrot_party: :parrot_party: {} build number 300! You are worth some :champagne:\nhttps://www.youtube.com/watch?v=eCzhNPSXpfI".format(data[pipeline_data.IMAGE_NAME])

        if int(Environment.get_build_number()) == 400:
            return "<!here> :parrot_party: :parrot_party: :parrot_party: {} build number 400! You are worth some :champagne:\nhttps://www.youtube.com/watch?v=eCzhNPSXpfI".format(data[pipeline_data.IMAGE_NAME])

        if int(Environment.get_build_number()) == 500:
            return "<!here> :parrot_party: :parrot_party: :parrot_party: {} build number 500! You are worth some :champagne:\nhttps://www.youtube.com/watch?v=eCzhNPSXpfI".format(data[pipeline_data.IMAGE_NAME])

        if int(Environment.get_build_number()) == 1000:
            return "<!here> :drum_with_drumsticks: 1 000 builds of {} and counting! \nhttps://www.youtube.com/watch?v=eCzhNPSXpfI".format(data[pipeline_data.IMAGE_NAME])

        return None