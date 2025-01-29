# py-algo-example
Example Python algorithm that is integrated into TradeBot. This Python algorithm is just a simple algortithm that uses EMA crossovers to send a buy and sell signals. The EMA periods are set as runtime parameters. It will calculate the EMAs and whenever there is a crossover, it will advise to BUY or SELL accordingly. NOTE: This is a simple algo just used as an example and should be not be used in practice. 

TradeBot uses pyo3 to execute the python code. Integration and execution of this Python algoirthm can be found here:

https://github.com/sayedrasheed/tradebot-rs/blob/master/algo-service/src/py_algo/py_algo.rs

Currently, TradeBot includes this python example as a submodule to get the python source code and handles all the python execution at runtime. I believe a better way of doing this is changing this repo be a crate that wraps the pyo3 usage and TradeBot will add just the crate. However, doing it this way we will need to create a python package of the algorithm code that TradeBot will need to pip install since it needs it at runtime.

# Installation
1. Download and install [Python]([https://cmake.org/download/](https://www.python.org/downloads/))
2. Download and install [Rust](https://www.rust-lang.org/tools/install). The version I use is 1.85.0
3. This Python algo uses the TA-Lib. So C library TA-Lib so that needs to be installed. Follow these instructions [here](https://ta-lib.org/install/). Then need to pip install TA-Lib

# Usage
Algorithm is executed via a generic AlgoInterface which all algorithms will implement. The interface file can be found [here](https://github.com/sayedrasheed/py-algo-example/blob/master/algo_interface.py)

The AlgoParams struct is designed to contain runtime parameters that each Algo can have. These parameters are set in TradeBot via a yaml file then passed into this Algo via the AlgoParams struct. See how that is done here:

https://github.com/sayedrasheed/tradebot-rs/blob/master/algo-service/src/py_algo/py_algo.rs#L227

There are 3 execution entry points into the algo via the AlgoInterface.
1. [tick_update](https://github.com/sayedrasheed/py-algo-example/blob/master/algo_interface.py#L62)
2. [candle_update](https://github.com/sayedrasheed/py-algo-example/blob/master/algo_interface.py#L66)
3. [historical_data_update](https://github.com/sayedrasheed/py-algo-example/blob/master/algo_interface.py#L77)

Each one of these functions will have their own input and output that needs to be defined by the algo. If your algo doesn't use any of the functions then you can stub them out.

These functions will then be called by TradeBot any time the node receives the corressponding message. See here for the PyAlgo candle_update execution:

https://github.com/sayedrasheed/tradebot-rs/blob/master/algo-service/src/py_algo/py_algo.rs#L322

# Demo
See video for an example of this algorithm running in TradeBot:
[Youtube](https://www.youtube.com/shorts/MzAcaJlIPCU)
