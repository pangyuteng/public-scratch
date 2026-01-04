


use straddle price change to speculate on future intraday IV

ignore FOMC, event days.

compute correlation of major stocks to gauge sentiment

thurs,friday ? ignore, do something different ?

op ex. every montly third wed,thu,fri
https://www.optionseducation.org/referencelibrary/expiration-calendar

ignore switch strategy (long or short) based on $insert-criteria

check performance with ipynb


--

# nice starter links


https://www.quantconnect.cloud/backtest/6eacfbf079b3e553d97441ff44376ff8
https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/option-strategies/bull-put-spread
https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/risk-management/supported-models
https://www.quantconnect.com/docs/v2/writing-algorithms/securities/asset-classes/index-options/requesting-data/universes
https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/algoseek/us-index-options


--

# code hoarding
```

self._vix = self.add_index('VIX')
self._spx = self.add_index('SPX')

self._spxw = self.add_index_option(self._spx.symbol,"SPXW")
self._spxw.set_filter(self.option_filter)

def option_filter(self, universe):
    return universe.expiration(0, 0).weeklys_only()
    #return universe.expiration(0, 0).include_weeklys()

chain = [c for c in chain if OptionSymbol.is_weekly(c)]
if len(chain) == 0: return

if self.time.date().isoweekday() in [4,5]: # reduce size for Thur and Fri


# rsi
self._spy = self.add_equity("SPY", Resolution.DAILY)
self._rsi = self.rsi(self._spy, 5)
if rsi_value < 55:
rsi_value = self._rsi.current.value

```