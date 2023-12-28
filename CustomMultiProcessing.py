from abc import ABC,abstractmethod

class customMultiProcess(ABC):
    
    def __init__(self) -> None:
        
        super().__init__()

    @abstractmethod
    def scrapeLinks(self):
        pass

    @abstractmethod 
    def scrapeData(self,instance,url_chunk):
        pass
    
