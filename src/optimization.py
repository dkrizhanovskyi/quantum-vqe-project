import pennylane as qml
from pennylane import numpy as np
from circuits import create_vqe_circuit
import logging
import json
import os

def cost_fn(params, circuit_type):
    circuit = create_vqe_circuit(params, circuit_type)
    return circuit()

def optimize_vqe(initial_params, steps=100, stepsize=0.1, circuit_type='default', save_path=None):
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

def save_state(params, cost_history, save_path):
    # Преобразование save_path в абсолютный путь
    save_path = os.path.abspath(save_path)
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    # Преобразование объектов в списки
    state = {
        'params': params.tolist(),
        'cost_history': [cost.item() if isinstance(cost, np.ndarray) else cost for cost in cost_history]
    }
    with open(save_path, 'w') as f:
        json.dump(state, f)
    logging.info(f"State saved to {save_path}")

def load_state(load_path):
    load_path = os.path.abspath(load_path)
    with open(load_path, 'r') as f:
        state = json.load(f)
    params = np.array(state['params'])
    cost_history = state['cost_history']
    logging.info(f"State loaded from {load_path}")
    return params, cost_history
