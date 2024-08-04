import sys
import os
import logging
import argparse
import yaml
from circuits import create_vqe_circuit
from optimization import optimize_vqe, load_state
from analysis import analyze_results
from metrics import calculate_metrics
# from error_handler import send_error_email
import numpy as np

def main(config):
    try:
        # Загрузка состояния, если указан путь
        if config['optimization']['load_path']:
            initial_params, cost_history = load_state(config['optimization']['load_path'])
            logging.info("Continuing optimization from loaded state.")
        else:
            initial_params = np.random.random(2)
        
        # Оптимизация
        optimized_params, cost_history = optimize_vqe(
            initial_params,
            steps=config['optimization']['steps'],
            stepsize=config['optimization']['stepsize'],
            circuit_type=config['optimization']['circuit'],
            save_path=config['optimization']['save_path']
        )
        
        # Анализ результатов
        analyze_results(optimized_params, cost_history)
        
        # Метрики
        metrics = calculate_metrics(cost_history)
        logging.info(f"Optimization metrics: {metrics}")
    
    except Exception as e:
        logging.error("An error occurred during the execution of the script.", exc_info=True)
        # send_error_email("Quantum VQE Project Error", str(e), "recipient_email@example.com")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Quantum VQE Project')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file')

    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)
    
    main(config)
