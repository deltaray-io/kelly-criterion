
from datetime import date

from pytest import approx

from kelly_criterion import calc_kelly_leverages


def test_kelly_criterion():
    # Given a time period and multiple securities
    start_date = date(2018, 1, 1)
    end_date = date(2018, 12, 31)
    securities = {'AAPL', 'IBM'}

    # When we calculate kelly leverages
    actual_leverages = calc_kelly_leverages(securities, start_date, end_date)

    # Then the calculated leverages should match the actual ones
    expected_leverages = {'AAPL': 1.2944, 'IBM': -5.2150}
    assert expected_leverages == approx(actual_leverages, rel=1e-3)
