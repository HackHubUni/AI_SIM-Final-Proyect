# This file will contain a class that will generate statistics from the Registry class of the simulation
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable
from statistics import variance, mean

from registers import *
from simulation_engine import InventorySimulation


class StatisticsResults:
    def __init__(
        self,
        loss_expectation: float,
        costs_expectation: float,
        final_balance_expectation: float,
        loss_variance: float,
        costs_variance: float,
        final_balance_variance: float,
    ) -> None:
        self.loss_expectation: float = loss_expectation
        self.costs_expectation: float = costs_expectation
        self.final_balance_expectation: float = final_balance_expectation
        self.loss_variance: float = loss_variance
        self.costs_variance: float = costs_variance
        self.final_balance_variance: float = final_balance_variance


def calculate_sell_loss(sells: list[SellRecord]):
    demand = 0
    sold = 0
    for sell in sells:
        demand += sell.amount_asked
        sold += sell.amount_sold
    return demand - sold


class SimStatistics:
    """This class extracts statistics from a simulation"""

    def __init__(self, simulation: InventorySimulation) -> None:
        self.simulation: InventorySimulation = simulation
        self.flat_registry: FlattenRegistry = FlattenRegistry(simulation.registry)

    def calculate_statistics_results(self, number_of_runs: int = 40):
        balance = []
        costs = []
        loss = []
        for _ in range(number_of_runs):
            self.simulation.run()
            sim = self.simulation
            self.flat_registry = FlattenRegistry(sim.registry)
            sim_loss: tuple[list[int], list[float]] = self.get_sells_data(
                lambda sells: sim.product_value * calculate_sell_loss(sells)
            )
            sim_balance: float = sim.actual_balance
            sim_inventory_costs: tuple[list[int], list[float]] = self.get_pay_hold_data(
                lambda pay_record: pay_record.cost
            )
            sim_supply_costs: tuple[list[int], list[float]] = self.get_buy_data(
                lambda buy_record: buy_record.cost
            )

            loss.append(sum(sim_loss[1]))
            balance.append(sim_balance)
            costs.append(sum(sim_inventory_costs[1]) + sum(sim_supply_costs[1]))
        results = StatisticsResults(
            loss_expectation=mean(loss),
            costs_expectation=mean(costs),
            final_balance_expectation=mean(balance),
            loss_variance=variance(loss),
            costs_variance=variance(costs),
            final_balance_variance=variance(balance),
        )
        return results

    def give_fitness(self):
        """Fitness useful for optimization"""
        sells: list[tuple[int, list[SellRecord]]] = self.flat_registry.flat_sells
        hold_costs: list[tuple[int, PayHoldingRecord]] = (
            self.flat_registry.flat_pay_holding
        )
        buy_costs: list[tuple[int, BuyRecord]] = self.flat_registry.flat_buy

        total_loss = 0
        for _, sell in sells:
            loss = sum(map(lambda x: x.amount_asked - x.amount_sold, sell))
            total_loss += loss
        total_hold_cost = sum(map(lambda t: t[1].cost, hold_costs))
        total_buy_cost = sum(map(lambda t: t[1].amount, buy_costs))
        return 3 * total_loss + total_buy_cost + 2 * total_hold_cost

    def get_sells_data(
        self, process_function: Callable[[list[SellRecord]], float]
    ) -> tuple[list[int], list[float]]:
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the sells at that time.
        The 'process function' is a function that receives a list of SellsRecords and return some float representing statistic information of that list of sales
        """
        return SimStatistics.get_data(self.flat_registry.flat_sells, process_function)

    def get_buy_data(self, process_function: Callable[[BuyRecord], float]):
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the BuyRecord at that time.
        The 'process function' is a function that receives a single BuyRecord and return some float representing statistic information about it
        """
        return SimStatistics.get_data(self.flat_registry.flat_buy, process_function)

    def get_stock_data(self, process_function: Callable[[StockRecord], float]):
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the StockRecord at that time.
        The 'process function' is a function that receives a single StockRecord and return some float representing statistic information about it
        """
        return SimStatistics.get_data(self.flat_registry.flat_stock, process_function)

    def get_balance_data(self, process_function: Callable[[BalanceRecord], float]):
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the BalanceRecord at that time.
        The 'process function' is a function that receives a single BalanceRecord and return some float representing statistic information about it
        """
        return SimStatistics.get_data(self.flat_registry.flat_balance, process_function)

    def get_pay_hold_data(self, process_function: Callable[[PayHoldingRecord], float]):
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the PayHoldingRecord at that time.
        The 'process function' is a function that receives a single PayHoldingRecord and return some float representing statistic information about it
        """
        return SimStatistics.get_data(
            self.flat_registry.flat_pay_holding, process_function
        )

    @staticmethod
    def get_data[
        T
    ](raw_data: list[tuple[int, T]], process_function: Callable[[T], float]) -> tuple[
        list[int], list[float]
    ]:
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the elements of data in the raw_data input.
        The 'process_function' is a function that receives some value and computes some float representing statistic information about the value
        """
        time: list[int] = []
        values: list[float] = []

        for t, val in raw_data:
            time.append(t)
            values.append(process_function(val))
        return time, values

class FlattenRegistry:
    def __init__(self, registry: Registry) -> None:
        self.registry: Registry = registry
        self.flat_sells: list[tuple[int, list[SellRecord]]] = self.flat_sells_registry()
        self.flat_stock: list[tuple[int, StockRecord]] = self.flat_stock_registry()
        self.flat_buy: list[tuple[int, BuyRecord]] = self.flat_buy_registry()
        self.flat_balance: list[tuple[int, BalanceRecord]] = (
            self.flat_balance_registry()
        )
        self.flat_pay_holding: list[tuple[int, PayHoldingRecord]] = (
            self.flat_pay_holding_registry()
        )

    def flat_sells_registry(self) -> list[tuple[int, list[SellRecord]]]:
        """Returns a sorted list of tuples where the first element is the time in which a sell
        occurs and the second one is a list of sells at that time"""
        sells: list[tuple[int, list[SellRecord]]] = sorted(
            self.registry.sell_registry.items()
        )
        return sells

    def flat_stock_registry(self) -> list[tuple[int, StockRecord]]:
        """Returns a sorted list of tuples where the first element is the time and the second one
        is a StockRecord"""
        stock: list[tuple[int, StockRecord]] = sorted(
            self.registry.stock_registry.items()
        )
        return stock

    def flat_buy_registry(self) -> list[tuple[int, BuyRecord]]:
        """Returns a sorted list of tuples where the first element is the time and the second one
        is the BuyRecord"""
        buy: list[tuple[int, BuyRecord]] = sorted(self.registry.buy_registry.items())
        return buy

    def flat_balance_registry(self) -> list[tuple[int, BalanceRecord]]:
        """Returns a sorted list of tuples where the first element is the time and the second one
        is a BalanceRecord"""
        balance: list[tuple[int, BalanceRecord]] = sorted(
            self.registry.balance_registry.items()
        )
        return balance

    def flat_pay_holding_registry(self) -> list[tuple[int, PayHoldingRecord]]:
        """Returns a sorted list of tuples where the first element is the time and the second one
        is a PayHoldRecord"""
        pay_holding: list[tuple[int, PayHoldingRecord]] = sorted(
            self.registry.pay_holding_registry.items()
        )
        return pay_holding
