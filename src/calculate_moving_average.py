import numpy as np
from typing import List

def calculate_moving_average(data: List[float], window_size: int) -> np.ndarray:
    """
    Calculate the moving average of a given list of numbers.

    Args:
        data: A list of float numbers representing the data.
        window_size: An integer representing the size of the moving window.

    Returns:
        A NumPy array containing the moving averages.
    """
    if window_size <= 0:
        raise ValueError("Window size must be greater than 0")
    if window_size > len(data):
        raise ValueError("Window size must not be greater than the length of the data")
    
    return np.convolve(data, np.ones(window_size), 'valid') / window_size
