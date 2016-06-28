Kelly Criterion
===============
Money management strategy based on Kelly J. L.'s formula described in "A New Interpretation of Information Rate" [1]. 
The formula was adopted to gambling and stock market by Ed Thorp, et al., see:
"The Kelly Criterion in Blackjack Sports Betting, and the Stock Market" [2].

This program calculates the optimal capital allocation for the provided portfolio of securities with the formula:

        `f_i = m_i / s_i^2`

where
  * `f_i` is the calculated leverage of the i-th security from the portfolio
  * `m_i` is the mean of the return of the i-th security from the portfolio
  * `s_i` is the standard deviation of the return of the i-th security from the portfolio

assuming that the strategies for the securuties are all statistically independent.

The stock quotes are downloaded from Yahoo Finance using Pandas.

Reference (Matlab) implementation was taken from Ernie Chan's Quantitative Trading book [3].

Installation
------------
`pip install kelly_criterion`

Usage
-----
`kelly_criterion [--risk-free-rate=<pct>] <start-date> <end-date> <security>...`

Example
-------
```
$ kelly_criterion --risk-free-rate 0.04 2001-02-26 2014-12-28 IBB VDE SPY
Kelly Criterion calculation
Arguments: risk-free-rate=0.04 start-date=2001-02-26 end-date=2014-12-28 securities=['IBB', 'VDE', 'SPY']

Leverages per security:
  IBB: 3.61
  SPY: -2.73
  VDE: 1.04
Sum leverage: 1.92
```

Dependencies
------------
  * Python 2.7
  * [Numpy](http://www.numpy.org/)
  * [Pandas](http://pandas.pydata.org/)
  * [Docopt](http://docopt.org/)

References
----------
  * [1]: [A New Interpretation of Information Rate](http://ieeexplore.ieee.org/stamp/stamp.jsp?reload=true&tp=&arnumber=6771227)
  * [2]: [The Kelly Criterion in Blackjack Sports Betting, and the Stock Market](http://www.edwardothorp.com/sitebuildercontent/sitebuilderfiles/beatthemarket.pdf)
  * [3]: [Ernest P. Chan: Quantitative Trading (ISBN 978-0470284889)](http://www.amazon.com/Quantitative-Trading-Build-Algorithmic-Business/dp/0470284889)
