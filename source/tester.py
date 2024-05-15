"""
There are three classes used in this module.
They have the same processing flow:
    1. Be called by the main function one by one.
    2. Get the configuration from the complete json file
    3. Output the data of initialization.
"""

import json

from modifier import Modifier
from runner import Runner
from dataProcessor import DataProcessor


class Tester:
    def __init__(self, path, logger):
        self.modifier = None
        self.runner = None
        self.dataProcessor = None

        self.logger = logger
        with open(path, 'r') as f:
            self.config_json = json.load(f)
            self.logger.info(json.dumps(self.config_json, indent=4))

    def run(self):
        self.modifier = Modifier(self.logger, **self.config_json.get('modifier'))
        self.runner = Runner(self.logger, self.modifier, **self.config_json.get('runner'))
        self.runner.run()
        pass

    def process_data(self):
        self.dataProcessor = DataProcessor(self.logger, self.config_json.get('modifier'), **self.config_json.get('dataProcessor'))
        # ToDo Test
        self.dataProcessor.process(self.modifier.subject)
        # self.dataProcessor.process("amount")
        pass
