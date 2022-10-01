from abc import abstractmethod, ABC
import pickle, json

class SerializationInterface(ABC):

    @abstractmethod
    def serialize(self, data, filename):
        pass

    @abstractmethod
    def deserialize(self, filename):
        pass

class JsonSerialization(SerializationInterface):
    def serialize(self, data, filename):
        with open(filename, "w") as file:
            json.dump(data, file)

    def deserialize(self, filename):
        with open(filename, "r") as file:
            return json.load(file)



class BinSerialization(SerializationInterface):
    def serialize(self, data, filename):
        with open(filename, "wb") as file:
            pickle.dump(data, file)

    def deserialize(self, filename):
        with open(filename, "rb") as file:
            return pickle.load(file)


data = [13, 'cat', 1/2, 8, (3, 5)]
seria = JsonSerialization()
seria.serialize(data, 'test.json')
print(seria.deserialize('test.json'))
data2 = ['simple', 42]
seria2 = BinSerialization()
seria2.serialize(data2, 'test2.bin')
print(seria2.deserialize('test2.bin'))