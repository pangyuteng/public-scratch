
from AlgorithmImports import *

class VolatilityTradingOptionAlgorithm(QCAlgorithm):

    def initialize(self):

        self.set_start_date(2024, 1, 1)
        self.set_end_date(2024, 12, 31)
        
        self.set_cash(200000)

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
        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.after_market_open(self._spx.symbol, 30), self._open_trade)
        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.every(timedelta(minutes=1)),self._manage_trade)
        self.schedule.on(self.date_rules.every_day(self._spxw.symbol), self.time_rules.before_market_close(self._spx.symbol, 1),self._close_trade)

    def option_filter(self, universe):
        return universe.expiration(0, 0).weeklys_only()

    def _mark_market_open(self):
        self.spx_open = self._spx.price
        self.vix_open = self._vix.price

    def _manage_trade(self):
        if self.portfolio.invested and self.portfolio.total_unrealised_profit > 0.4:
            self.liquidate()

    def _close_trade(self):
        if self.portfolio.invested:
            self.liquidate()

    def _open_trade(self):

        if not self.portfolio.invested:

            chain = self.current_slice.option_chains.get(self._spxw.symbol, None)
            if not chain: return

            expiry = min([x.expiry for x in chain])

            puts = [i for i in chain if i.expiry == expiry and i.right == OptionRight.PUT]
            if len(puts) == 0: return

            calls = [i for i in chain if i.expiry == expiry and i.right == OptionRight.CALL]
            if len(calls) == 0: return
            
            puts = [x for x in puts if x.strike < self._spx.price]
            short_put_strike = sorted(puts, key=lambda x: abs(x.greeks.delta - 0.15*-1))[0].strike
            long_put_strike = sorted(puts, key=lambda x: abs(x.greeks.delta - 0.10*-1))[0].strike

            calls = [x for x in calls if x.strike > self._spx.price]
            short_call_strike = sorted(calls, key=lambda x: abs(x.greeks.delta - 0.15))[0].strike
            long_call_strike = sorted(calls, key=lambda x: abs(x.greeks.delta - 0.10))[0].strike

            if not long_put_strike < short_put_strike < short_call_strike < long_call_strike:
                return

            quantity = 1
            strategy = OptionStrategies.iron_condor(
                self._spxw.symbol,
                long_put_strike,short_put_strike,short_call_strike,long_call_strike,
                expiry
            )
            self.order(strategy, quantity)

    def on_order_event(self, order_event):
        if order_event.status == OrderStatus.FILLED and order_event.is_assignment:
            self.liquidate()
