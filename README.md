# Genetic Algorithm for project resource planning

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Algorithm Details](#algorithm-details)
5. [Examples](#examples)

## Introduction
This project implements a Genetic Algorithm to optimize resource planning for software projects. It aims to allocate resources efficiently to maximize productivity and minimize costs.

The project is based on the research presented in the paper by Chang, C. K., Christensen, M. J., & Zhang, T. (2001). Genetic Algorithms for Project Management. Annals of Software Engineering, 11, 107–139. https://doi.org/10.1023/A:1012543203763

## Installation
To install the necessary dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage
To run the algorithm, execute:
```bash
python main.py --input_folder <path_to_input_folder> --output_folder <path_to_output_folder>
```

### Arguments

### Required

- **input_folder**: Folder that contains necessary CSV files with problem specifications and a JSON file containing the parameters for the genetic algorithm. The following are the names and descriptions of the files that are expected in the input folder:
  
  - **skill_table.csv**: This table represents a matrix where each row corresponds to an individual (employee), and each column represents a specific skill. The values in the matrix are binary (0 or 1), indicating whether a person possesses a particular skill (1) or not (0). For example, if row 2, column 3 has a value of `1`, this means person 2 has skill 3. This matrix is used by the genetic algorithm to assess whether a team of people can collectively cover all the required skills for a given task.
  
    **Example**:
    ```
    Skill1, Skill2, Skill3
    1,      0,      1
    0,      1,      0
    1,      1,      0
    ```
    - Row 1 (Person 1) has skills 1 and 3.
    - Row 2 (Person 2) has skill 2.
    - Row 3 (Person 3) has skills 1 and 2.
  
  - **months_per_task.csv**: This file contains a single column listing the number of months required to complete each task. The number of rows corresponds to the number of tasks in the project. Each value represents the time commitment for completing a specific task, which the genetic algorithm uses to calculate the schedule. It influences the overall time needed for task allocation.
  
    **Example**:
    ```
    Months
    3
    6
    4
    ```
    - Task 1 takes 3 months to complete.
    - Task 2 takes 6 months to complete.
    - Task 3 takes 4 months to complete.
  
  - **cost_per_person.csv**: This file contains a single column where each row corresponds to a person and represents their cost per unit of time (e.g., per month). The cost data is used in the genetic algorithm to minimize the total project cost based on the team’s composition. The algorithm aims to optimize task assignments based on skill match and cost efficiency.
  
    **Example**:
    ```
    Cost
    1000
    1200
    1500
    ```
    - Person 1 costs $1000 per month.
    - Person 2 costs $1200 per month.
    - Person 3 costs $1500 per month.
  
  - **skills_per_task.csv**: This matrix specifies the required skills for each task. Each row corresponds to a task, and each column corresponds to a specific skill. The values in the matrix are binary (0 or 1), indicating whether a specific skill is required for that task. This information is crucial for the genetic algorithm to ensure that the team assigned to each task has the necessary skills.
  
    **Example**:
    ```
    Skill1, Skill2, Skill3
    1,      0,      1
    1,      1,      0
    0,      1,      1
    ```
    - Task 1 requires skills 1 and 3.
    - Task 2 requires skills 1 and 2.
    - Task 3 requires skills 2 and 3.
  
  - **ga_params.json**: This JSON file contains the parameters for configuring the genetic algorithm. These parameters control how the algorithm operates and evolves solutions over multiple generations. The key parameters typically include:
    - `w1`: Weight for cost optimization in the fitness function.
    - `w2`: Weight for time optimization in the fitness function.
    - `population_size`: The number of individuals in the population.
    - `crossover_probability`: The probability of crossover between individuals during evolution.
    - `mutation_probability`: The probability of mutation in the population.
    - `replacement_percentage`: The percentage of the population to replace in each generation.
    - `max_generations`: The maximum number of generations for the genetic algorithm to evolve.

### Optional

- **output_folder**: Folder where the program will save the output results, including the best chromosome configuration and the fitness evolution plot. If this argument is not provided, the results will be saved in an output folder generated with a time stamp.

## Algorithm Details

The Genetic Algorithm (GA) implemented in this project follows a classic evolutionary optimization approach to solving project resource planning problems. The goal is to optimize the allocation of resources (e.g., team members) to tasks while minimizing costs and completion times, and ensuring that the assigned teams possess the required skills for each task.

The main components of the algorithm are as follows:

- **Initialization**: A population of potential solutions (individuals) is randomly generated. Each individual represents a specific assignment of team members to tasks over a given timeline.
The population size and structure are defined based on the input parameters, including the skills table, months required for each task, and cost per person.

- **Fitness Calculation**: The fitness function evaluates each individual's performance based on the following criteria:
    - Time: Total time required to complete the project, determined by how tasks are distributed across the team.
    - Cost: The total cost of assigning team members to tasks, accounting for individual costs per time unit.
    - Skill Match: The degree to which the assigned team collectively covers the required skills for each task.

    These factors are combined in a weighted fitness function, where w1 and w2 are user-defined weights that balance the optimization between cost and time.
    Fitness values are normalized, and a selection probability is calculated for each individual based on their relative fitness scores.

- **Selection**: Individuals are selected for reproduction using roulette wheel selection, which assigns a higher probability of selection to individuals with higher fitness scores. This stochastic approach ensures that better-performing individuals have a higher chance of passing on their traits to the next generation.

- **Crossover**: Pairs of selected individuals undergo crossover, where parts of their solution (team assignments) are exchanged to produce offspring. This process combines the strengths of both parents to explore new potential solutions.
The probability of crossover is governed by the parameter p_crossover, and the crossover process may involve randomly selecting points in the task-team assignment matrix to perform the swap.

- **Mutation**: After crossover, offspring may undergo mutation, where random changes are introduced to some of the task assignments. This helps maintain diversity in the population and allows the algorithm to explore new areas of the solution space.
The mutation rate is controlled by the parameter p_mutation, and the mutation ensures that at least one team member is assigned to each task by adjusting the assignment probabilities.

- **Replacement**:
In each generation, a portion of the population is replaced by the newly generated offspring. The percentage of the population to be replaced is determined by p_replacement.
This step ensures that the population evolves over time, with better-performing individuals having a higher likelihood of surviving and passing on their characteristics.

- **Termination**:
The process of selection, crossover, mutation, and replacement is repeated for a predefined number of generations (max_generations), or until the algorithm converges on an optimal solution.
The best solution found over all generations is selected as the final output, and the fitness values of the population are recorded for analysis.
By continuously evolving the population through these mechanisms, the Genetic Algorithm seeks to find the most efficient and cost-effective resource allocation for the project.

The fitness evolution is visualized in a plot that shows the minimum, maximum, and average fitness scores across generations, providing insights into how the algorithm improves over time. This helps track progress and ensure that the algorithm is optimizing toward the desired goals.


## Examples
Here is an example of running the algorithm:
```bash
python main.py --input_folder InputDataExample
```



