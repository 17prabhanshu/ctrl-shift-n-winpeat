import numpy as np
from src.cleaning.salary_parser import parse_ds_salary, parse_analytics_salary

def test_parse_ds_salary():
    val, fmt = parse_ds_salary('7.8L')
    assert val == 780000.0
    assert fmt == 'lakhs'

    val2, fmt2 = parse_ds_salary('12.8L')
    assert val2 == 1280000.0
    assert fmt2 == 'lakhs'

    val_inv, fmt_inv = parse_ds_salary('invalid')
    assert np.isnan(val_inv)
    assert fmt_inv.startswith('unmatched')

def test_parse_analytics_salary():
    s_min, s_max, fmt = parse_analytics_salary('6to10')
    assert s_min == 600000.0
    assert s_max == 1000000.0
    assert fmt == 'range_lpa'

    s_min_nd, s_max_nd, fmt_nd = parse_analytics_salary('Not disclosed')
    assert np.isnan(s_min_nd)
    assert np.isnan(s_max_nd)
    assert fmt_nd == 'not_disclosed'
