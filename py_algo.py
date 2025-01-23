
import numpy as np
import talib

# EMA output from PyAlgo
class PyEma:
    def __init__(self, timestamp_ns: int, value: float):
        self.timestamp_ns = timestamp_ns
        self.value = value

# Candle input for PyAlgo
class PyCandle:
    def __init__(self, timestamp_ns: int, close: float):
        self.timestamp_ns = timestamp_ns
        self.close = close
# Advice from PyAlgo
class PyAdvice:
    def __init__(self, timestamp_ns: int, price: float, size: int, is_valid: bool):
        self.timestamp_ns = timestamp_ns
        self.price = price
        self.size = size
        self.is_valid = is_valid
        
# Main PyAlgo class for algo execution
class PyAlgo:
    def __init__(self, ema_slow_period: int,  ema_fast_period: int, candle_period: int):
        self.ema_slow_period = ema_slow_period
        self.ema_fast_period = ema_fast_period
        self.candle_period = candle_period
        self.emas = { self.ema_slow_period: [], self.ema_fast_period: []}
        self.candles = []
        self.candle_closes = []
        self.long_position = False
        self.slow_less_fast_count = 0

    def handle_candle(self, period_s: int, candle: PyCandle):
        if self.candle_period == period_s:
            self.candles.append(candle)
            self.candle_closes.append(candle.close)

            self.ema_slow = talib.EMA(np.array(self.candle_closes), timeperiod=self.ema_slow_period)
            self.ema_fast = talib.EMA(np.array(self.candle_closes), timeperiod=self.ema_fast_period)

            if not self.long_position:
                if self.ema_slow[-1] < self.ema_fast[-1]:
                    self.slow_less_fast_count += 1
                else:
                    if self.slow_less_fast_count >= 25:
                        self.long_position = True
                        self.slow_less_fast_count = 0
                        return PyAdvice(candle.timestamp_ns, candle.close, 1, True)
                    
                    self.slow_less_fast_count = 0
            else:
                if self.ema_slow[-1] < self.ema_fast[-1]:
                    self.long_position = False
                    return PyAdvice(candle.timestamp_ns, candle.close, -1, True)

        return PyAdvice(0, 0, 0, False)

    def handle_historical_data(self, period_s: int, hd: list):
        if period_s == self.candle_period:
            for candle in hd:
                self.candles.append(candle)
                self.candle_closes.append(candle.close)

            self.ema_slow = talib.EMA(np.array(self.candle_closes), timeperiod=self.ema_slow_period)
            self.ema_fast = talib.EMA(np.array(self.candle_closes), timeperiod=self.ema_fast_period)

    def get_ema_val(self, ema_period):
        if ema_period == self.ema_slow_period:
            return PyEma(self.candles[-1].timestamp_ns, self.ema_slow[-1])
        else:
            return PyEma(self.candles[-1].timestamp_ns, self.ema_fast[-1])
        
    def get_ema_line(self, ema_period):
        ema_list = []
        if ema_period == self.ema_slow_period:
            slow_ema = self.ema_slow.tolist()
            for i, ema in enumerate(slow_ema):
                ema_list.append(PyEma(self.candles[i].timestamp_ns, ema))
        else:
            fast_ema = self.ema_fast.tolist()
            for i, ema in enumerate(fast_ema):
                ema_list.append(PyEma(self.candles[i].timestamp_ns, ema))

        return ema_list

    

    

    