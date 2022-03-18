import os
script_dir = os.path.dirname(__file__)

class DictionaryLoader:
    def __init__(self):
        self.__dictionary1_string = ""
        self.__dictionary2_string = ""

        current_dir = os.path.dirname(__file__)

        with open(os.path.join(current_dir, "dictionaries/dictionary_1.txt")) as f:
            self.__dictionary1_string = f.read()

        with open(os.path.join(current_dir, "dictionaries/dictionary_2.txt")) as f:
            self.__dictionary2_string = f.read()

    def dictionary1_string(self):
        return self.__dictionary1_string

    def dictionary2_string(self):
        return self.__dictionary2_string

    def dictionary1(self):
        return self.__dictionary1_string.split("\n")

    def dictionary2(self):
        return self.__dictionary2_string.split("\n")