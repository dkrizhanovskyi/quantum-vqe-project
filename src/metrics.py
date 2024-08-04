import numpy as np

def mean_absolute_error(cost_history):
    return np.mean(np.abs(cost_history))

def mean_squared_error(cost_history):
    return np.mean(np.square(cost_history))

def final_cost(cost_history):
    return cost_history[-1]

def calculate_statistics(cost_history):
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

def calculate_metrics(cost_history):
    metrics = {
        'MAE': mean_absolute_error(cost_history),
        'MSE': mean_squared_error(cost_history),
        'Final Cost': final_cost(cost_history)
    }
    metrics.update(calculate_statistics(cost_history))
    return metrics
