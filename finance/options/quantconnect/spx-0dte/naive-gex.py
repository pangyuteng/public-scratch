# source:
# https://www.reddit.com/r/algotrading/comments/1niqfdr/sharing_gamma_exposure_calculator_useful_for_0dte

from AlgorithmImports import *
import json
from collections import defaultdict

class GammaExposureAlgorithm(QCAlgorithm):
    
    def initialize(self):
        self.set_start_date(2026, 1, 2)
        self.set_end_date(2026, 1, 2)
        self.set_cash(100000)
        self.universe_settings.resolution = Resolution.MINUTE
        
        self._spx = self.add_index("SPX")
        self._spxw = self.add_index_option(self._spx.symbol, "SPXW")
        self._spxw.set_filter(lambda x: x.weeklys_only().strikes(-100, 100).expiration(0, 7))
        
        self.schedule.On(self.date_rules.every_day(), self.time_rules.at(10, 30), self.calculate_gex)
        self.object_store_key = f"gex_test_{self.time.strftime('%Y%m%d')}"
        
    def OnData(self, data):
        pass
    
    def calculate_gex(self):
        spot = self._spx.price
        if spot == 0:
            self.log("ERROR: No SPX price")
            return
            
        chains = self.current_slice.option_chains.get(self._spxw.symbol, None)
        if not chains: return
                
        gex_data = defaultdict(lambda: {'call_gex': 0, 'put_gex': 0, 'total_gex': 0})
        total_gex = contracts = 0
        today = self.time.date()
        
        for c in chains:

            if c.expiry.date() != today or not c.greeks or c.greeks.gamma == 0:
                continue

            strike = float(c.strike)
            gamma = c.greeks.gamma
            #oi = getattr(c, 'OpenInterest', None) or c.Volume or 1000
            oi = c.open_interest
            
            contract_gex = gamma * oi * 100 * (spot ** 2)
            adjusted_gex = -contract_gex if c.right == OptionRight.CALL else contract_gex
            
            if c.right == OptionRight.CALL:
                gex_data[strike]['call_gex'] += adjusted_gex
            else:
                gex_data[strike]['put_gex'] += adjusted_gex
                
            gex_data[strike]['total_gex'] += adjusted_gex
            total_gex += adjusted_gex
            contracts += 1
    
        self.log(f"SPX: {spot}, Contracts: {contracts}, Total GEX: ${total_gex:,.0f}")
        self.export_data(gex_data, spot, total_gex)
        
    def export_data(self, gex_data, spot, total_gex):
        strikes = sorted(gex_data.keys())
        
        export_data = {
            'metadata': {
                'timestamp': self.time.isoformat(),
                'spot_price': float(spot),
                'total_gamma_exposure': float(total_gex),
                'num_strikes': len(strikes)
            },
            'strike_data': [{
                'strike': float(s),
                'total_gex': float(gex_data[s]['total_gex']),
                'call_gex': float(gex_data[s]['call_gex']),
                'put_gex': float(gex_data[s]['put_gex']),
                'distance_from_spot': float(s - spot)
            } for s in strikes]
        }
        
        try:
            success = self.object_store.save(self.object_store_key, json.dumps(export_data))
            self.log(f"{'✓' if success else '✗'} Export: {len(strikes)} strikes")
        except Exception as e:
            self.log(f"Export error: {e}")
            
        # Log top 3 GEX strikes
        top_strikes = sorted(gex_data.items(), key=lambda x: abs(x[1]['total_gex']), reverse=True)[:3]
        for i, (strike, data) in enumerate(top_strikes):
            self.log(f"{i+1}. {strike}: ${data['total_gex']:,.0f}")

    def on_end_of_algorithm(self):
        self.log(f"Complete. ObjectStore key: {self.object_store_key}")


# research.ipynb
"""
# Single cell execution for QuantConnect Gamma Exposure visualization
from QuantConnect.Research import *
from QuantConnect import *
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configure matplotlib
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 12

# Initialize QuantConnect Research
qb = QuantBook()

# Load data from ObjectStore
object_store_key = "gex_test_20260102"  # Update date as needed
json_data = qb.ObjectStore.Read(object_store_key)
gamma_data = json.loads(json_data)

# Extract data
metadata = gamma_data['metadata']
spot_price = metadata['spot_price']
total_gex = metadata['total_gamma_exposure']
timestamp = metadata['timestamp']

# Convert to DataFrame and sort
df = pd.DataFrame(gamma_data['strike_data'])
df = pd.DataFrame(gamma_data['strike_data']).sort_values('strike')

# Create chart
fig, ax = plt.subplots(figsize=(16, 10))

strikes = df['strike'].values
gex_values = df['total_gex'].values / 1e9  # Convert to billions
colors = ['#2E8B57' if gex >= 0 else '#DC143C' for gex in gex_values]

# Bar chart
ax.bar(strikes, gex_values, color=colors, alpha=0.8, width=2.5)

# SPX price line
ax.axvline(x=spot_price, color='#4169E1', linestyle='--', linewidth=2, 
           label=f'SPX: {spot_price:,.2f}')

# Formatting
ax.set_xlabel('Strike Price', fontsize=14, fontweight='bold')
ax.set_ylabel('Gamma Exposure (Billions $)', fontsize=14, fontweight='bold')
ax.set_title(f'SPX 0DTE Gamma Exposure by Strike\n{timestamp[:10]} at 10:30 AM EST', 
            fontsize=16, fontweight='bold', pad=20)

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}B'))
ax.set_xlim(strikes.min() - 10, strikes.max() + 10)
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)
ax.legend(loc='upper right', fontsize=12)

# Summary text
textstr = f'Total GEX: ${total_gex/1e9:.2f}B\nStrikes: {len(df)}\nRange: {strikes.min():.0f} - {strikes.max():.0f}'
props = dict(boxstyle='round', facecolor='lightgray', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.show()
"""
