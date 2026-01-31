""" 

 Tammy Chambless Explains Her 0DTE Options Iron Condor Strategy
 https://www.youtube.com/watch?v=o-CmLEeiaoU

Tammy's Multiple Entry Iron Condor (MEIC+):
+ 1.00 to 1.75 credit on each side (50 wide?)
+ 1x Net Stop (2x initial credit)
+ manage each side separately
+ twist: set stop for $.1 less than 1x Net Stop

"""

from AlgorithmImports import *

class VolatilityTradingOptionAlgorithm(QCAlgorithm):

    def initialize(self):

        self.set_start_date(2022, 1, 1) # see ref.4
        self.set_end_date(2025, 12, 31)
        
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

        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.after_market_open(self._spx.symbol, 1), self._mark_market_open)
        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.after_market_open(self._spx.symbol, 60), self._open_trade)
        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.every(timedelta(minutes=1)),self._manage_trade)
        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.before_market_close(self._spx.symbol, 1),self._close_trade)

    def option_filter(self, universe):
        return universe.expiration(0, 0).weeklys_only() # see ref.3

    def on_order_event(self, order_event): # see ref.1
        if order_event.status == OrderStatus.FILLED and order_event.is_assignment:
            self.liquidate()

    def _mark_market_open(self):
        self.spx_open = self._spx.price
        self.vix_open = self._vix.price

    def _manage_trade(self):
        if self.portfolio.invested:
            # take profit
            total_holdings_cost = 0.0
            if self.call_spread_order_ticket:
                total_holdings_cost += np.sum([float(self.portfolio[ticket.symbol].holdings_cost) for ticket in self.call_spread_order_ticket])
            if self.put_spread_order_ticket:
                total_holdings_cost += np.sum([float(self.portfolio[ticket.symbol].holdings_cost) for ticket in self.put_spread_order_ticket])
            if total_holdings_cost == 0:
                pass # bad/no data?
            else:
                total_unrealized_profit_ratio = self.portfolio.total_unrealised_profit/(-1*total_holdings_cost)
                if total_unrealized_profit_ratio > 0.99:
                    self.liquidate()
                    self.call_spread_order_ticket = None 
                    self.put_spread_order_ticket = None

            # otherwise 1x net stop per side
            if self.call_spread_order_ticket is not None: # see ref.2
                holdings_cost = np.sum([self.portfolio[ticket.symbol].holdings_cost for ticket in self.call_spread_order_ticket])
                holdings_value = np.sum([self.portfolio[ticket.symbol].holdings_value for ticket in self.call_spread_order_ticket])
                unrealized_profit = np.sum([self.portfolio[ticket.symbol].unrealized_profit for ticket in self.call_spread_order_ticket])
                if holdings_cost == 0.0:
                    pass # bad/no data?
                else:
                    unrealized_profit_ratio = unrealized_profit/(-1*holdings_cost)
                    if unrealized_profit_ratio < -1.95:
                        for ticket in self.call_spread_order_ticket:
                            self.liquidate(ticket.symbol)

            if self.put_spread_order_ticket is not None:
                holdings_cost = np.sum([self.portfolio[ticket.symbol].holdings_cost for ticket in self.put_spread_order_ticket])
                holdings_value = np.sum([self.portfolio[ticket.symbol].holdings_value for ticket in self.put_spread_order_ticket])
                unrealized_profit = np.sum([self.portfolio[ticket.symbol].unrealized_profit for ticket in self.put_spread_order_ticket])
                if holdings_cost == 0.0:
                    pass # bad/no data?
                else:
                    unrealized_profit_ratio = unrealized_profit/(-1*holdings_cost)
                    if unrealized_profit_ratio < -1.95:
                        for ticket in self.put_spread_order_ticket:
                            self.liquidate(ticket.symbol)

    def _close_trade(self):
        if self.portfolio.invested:
            self.liquidate()
            self.call_spread_order_ticket = None 
            self.put_spread_order_ticket = None

    def _open_trade(self):
        self.call_spread_order_ticket = None
        self.put_spread_order_ticket = None

        if not self.portfolio.invested:

            chain = self.current_slice.option_chains.get(self._spxw.symbol, None)
            if not chain: return

            expiry = min([x.expiry for x in chain])

            puts = [i for i in chain if i.expiry == expiry and i.right == OptionRight.PUT]
            if len(puts) == 0: return

            calls = [i for i in chain if i.expiry == expiry and i.right == OptionRight.CALL]
            if len(calls) == 0: return
            
            puts = [x for x in puts if x.strike < self._spx.price]
            short_put_strike = sorted(puts, key=lambda x: abs(x.ask_price - 2.0))[0].strike
            long_put_strike = sorted(puts, key=lambda x: abs(x.ask_price - 0.5))[0].strike

            calls = [x for x in calls if x.strike > self._spx.price]
            short_call_strike = sorted(calls, key=lambda x: abs(x.ask_price - 2.0))[0].strike
            long_call_strike = sorted(calls, key=lambda x: abs(x.ask_price - 0.5))[0].strike

            if not long_put_strike < short_put_strike < short_call_strike < long_call_strike:
                return

            quantity = 1
            strategy = OptionStrategies.bear_call_spread(
                self._spxw.symbol,short_call_strike,long_call_strike,
                expiry
            )
            self.call_spread_order_ticket = self.order(strategy, quantity)

            strategy = OptionStrategies.bull_put_spread(
                self._spxw.symbol,short_put_strike,long_put_strike,
                expiry
            )
            self.put_spread_order_ticket = self.order(strategy, quantity)


"""

ref 1. order cleanup "order_event.is_assignment": https://www.quantconnect.com/research/17882/trading-volatility-with-options/p1

ref 2. manage multi-leg "self.call_spread_order_ticket" : https://www.quantconnect.com/forum/discussion/11359/tracking-multi-legged-option-positions/

ref 3. get 0dte with symbol `SPXW`, filters `weeklys_only`, `expiration`  https://www.quantconnect.com/docs/v2/writing-algorithms/universes/index-options

ref 4. "By 2022, Cboe had listed an SPX Weeklys option with an expiration for each day of the week (Monday through Friday)" https://www.cboe.com/insights/posts/the-evolution-of-same-day-options-trading

"""
