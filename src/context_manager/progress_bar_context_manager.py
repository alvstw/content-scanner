from tqdm import tqdm

from src import context


class ProgressBarContextManager:
    tqdmInstance: tqdm

    def __init__(self, *args, **kwargs):
        self.tqdmInstance = tqdm(*args, **kwargs)
        context.messageHelper.setProgressInstance(self.tqdmInstance)

    def __enter__(self):
        return self.tqdmInstance

    def __exit__(self, exc_type, exc_val, exc_tb):
        context.messageHelper.clearProgressInstance()
        self.tqdmInstance.close()
