import subprocess

from modifier import Modifier


class Runner:
    def __init__(self, logger, modifier: Modifier, **kwargs):
        self.logger = logger
        self.simulator = None
        self.modifier = modifier

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.logger.info(f"\nconfiguration of Runner class:{self.__dict__}")

    def run_once(self, number):
        # Call the modifier to change the file and run the simulation
        # At the same time, the index of the modifier will be subtracted by 1.
        # number = f"{number:05}"
        subject = self.modifier.subject
        value = getattr(self.modifier, subject)

        if self.simulator == 'iv':
            subprocess.run(["./simulate_iv.sh", 'iv', f'{subject}', f'{value}'], check=True)
        elif self.simulator == 'qs':
            subprocess.run(["./simulate_qs.sh", 'qs', f'{subject}', f'{value}'], check=True)
        elif self.simulator == 'all':
            subprocess.run(["./simulate_iv.sh", 'iv', f'{subject}', f'{value}'], check=True)
            subprocess.run(["./simulate_qs.sh", 'qs', f'{subject}', f'{value}'], check=True)
        pass

    def run(self):
        for i in range(self.modifier.index):
            self.logger.info(f"running {i}")
            self.modifier.modify()
            self.run_once(i)
