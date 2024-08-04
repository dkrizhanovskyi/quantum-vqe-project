# Quantum VQE Project

This project implements a Variational Quantum Eigensolver (VQE) using PennyLane and NumPy. The project includes modules for creating quantum circuits, optimizing parameters, calculating metrics, and analyzing results.

## Project Structure

```
/quantum-vqe-project
├── src
│   ├── calculate_moving_average.py
│   ├── circuits.py
│   ├── main.py
│   ├── metrics.py
│   ├── optimization.py
├── config.yaml
├── README.md
└── LICENSE
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dkrizhanovskyi/quantum-vqe-project.git
   cd quantum-vqe-project
   ```

2. Create a virtual environment and install the dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

1. Configure the project by editing `config.yaml` to set the optimization parameters, circuit type, and other options.

2. Run the main script:
   ```bash
   python src/main.py --config config.yaml
   ```

## Configuration

The `config.yaml` file contains configuration settings for the optimization process. Example:

```yaml
optimization:
  steps: 100
  stepsize: 0.1
  circuit: "default"
  save_path: results/state.json
  load_path: ''
```

## Project Modules

### calculate_moving_average.py
Contains the function to calculate the moving average of a given data series.

### circuits.py
Defines quantum circuits used for the VQE algorithm. It includes functions to create different types of circuits.

### main.py
The main script to run the VQE optimization. It loads configurations, performs optimization, analyzes results, and calculates metrics.

### metrics.py
Provides functions to calculate various metrics and statistics from the cost history of the optimization process.

### optimization.py
Includes functions to perform the VQE optimization, save and load states.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
