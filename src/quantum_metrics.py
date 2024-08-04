import numpy as np
from typing import List, Dict, Union

def mean_absolute_error(cost_history: List[Union[float, np.ndarray]]) -> float:
    """
    Calculate the mean absolute error of the cost history.

    Args:
        cost_history: A list of cost values from the optimization process.

    Returns:
        The mean absolute error as a float.
    """
    return np.mean(np.abs(cost_history))

def mean_squared_error(cost_history: List[Union[float, np.ndarray]]) -> float:
    """
    Calculate the mean squared error of the cost history.

    Args:
        cost_history: A list of cost values from the optimization process.

    Returns:
        The mean squared error as a float.
    """
    return np.mean(np.square(cost_history))

def final_cost(cost_history: List[Union[float, np.ndarray]]) -> float:
    """
    Retrieve the final cost value from the cost history.

    Args:
        cost_history: A list of cost values from the optimization process.

    Returns:
        The final cost value as a float.
    """
    return cost_history[-1]

def calculate_statistics(cost_history: List[Union[float, np.ndarray]]) -> Dict[str, float]:
    """
    Calculate various statistical metrics for the cost history.

    Args:
        cost_history: A list of cost values from the optimization process.

    Returns:
        A dictionary of statistical metrics.
    """
    cost_history = [cost.item() if isinstance(cost, np.ndarray) else cost for cost in cost_history]
    
    statistics = {
        'Mean': np.mean(cost_history),
        'Median': np.median(cost_history),
        'Standard Deviation': np.std(cost_history),
        'Variance': np.var(cost_history),
        'Minimum': np.min(cost_history),
        'Maximum': np.max(cost_history),
        '10th Percentile': np.percentile(cost_history, 10),
        '25th Percentile': np.percentile(cost_history, 25),
        '75th Percentile': np.percentile(cost_history, 75),
        '90th Percentile': np.percentile(cost_history, 90),
        'Interquartile Range': np.percentile(cost_history, 75) - np.percentile(cost_history, 25),
        'Coefficient of Variation': np.std(cost_history) / np.mean(cost_history) if np.mean(cost_history) != 0 else float('inf')
    }
    return statistics

def calculate_metrics(cost_history: List[Union[float, np.ndarray]]) -> Dict[str, float]:
    """
    Calculate various metrics, including mean absolute error, mean squared error, and other statistical metrics.

    Args:
        cost_history: A list of cost values from the optimization process.

    Returns:
        A dictionary of calculated metrics.
    """
    metrics = {
        'MAE': mean_absolute_error(cost_history),
        'MSE': mean_squared_error(cost_history),
        'Final Cost': final_cost(cost_history)
    }
    metrics.update(calculate_statistics(cost_history))
    return metrics
