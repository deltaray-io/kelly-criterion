#!/usr/bin/env python
# Copyright (c) 2014-2015, Tibor Kiss <tibor.kiss@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""Kelly Criterion - (c) 2014-2015, Tibor Kiss <tibor.kiss@gmail.com>

Usage:
  ./kelly_criterion.py [--risk-free-rate=<pct>] <start-date> <end-date> <security>...

Options:
  --risk-free-rate=<pct>  Annualized percentage of the Risk Free Rate. [default: 0.04]

"""

import sys
from datetime import datetime

from docopt import docopt

import pandas.io.data as web
from pandas import DataFrame

from numpy.linalg import inv


def calc_kelly_leverages(securities, start_date, end_date, risk_free_rate=0.04):
    """Calculates the optimal leverages for the given securities and time frame.
    Returns a list of (security, leverage) tuple with the calculate optimal leverages.

    Note: risk_free_rate is annualized
    """
    f = {}
    ret = {}
    excess_return = {}

    # Download the historical prices from Yahoo Finance and calculate the
    # excess return (return of security - risk free rate) for each security.
    for symbol in securities:
        try:
            hist_prices = web.DataReader(symbol, 'yahoo', start_date, end_date)
        except IOError, e:
            print 'Unable to download data for %s. Reason: %s' % (symbol, str(e))
            return None

        f[symbol] = hist_prices

        ret[symbol] = hist_prices['Adj Close'].pct_change()
        excess_return[symbol] = (ret[symbol] - (risk_free_rate / 252))  # risk_free_rate is annualized

    # Create a new DataFrame based on the Excess Returns.
    df = DataFrame(excess_return).dropna()

    # Calculate the CoVariance and Mean of the DataFrame
    C = 252 * df.cov()
    M = 252 * df.mean()

    # Calculate the Kelly-Optimal Leverages using Matrix Multiplication
    F = inv(C).dot(M)

    # Return a list of (security, leverage) tuple
    return zip(df.columns.values.tolist(), F)


def main():
    """Entry point of Kelly Criterion calculation."""

    print "Kelly Criterion calculation"
    args = docopt(__doc__, sys.argv[1:])

    # Parse risk-free-rate
    try:
        risk_free_rate = float(args['--risk-free-rate'])
    except ValueError, e:
        print 'Error converting risk-free-rate to float: %s' % args['--risk-free-rate']
        sys.exit(-1)

    # Verify risk-free-rate
    if not 0 <= risk_free_rate <= 1.0:
        print 'Error: risk-free-rate is not in between 0 and 1: %.2f' % risk_free_rate
        sys.exit(-1)

    # Parse start and end dates
    try:
        start_date = datetime.strptime(args['<start-date>'], "%Y-%m-%d").date()
    except ValueError, e:
        print 'Error parsing start-date: %s' % args['<start-date>']
        sys.exit(-1)

    try:
        end_date = datetime.strptime(args['<end-date>'], "%Y-%m-%d").date()
    except ValueError, e:
        print 'Error parsing end-date: %s' % args['<start-date>']
        sys.exit(-1)

    print 'Arguments: risk-free-rate=%s start-date=%s end-date=%s securities=%s' % (args['--risk-free-rate'], start_date, end_date, args['<security>'])
    print ''

    # Calculate the Kelly Optimal leverages
    leverages = calc_kelly_leverages(args['<security>'], start_date, end_date, risk_free_rate)

    # Print the results if calculation was successful
    if leverages:
        print "Leverages per security: "
        for (name, val) in leverages:
            print "  %s: %.2f" % (name, val)

        print "Sum leverage: %.2f " % reduce(lambda x, y: x+y, map(lambda z: z[1], leverages))


if __name__ == '__main__':
    main()


