# from abc import ABC, abstractmethod 
  
  
class Event: 
  
    def __init__(self, size: int, msgId: int, payload, vehicleId: str):
        self.size = size
        self.msgId = msgId
        self.payload = payload
        self.name = vehicleId
        
    def build(self):
        return self

    def log(self) -> str:
        
        text = "["
        for v in list(self.payload):
            text += f"{v:02X} "

        text = text.strip()        
        text += "]"
        return text

    def __str__(self):
        return f"[{self.name}] Uncategorised Event:: size={self.size:02X} msgid={self.msgId:02X} {self.log()}"

    def __repr__(self):
        return self.__str__()

    # @abstractmethod
    # def noofsides(self): 
    #     pass