# from abc import ABC, abstractmethod 
  
  
class Event: 
  
    def __init__(self, size: int, msgId: int, payload, vehicleId: str):
        self.size = size
        self.msgId = msgId
        self.payload = payload
        self.vehicleId = vehicleId
        

    def log(self) -> str:
        
        text = "["
        for v in list(self.payload):
            text += f"{v:02X} "
        
        text += "]"
        return text

    def __str__(self):
        return f"({self.size:02X}) {self.msgId:02X} {self.log()}"

    def __repr__(self):
        return self.__str__()

    # @abstractmethod
    # def noofsides(self): 
    #     pass