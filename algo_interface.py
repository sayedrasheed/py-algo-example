
import sys
import os
sys.path.append(os.path.dirname(__file__))

import py_algo

# Algo parameters entry point, fill in algo params here
class AlgoParams:
    def __init__(self, ema_slow_period: int,  ema_fast_period: int, candle_period: int):
        self.ema_slow_period = ema_slow_period
        self.ema_fast_period = ema_fast_period
        self.candle_period = candle_period

# Input to tick handler, fill in desired input, if any
class TickInput:
    def __init__(self):
        pass

# Output from tick handler, fill in algo output from a tick message, if any
class TickOutput:
    def __init__(self):
        pass

# Input to candle handler, fill in desired input, if any
class CandleInput:
    def __init__(self, timestamp_ns: int = 0, period_s: int = 0, close: float = 0):
        self.timestamp_ns = timestamp_ns
        self.period_s = period_s
        self.close = close

# Output from candle handler, fill in algo output from a candle message, if any
class CandleOutput:
    def __init__(self, advice: py_algo.PyAdvice = None, slow_ema: py_algo.PyEma = None, fast_ema: py_algo.PyEma = None):
        self.advice = advice
        self.slow_ema = slow_ema
        self.fast_ema = fast_ema

# Input to historical data handler, fill in desired input, if any
class HistoricalDataInput:
    def __init__(self, period_s: int = 0, candles: list = []):
        self.period_s = period_s
        self.candles = candles

# Output from historical data handler, fill in algo output from a historical data message, if any
class HistoricalDataOutput:
    def __init__(self, period_s: int = 0, slow_ema: list = [], fast_ema: list = []):
        self.period_s = period_s
        self.slow_ema = slow_ema
        self.fast_ema = fast_ema

# Algo interface entry point, fill in algo interface here
class AlgoInterface:
    def __init__(self, params: AlgoParams):
        self.ema_slow_period = params.ema_slow_period
        self.ema_fast_period = params.ema_fast_period
        self.candle_period = params.candle_period

        self.py_algo = py_algo.PyAlgo(self.ema_slow_period, self.ema_fast_period, self.candle_period)

    # Tick handler
    def tick_update(self, tick: TickInput, output: TickOutput):
        pass
    
    # Candle handler
    def candle_update(self, candle: CandleInput, output: CandleOutput):
        # Convert input provided by rust into PyAlgo input
        # Call PyAlgo cndle dhandler
        advice = self.py_algo.handle_candle(candle.period_s, py_algo.PyCandle(candle.timestamp_ns, candle.close))

        # Fill in PyAlgo output from a Candle message
        output.slow_ema = self.py_algo.get_ema_val(self.ema_slow_period)
        output.fast_ema = self.py_algo.get_ema_val(self.ema_fast_period)
        output.advice = advice

    # Historical Data handler
    def historical_data_update(self, historical_data: HistoricalDataInput, output: HistoricalDataOutput):
        # Convert input provided by rust into PyAlgo input
        candles = []
        for candle in historical_data.candles:
            candles.append(py_algo.PyCandle(candle['timestamp_ns'], candle['close']))

        # Call PyAlgo historical data handler
        self.py_algo.handle_historical_data(historical_data.period_s, candles)

        # Fill in PyAlgo output from a HistoricalData message
        output.period_s = historical_data.period_s
        output.slow_ema = self.py_algo.get_ema_line(self.ema_slow_period)
        output.fast_ema = self.py_algo.get_ema_line(self.ema_fast_period)
