import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sample_files.sample import calculate_area, greet_user, Calculator


def test_calculate_area():
    assert calculate_area(2) == math.pi * 4


def test_calculate_area_zero_radius():
    assert calculate_area(0) == 0


def test_greet_user(capsys):
    greet_user("Sanjay")
    captured = capsys.readouterr()
    assert "Hello Sanjay" in captured.out


def test_add_positive_numbers():
    calculator = Calculator()
    assert calculator.add(2, 3) == 5


def test_add_negative_numbers():
    calculator = Calculator()
    assert calculator.add(-2, -3) == -5
