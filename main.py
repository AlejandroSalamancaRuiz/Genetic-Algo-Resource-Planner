import pandas as pd
from GA import Genetic_Algo, plot_ga
import os
import json
import argparse
from datetime import datetime
import numpy as np

# Main function to load CSV files, run GA, and save output
def main(input_folder, output_folder):
    # Load input matrices from CSV files
    skill_table = pd.read_csv(os.path.join(input_folder, 'skill_table.csv')).values
    months_per_task = pd.read_csv(os.path.join(input_folder, 'months_per_task.csv')).values.flatten()
    cost_per_person = pd.read_csv(os.path.join(input_folder, 'cost_per_person.csv')).values.flatten()
    skills_per_task = pd.read_csv(os.path.join(input_folder, 'skills_per_task.csv')).values

    # Load GA parameters from JSON file
    with open(os.path.join(input_folder, 'ga_params.json'), 'r') as config_file:
        config = json.load(config_file)

    p_size = config['population_size']
    w1 = config['w1']
    w2 = config['w2']
    max_generations = config['max_generations']
    p_crossover = config['crossover_probability']
    p_mutation = config['mutation_probability']
    p_replacement = config['replacement_percentage']

    # Initialize GA and run selection
    ga = Genetic_Algo(w1, w2, skill_table, months_per_task, cost_per_person, skills_per_task, p_size, p_crossover, p_mutation, p_replacement, max_generations)
    mins, maxs, means, best_chromosomes = ga.run_algorithm()

    # Save results and plot
    plot_ga(mins, maxs, means, output_folder)

    # Save best chromosomes to CSV
    best_chromosome = best_chromosomes[np.argmax(maxs)]
    pd.DataFrame(best_chromosome).to_csv(os.path.join(output_folder, 'best_chromosome.csv'), index=False)

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run Genetic Algorithm Resource Planner.')
    parser.add_argument('--input_folder', type=str, help='Path to the input folder')
    parser.add_argument('--output_folder', type=str, nargs='?', default=None, help='Path to the output folder (optional)')
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder or f'out_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Run the GA process
    main(input_folder, output_folder)

    # Save input parameters to a JSON file in the output folder
    with open(os.path.join(output_folder, 'input_parameters.json'), 'w') as param_file:
        json.dump(vars(args), param_file, indent=4)