
import math
import os


def calculate_area(radius):
    return math.pi * radius * radius


def greet_user(name: str):
    print("Hello", name)


class Calculator:
    def add(self, a, b):
        return a + b