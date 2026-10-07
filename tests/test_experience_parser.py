from src.cleaning.experience_parser import parse_experience
import numpy as np

def test_parse_experience():
    assert parse_experience('6-10 yrs') == (6, 10, 8)
    assert parse_experience('3-8 yrs') == (3, 8, 5.5)
    assert parse_experience('2') == (2, 2, 2)
    assert parse_experience('invalid') == (np.nan, np.nan, np.nan)
