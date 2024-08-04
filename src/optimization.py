import pennylane as qml
from pennylane import numpy as np
from circuits import create_vqe_circuit
import logging
import json
import os
from typing import List, Tuple, Union

def cost_fn(params: Union[List[float], np.ndarray], circuit_type: str) -> float:
    """
    Calculate the cost function for the given parameters and circuit type.

    Args:
        params: A list or NumPy array of float numbers representing the parameters for the quantum circuit.
        circuit_type: A string indicating the type of the circuit.

    Returns:
        The calculated cost as a float.
    """
    circuit = create_vqe_circuit(params, circuit_type)
    return circuit()

def optimize_vqe(initial_params: Union[List[float], np.ndarray], steps: int = 100, stepsize: float = 0.1, circuit_type: str = 'default', save_path: str = None) -> Tuple[np.ndarray, List[float]]:
    """
    Optimize the VQE circuit parameters using gradient descent.

    Args:
        initial_params: A list or NumPy array of float numbers representing the initial parameters for the quantum circuit.
        steps: An integer representing the number of optimization steps.
        stepsize: A float representing the step size for the gradient descent optimizer.
        circuit_type: A string indicating the type of the circuit.
        save_path: A string representing the path to save the optimization state.

    Returns:
        A tuple containing the optimized parameters and the cost history.
    """
    params = np.array(initial_params, requires_grad=True)
    opt = qml.GradientDescentOptimizer(stepsize=stepsize)
    cost_history = []

    logging.info("Starting optimization...")
    for i in range(steps):
        params, cost = opt.step_and_cost(lambda p: cost_fn(p, circuit_type), params)
        cost_history.append(cost)
        if (i + 1) % 10 == 0:
            logging.info(f"Step {i+1}, Cost: {cost:.4f}")
            if save_path:
                save_state(params, cost_history, save_path)
    
    logging.info("Optimization finished.")
    return params, cost_history

def save_state(params: np.ndarray, cost_history: List[float], save_path: str) -> None:
    """
    Save the optimization state to a file.

    Args:
        params: A NumPy array of float numbers representing the optimized parameters for the quantum circuit.
        cost_history: A list of float numbers representing the cost history during optimization.
        save_path: A string representing the path to save the optimization state.

    Returns:
        None
    """
    save_path = os.path.abspath(save_path)
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    state = {
        'params': params.tolist(),
        'cost_history': [cost.item() if isinstance(cost, np.ndarray) else cost for cost in cost_history]
    }
    with open(save_path, 'w') as f:
        json.dump(state, f)
    logging.info(f"State saved to {save_path}")

def load_state(load_path: str) -> Tuple[np.ndarray, List[float]]:
    """
    Load the optimization state from a file.

    Args:
        load_path: A string representing the path to load the optimization state.

    Returns:
        A tuple containing the loaded parameters and the cost history.
    """
    load_path = os.path.abspath(load_path)
    with open(load_path, 'r') as f:
        state = json.load(f)
    params = np.array(state['params'])
    cost_history = state['cost_history']
    logging.info(f"State loaded from {load_path}")
    return params, cost_history
