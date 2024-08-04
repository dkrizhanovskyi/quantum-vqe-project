import sys
import os
import logging
import argparse
import yaml
import multiprocessing
from typing import Dict, Any, List, Tuple, Union
from circuits import create_vqe_circuit
from optimization import optimize_vqe, load_state
from analysis import analyze_results
from quantum_metrics import calculate_metrics
# from error_handler import send_error_email
import numpy as np

def parallel_optimize_vqe(params_list: List[Union[List[float], np.ndarray]], steps: int, stepsize: float, circuit_type: str) -> List[Tuple[np.ndarray, List[float]]]:
    """
    Optimize VQE circuits in parallel.

    Args:
        params_list: A list of initial parameters for the quantum circuits.
        steps: An integer representing the number of optimization steps.
        stepsize: A float representing the step size for the gradient descent optimizer.
        circuit_type: A string indicating the type of the circuit.

    Returns:
        A list of tuples containing optimized parameters and cost history for each set of initial parameters.
    """
    logging.info("Starting parallel optimization...")
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.starmap(optimize_vqe, [(params, steps, stepsize, circuit_type) for params in params_list])
    pool.close()
    pool.join()
    logging.info("Parallel optimization completed.")
    return results

def parallel_analyze_results(results: List[Tuple[np.ndarray, List[float]]], results_dir: str) -> None:
    """
    Analyze optimization results in parallel.

    Args:
        results: A list of tuples containing optimized parameters and cost history.
        results_dir: The directory to save the analysis results.

    Returns:
        None
    """
    logging.info("Starting parallel analysis...")
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.starmap(analyze_results, [(params, cost_history) for params, cost_history in results])
    pool.close()
    pool.join()
    logging.info("Parallel analysis completed.")

def main(config: Dict[str, Any]) -> None:
    """
    Main function to execute the quantum VQE optimization project.

    Args:
        config: A dictionary containing configuration parameters.

    Returns:
        None
    """
    try:
        logging.info("Starting main function...")
        parallel_processes = config.get('parallel_processes', multiprocessing.cpu_count())
        logging.info(f"Using {parallel_processes} parallel processes.")

        # Загрузка состояния, если указан путь
        if config['optimization']['load_path']:
            initial_params, cost_history = load_state(config['optimization']['load_path'])
            logging.info("Continuing optimization from loaded state.")
            params_list = [initial_params]
        else:
            params_list = [np.random.random(2) for _ in range(parallel_processes)]
            logging.info(f"Initialized {parallel_processes} sets of random initial parameters.")
        
        # Параллельная оптимизация
        results = parallel_optimize_vqe(
            params_list,
            steps=config['optimization']['steps'],
            stepsize=config['optimization']['stepsize'],
            circuit_type=config['optimization']['circuit']
        )

        # Параллельный анализ результатов
        parallel_analyze_results(results, config['results_dir'])
        logging.info("Main function completed successfully.")
    
    except Exception as e:
        logging.error("An error occurred during the execution of the script.", exc_info=True)
        # send_error_email("Quantum VQE Project Error", str(e), "recipient_email@example.com")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Quantum VQE Project')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file')

    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    with open(args.config, 'r', encoding='utf-8') as file:  # Добавлено указание кодировки
        config = yaml.safe_load(file)
    
    main(config)
