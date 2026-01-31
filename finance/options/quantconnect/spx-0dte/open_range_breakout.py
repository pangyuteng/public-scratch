#
# references
#
# [1] Carlo Zarattini, Beat the Market An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)
#     https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172
#     https://www.quantconnect.com/forum/discussion/17091/beat-the-market-an-effective-intraday-momentum-strategy-for-s-amp-p500-etf-spy/
#
# [2] /u/shock_and_awful, Profitably Trading the SPX Opening Range with Option Credit Spreads.
#     https://substack.com/home/post/p-172286099
#     https://www.reddit.com/r/algotrading/comments/1nc1p7q/full_deep_dive_into_profitable_0dte_strategy_for
#

# open range breakout "ORB" references
# https://optionalpha.com/blog/opening-range-breakout-0dte-options-trading-strategy-explained
# https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172
# https://www.reddit.com/r/algotrading/comments/1nc1p7q/full_deep_dive_into_profitable_0dte_strategy_for/


from AlgorithmImports import *

class VolatilityTradingOptionAlgorithm(QCAlgorithm):

    def initialize(self):

        self.set_start_date(2022, 1, 1)
        self.set_end_date(2024, 12, 31)
        
        self.set_cash(100000)

        self.universe_settings.asynchronous = True
        self.settings.automatic_indicator_warm_up = True
        self.universe_settings.resolution = Resolution.MINUTE

        self._vix = self.add_index('VIX')
        self._spx = self.add_index('SPX')
        
        self._spxw = self.add_index_option(self._spx.symbol,"SPXW")
        self._spxw.set_filter(self.option_filter)

        self._spxw.set_fee_model(TastytradeFeeModel())
        self._spxw.set_slippage_model(ConstantSlippageModel(0.01))

        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.after_market_open(self._spxw.symbol, 1), self._mark_market_open)
        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.after_market_open(self._spxw.symbol, 60), self._open_trade)
        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.every(timedelta(minutes=1)),self._manage_trade)
        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.before_market_close(self._spxw.symbol, 1),self._close_trade)

    def option_filter(self, universe):
        return universe.expiration(0, 0).weeklys_only()

    def _mark_market_open(self):
        self.spx_open = self._spx.price
        self.vix_open = self._vix.price

    def _manage_trade(self):
        if self.portfolio.invested:
            if self.order_ticket is None: # something is wrong, liquidate.
                self.liquidate()
                return
            # take profit at 50%
            total_holdings_cost = np.sum([float(self.portfolio[ticket.symbol].holdings_cost) for ticket in self.order_ticket])
            if total_holdings_cost == 0:
                pass # bad/no data?
            else:
                total_unrealized_profit_ratio = self.portfolio.total_unrealised_profit/(-1*total_holdings_cost)
                if total_unrealized_profit_ratio > 0.5:
                    self.liquidate()
                elif total_unrealized_profit_ratio < -3.0:
                    self.liquidate()

    def _close_trade(self):
        if self.portfolio.invested:
            self.liquidate()

    def _open_trade(self):
        # see figure 1 in https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172
        breakout = True if (self._spx.price/self.spx_open - 1) > 0.002 else False

        self.order_ticket = None
        if not self.portfolio.invested and breakout:

            chain = self.current_slice.option_chains.get(self._spxw.symbol, None)
            if not chain: return

            expiry = min([x.expiry for x in chain])

            puts = [i for i in chain if i.expiry == expiry and i.right == OptionRight.PUT]
            if len(puts) == 0: return

            calls = [i for i in chain if i.expiry == expiry and i.right == OptionRight.CALL]
            if len(calls) == 0: return
            
            puts = sorted([x for x in puts if x.strike < self._spx.price],key=lambda x: x.strike)
            short_put_strike = sorted(puts,key=lambda x: abs(x.greeks.delta - 0.15*-1 ))[0].strike
            long_put_strike = sorted(puts,key=lambda x: abs(x.greeks.delta - 0.10*-1 ))[0].strike
            
            if not short_put_strike > long_put_strike: return

            quantity = 1
            strategy = OptionStrategies.bull_put_spread(self._spxw.symbol,short_put_strike,long_put_strike,expiry)
            self.order(strategy, quantity)
            self.order_ticket = self.order(strategy, quantity)

    def on_order_event(self, order_event):
        if order_event.status == OrderStatus.FILLED and order_event.is_assignment:
            self.liquidate()
