import queue

from data import HistoricCSVDataHandler
from strategy import MovingAverageCrossStrategy
from portfolio import Portfolio
from execution import SimulatedExecutionHandler
import performance


class Backtest:
    def __init__(self, csv_dir, symbol_list, initial_capital, start_date,
                 data_handler, execution_handler, portfolio, strategy):
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.initial_capital = initial_capital
        self.start_date = start_date

        self.events = queue.Queue()

        # one shared queue handed to every component
        self.data = data_handler(self.events, self.csv_dir, self.symbol_list)
        self.strategy = strategy(self.data, self.events)
        self.portfolio = portfolio(self.data, self.events, self.start_date, self.initial_capital)
        self.execution = execution_handler(self.data, self.events)

    def _run_backtest(self):
        while self.data.continue_backtest:
            self.data.update_bars()
            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                if event.type == 'MARKET':
                    self.strategy.calculate_signals(event)
                    self.portfolio.update_timeindex(event)
                elif event.type == 'SIGNAL':
                    self.portfolio.update_signal(event)
                elif event.type == 'ORDER':
                    self.execution.execute_order(event)
                elif event.type == 'FILL':
                    self.portfolio.update_fill(event)

    def _output_performance(self):
        curve = self.portfolio.create_equity_curve_dataframe()

        total_return = curve['equity_curve'].iloc[-1]
        returns = curve['returns']
        sharpe = performance.create_sharpe_ratio(returns)
        max_dd, dd_duration = performance.create_drawdowns(curve['equity_curve'])

        print(f"Total Return: {(total_return - 1.0) * 100.0:.2f}%")
        print(f"Sharpe Ratio: {sharpe:.2f}")
        print(f"Max Drawdown: {max_dd * 100.0:.2f}%")
        print(f"Drawdown Duration: {dd_duration}")
        print(f"Signals/Trades fired: {len(self.portfolio.all_holdings)} bars recorded")

    def simulate_trading(self):
        self._run_backtest()
        self._output_performance()