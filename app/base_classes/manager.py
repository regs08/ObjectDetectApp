from abc import ABC, abstractmethod
from threading import Thread, Event

from utils.configs.config_manager import ConfigManager
from utils.factories.annotator_factory import AnnotatorFactory


class BaseManager(ABC):
    def __init__(self):
        self.name = None
        self.set_name()
        self.config = None
        self.running = Event()
        self.config_manager= ConfigManager()
        self.annotator_factory = AnnotatorFactory()

        if self.name is None:
            raise NotImplementedError('self.name has not been implemented yet.')

    @abstractmethod
    def initialize(self, *args):
        """
        Initialize the manager with the required parameters.
        """
        pass

    @abstractmethod
    def set_name(self):
        """
        Fill in the `name` attribute of the class.
        """
        pass

    @abstractmethod
    def run(self, *args):
        """
        The main logic for the manager's thread. This must be implemented in subclasses.
        """
        pass

    def start_thread(self):
        """
        Start the thread that executes the `run` method.
        """
        if not self.thread or not self.thread.is_alive():
            self.running.set()  # Signal that the thread should run
            self.thread = Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop_thread(self):
        """
        Stop the thread by clearing the running event and joining the thread.
        """
        self.running.clear()  # Signal the thread to stop
        if self.thread:
            self.thread.join()
