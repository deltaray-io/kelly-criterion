# Copyright (c) 2014-2019, Tibor Kiss <tibor.kiss@gmail.com>
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
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Kelly Criterion - (c) 2014-2019, Tibor Kiss <tibor.kiss@gmail.com>

Usage:
  kelly_criterion [options] <start-date> <end-date> <security>...

Options:
  --risk-free-rate=<pct>  Annualized percentage of the Risk Free Rate.
                          [default: 0.04]

"""

import sys
from datetime import datetime, date
from typing import Set, Dict
import logging

from docopt import docopt

from pandas import DataFrame
from numpy.linalg import inv
from iexfinance.stocks import get_historical_data

log = logging.getLogger(__name__)


def calc_kelly_leverages(securities: Set[str],
                         start_date: date,
                         end_date: date,
                         risk_free_rate: float = 0.04) -> Dict[str, float]:
    """Calculates the optimal leverages for the given securities and
    time frame. Returns a list of (security, leverage) tuple with the
    calculate optimal leverages.

    Note: risk_free_rate is annualized
    """
    f = {}
    ret = {}
    excess_return = {}

    # Download the historical prices from Yahoo Finance and calculate the
    # excess return (return of security - risk free rate) for each security.
    for symbol in securities:
        try:
            hist_prices = get_historical_data(
                symbol, start=start_date, end=end_date,
                output_format='pandas')
        except IOError as e:
            raise ValueError(f'Unable to download data for {symbol}. '
                             f'Reason: {str(e)}')

        f[symbol] = hist_prices

        ret[symbol] = hist_prices['close'].pct_change()
        # risk_free_rate is annualized
        excess_return[symbol] = (ret[symbol] - (risk_free_rate / 252))

    # Create a new DataFrame based on the Excess Returns.
    df = DataFrame(excess_return).dropna()

    # Calculate the CoVariance and Mean of the DataFrame
    C = 252 * df.cov()
    M = 252 * df.mean()

    # Calculate the Kelly-Optimal Leverages using Matrix Multiplication
    F = inv(C).dot(M)

    # Return a list of (security, leverage) tuple
    return {security: leverage
            for security, leverage in zip(df.columns.values.tolist(), F)}


def main():
    """Entry point of Kelly Criterion calculation."""
    logging.basicConfig(level=logging.INFO)

    log.info("Kelly Criterion calculation")
    args = docopt(__doc__, sys.argv[1:])

    # Parse risk-free-rate
    try:
        risk_free_rate = float(args['--risk-free-rate'])
    except ValueError:
        log.error(f"Error converting risk-free-rate to float: "
                  f"{args['--risk-free-rate']}")
        sys.exit(-1)

    # Verify risk-free-rate
    if not 0 <= risk_free_rate <= 1.0:
        log.error(f"risk-free-rate is not in between 0 and 1: "
                  f"{risk_free_rate:%.2f}")
        sys.exit(-1)

    # Parse start and end dates
    try:
        start_date = datetime.strptime(args['<start-date>'], "%Y-%m-%d").date()
    except ValueError:
        log.error(f"Error parsing start-date: {args['<start-date>']}")
        sys.exit(-1)

    try:
        end_date = datetime.strptime(args['<end-date>'], "%Y-%m-%d").date()
    except ValueError:
        log.error(f"Error parsing end-date: {args['<start-date>']}")
        sys.exit(-1)

    log.info(
        f"Arguments: "
        f"risk-free-rate={args['--risk-free-rate']} "
        f"start-date={start_date} "
        f"end-date={end_date} "
        f"securities={args['<security>']}")

    # Calculate the Kelly Optimal leverages
    try:
        leverages = calc_kelly_leverages(
            args['<security>'], start_date, end_date, risk_free_rate)
    except ValueError as e:
        log.error(f"Error during Kelly calculation: {str(e)}")
        sys.exit(-1)

    # Print the results if calculation was successful
    if leverages:
        log.info("Leverages per security:")
        sum_leverage = 0
        for symbol, leverage in leverages.items():
            sum_leverage += leverage
            log.info(f"  {symbol}: {leverage:.2f}")

        log.info(f"Sum leverage: {sum_leverage}")


if __name__ == '__main__':
    main()
