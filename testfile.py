# -*- coding: utf-8 -*-
import tetueSrc
from enum import Enum, auto

class Color(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()

class Test:
    def __init__(self, name, nummer = 5 ):
        self.__name = name
        self.__nummer = nummer
        self.color = Color.RED

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, new_name):
        self.__name = new_name
    @property
    def nummer(self):
        return self.__nummer

def main():
    PREFIX = "!"
    teststring = "!gehk!"
    output_text = tetueSrc.get_string_element("outputtext", "huhn")
    print(output_text)
    
    if PREFIX in teststring:
        print("yes")
    else:
        print("no")

    new_test = Test("Roland", nummer = 77)
    print(new_test.name)
    new_test.name = "Vanessa"
    print(new_test.name)
    print(new_test.nummer)
    print(new_test.color)
    if new_test.color == Color.GREEN:
        print("Yes")
    else:
        print("No")
    print(list(Color))

if __name__ == "__main__":
    main()
