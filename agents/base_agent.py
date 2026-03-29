from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, model):
        self.model = model
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass