import os
script_dir = os.path.dirname(__file__)

class Dictionary:
    def __init__(self, num):
        if num not in [1, 2]:
            raise(BaseException("Invalid dictionary number!"))

        self.__num = num
        self.__string = ""

        current_dir = os.path.dirname(__file__)

        with open(os.path.join(current_dir, f"dictionaries/dictionary_{num}.txt")) as f:
            self.__string = f.read()

    def string(self):
        return self.__string

    def words(self):
        if self.__num == 1:
            return self.__string.split("\n")
        else:
            return self.__string.split(" ")
