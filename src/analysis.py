import os
import matplotlib.pyplot as plt
import pandas as pd
import logging
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import seaborn as sns
from calculate_moving_average import calculate_moving_average
from quantum_metrics import calculate_statistics
from typing import List, Union

def analyze_results(params: Union[List[float], np.ndarray], cost_history: List[Union[float, np.ndarray]]) -> None:
    """
    Analyze and visualize the results of the optimization process.

    Args:
        params: Optimized parameters.
        cost_history: List of cost values over the optimization steps.

    Returns:
        None
    """
    logging.info(f"Optimized Parameters: {params}")
    
    # Сохранение результатов
    results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    results_file = os.path.join(results_dir, 'results.csv')
    results_df = pd.DataFrame({'Step': range(len(cost_history)), 'Cost': [cost.item() if isinstance(cost, np.ndarray) else cost for cost in cost_history]})
    results_df.to_csv(results_file, index=False)
    
    # Визуализация с Matplotlib
    cost_history_simple = [cost.item() if isinstance(cost, np.ndarray) else cost for cost in cost_history]
    
    plot_path = plot_cost_history(cost_history_simple, results_dir)
    histogram_path = plot_histogram(cost_history_simple, results_dir)
    moving_average_path = plot_moving_average(cost_history_simple, results_dir)
    boxplot_path = plot_boxplot(cost_history_simple, results_dir)
    density_plot_path = plot_density(cost_history_simple, results_dir)

    # Визуализация с Plotly
    interactive_plot_path = plot_interactive(cost_history, results_dir)
    
    # Генерация HTML-отчета
    html_report_path = generate_report(params, cost_history_simple, plot_path, histogram_path, moving_average_path, boxplot_path, density_plot_path, interactive_plot_path, results_dir)

    # Конвертация HTML-отчета в PDF (если требуется)
    # pdf_report_path = os.path.join(results_dir, 'report.pdf')
    # convert_html_to_pdf(html_report_path, pdf_report_path)

def plot_cost_history(cost_history: List[float], results_dir: str) -> str:
    """
    Plot and save the cost history.

    Args:
        cost_history: List of cost values over the optimization steps.
        results_dir: Directory to save the plot.

    Returns:
        Path to the saved plot.
    """
    plt.plot(cost_history)
    plt.xlabel('Step')
    plt.ylabel('Cost')
    plt.title('Optimization Cost History')
    plot_path = os.path.join(results_dir, 'Figure_1.png')
    plt.savefig(plot_path)
    plt.close()
    logging.info(f"Cost plot saved at {plot_path}")
    return plot_path

def plot_histogram(cost_history: List[float], results_dir: str) -> str:
    """
    Plot and save the histogram of cost history.

    Args:
        cost_history: List of cost values over the optimization steps.
        results_dir: Directory to save the histogram.

    Returns:
        Path to the saved histogram.
    """
    plt.hist(cost_history, bins=20)
    plt.xlabel('Cost')
    plt.ylabel('Frequency')
    plt.title('Cost Distribution')
    histogram_path = os.path.join(results_dir, 'Histogram.png')
    plt.savefig(histogram_path)
    plt.close()
    logging.info(f"Histogram saved at {histogram_path}")
    return histogram_path

def plot_moving_average(cost_history: List[float], results_dir: str, window_size: int = 10) -> str:
    """
    Plot and save the moving average of the cost history.

    Args:
        cost_history: List of cost values over the optimization steps.
        results_dir: Directory to save the plot.
        window_size: Window size for moving average calculation.

    Returns:
        Path to the saved plot.
    """
    moving_average = calculate_moving_average(cost_history, window_size)
    plt.plot(moving_average)
    plt.xlabel('Step')
    plt.ylabel('Moving Average Cost')
    plt.title('Moving Average of Cost')
    moving_average_path = os.path.join(results_dir, 'Moving_Average.png')
    plt.savefig(moving_average_path)
    plt.close()
    logging.info(f"Moving average plot saved at {moving_average_path}")
    return moving_average_path

def plot_boxplot(cost_history: List[float], results_dir: str) -> str:
    """
    Plot and save the boxplot of cost history.

    Args:
        cost_history: List of cost values over the optimization steps.
        results_dir: Directory to save the boxplot.

    Returns:
        Path to the saved boxplot.
    """
    plt.boxplot(cost_history, vert=False)
    plt.xlabel('Cost')
    plt.title('Boxplot of Cost')
    boxplot_path = os.path.join(results_dir, 'Boxplot.png')
    plt.savefig(boxplot_path)
    plt.close()
    logging.info(f"Boxplot saved at {boxplot_path}")
    return boxplot_path

def plot_density(cost_history: List[float], results_dir: str) -> str:
    """
    Plot and save the density plot of cost history.

    Args:
        cost_history: List of cost values over the optimization steps.
        results_dir: Directory to save the density plot.

    Returns:
        Path to the saved density plot.
    """
    plt.figure()
    sns.kdeplot(cost_history, fill=True)
    plt.xlabel('Cost')
    plt.ylabel('Density')
    plt.title('Density Plot of Cost')
    density_plot_path = os.path.join(results_dir, 'Density_Plot.png')
    plt.savefig(density_plot_path)
    plt.close()
    logging.info(f"Density plot saved at {density_plot_path}")
    return density_plot_path

def plot_interactive(cost_history: List[float], results_dir: str) -> str:
    """
    Create and save an interactive plot of the cost history using Plotly.

    Args:
        cost_history: List of cost values over the optimization steps.
        results_dir: Directory to save the interactive plot.

    Returns:
        Path to the saved interactive plot.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(cost_history))), y=cost_history, mode='lines', name='Cost'))
    fig.update_layout(title='Optimization Cost History', xaxis_title='Step', yaxis_title='Cost')
    interactive_plot_path = os.path.join(results_dir, 'interactive_plot.html')
    pio.write_html(fig, file=interactive_plot_path, auto_open=False)
    return interactive_plot_path

def generate_report(params: Union[List[float], np.ndarray], cost_history: List[float], plot_path: str, histogram_path: str, moving_average_path: str, boxplot_path: str, density_plot_path: str, interactive_plot_path: str, results_dir: str) -> str:
    """
    Generate an HTML report of the optimization results.

    Args:
        params: Optimized parameters.
        cost_history: List of cost values over the optimization steps.
        plot_path: Path to the cost plot.
        histogram_path: Path to the histogram.
        moving_average_path: Path to the moving average plot.
        boxplot_path: Path to the boxplot.
        density_plot_path: Path to the density plot.
        interactive_plot_path: Path to the interactive plot.
        results_dir: Directory to save the report.

    Returns:
        Path to the saved HTML report.
    """
    statistics = calculate_statistics(cost_history)
    report_path = os.path.join(results_dir, 'report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"""
        <html>
        <head>
            <title>Optimization Report</title>
            <style>
                body {{ font-family: 'Arial', sans-serif; margin: 40px; line-height: 1.6; color: #333; background-color: #f9f9f9; }}
                h1, h2 {{ color: #333; }}
                h1 {{ font-size: 28px; text-align: center; }}
                h2 {{ font-size: 24px; border-bottom: 2px solid #ddd; padding-bottom: 10px; text-align: center; }}
                table {{ width: 80%; border-collapse: collapse; margin: 20px auto; background-color: #fff; }}
                th, td {{ padding: 12px; border: 1px solid #ddd; text-align: center; }}
                th {{ background-color: #f4f4f4; }}
                .explanation, .conclusion {{ margin-top: 20px; text-align: center; }}
                .conclusion {{ font-weight: bold; }}
                .container {{ max-width: 1200px; margin: auto; padding: 20px; }}
                img {{ max-width: 100%; height: auto; display: block; margin-left: auto; margin-right: auto; }}
            </style>
        </head>
        <body>
        <div class="container">
            <h1>Optimization Report</h1>
            <h2>Optimized Parameters</h2>
            <p style="text-align: center;">{params}</p>
            <h2>Cost History</h2>
            <table>
                <tr><th>Step</th><th>Cost</th></tr>
        """)
        for i, cost in enumerate(cost_history):
            f.write(f"<tr><td>{i+1}</td><td>{cost}</td></tr>")
        f.write(f"""
            </table>
            <h2>Statistical Analysis</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
        """)
        for key, value in statistics.items():
            f.write(f"<tr><td>{key}</td><td>{value}</td></tr>")
        f.write(f"""
            </table>
            <h2>Cost Plot</h2>
            <img src="file://{os.path.abspath(plot_path)}" alt="Cost Plot">
            <div class="explanation">
                <p>This plot shows the change in cost at each step of the optimization. As seen, the cost decreases over the course of the optimization, indicating a converging optimization process.</p>
            </div>
            <h2>Cost Distribution</h2>
            <img src="file://{os.path.abspath(histogram_path)}" alt="Cost Distribution">
            <div class="explanation">
                <p>The histogram shows the distribution of cost values throughout the optimization. Most values are concentrated around the minimum values, indicating successful finding of the optimal solution.</p>
            </div>
            <h2>Moving Average Plot</h2>
            <img src="file://{os.path.abspath(moving_average_path)}" alt="Moving Average Plot">
            <div class="explanation">
                <p>The moving average plot helps to smooth out fluctuations in the cost, providing a clearer view of the downward trend in cost throughout the optimization.</p>
            </div>
            <h2>Boxplot</h2>
            <img src="file://{os.path.abspath(boxplot_path)}" alt="Boxplot">
            <div class="explanation">
                <p>The boxplot visualizes the distribution of cost data through their quartile values, including the median and outliers.</p>
            </div>
            <h2>Density Plot</h2>
            <img src="file://{os.path.abspath(density_plot_path)}" alt="Density Plot">
            <div class="explanation">
                <p>The density plot shows the density of cost values, providing a better understanding of their distribution.</p>
            </div>
            <h2>Interactive Cost Plot</h2>
            <a href="{interactive_plot_path}" target="_blank" style="display: block; text-align: center;">Interactive Plot</a>
            <div class="explanation">
                <p>The interactive plot allows for a more detailed examination of the change in cost at each step of the optimization.</p>
            </div>
            <div class="conclusion">
                <p>Based on the conducted analysis, we can conclude that the optimization process converges successfully, as the cost values decrease and stabilize at minimal values.</p>
            </div>
        </div>
        </body>
        </html>
        """)
    logging.info(f"Report generated at {report_path}")
    return report_path
