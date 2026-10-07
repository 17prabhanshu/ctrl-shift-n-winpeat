from src.cleaning.salary_parser import parse_ds_salary, parse_analytics_salary
import numpy as np

def test_parse_ds_salary():
    assert parse_ds_salary('7.8L') == 780000
    assert parse_ds_salary('12.8L') == 1280000
    assert np.isnan(parse_ds_salary('invalid'))

def test_parse_analytics_salary():
    assert parse_analytics_salary('6to10') == (600000, 1000000)
    assert parse_analytics_salary('Not disclosed') == (np.nan, np.nan)
