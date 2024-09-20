from constraint import *
from pandasPart import list_of_subjects, list_of_slots
import pandas as pd

# Your existing problem setup
problem = Problem()
CONSTRAINTS = []

# Add variables to the problem
for subject, slots in zip(list_of_subjects, list_of_slots):
    problem.addVariable(subject, slots)

# Create constraints to ensure different subjects have different slots
for i in range(len(list_of_subjects)):
    for j in range(i + 1, len(list_of_subjects)):
        if list_of_subjects[i] != list_of_subjects[j]:
            CONSTRAINTS.append((list_of_subjects[i], list_of_subjects[j]))

for x, y in CONSTRAINTS:
    problem.addConstraint(lambda x, y: x != y, (x, y))

# Get all solutions
solutions = problem.getSolutions()

# Subject and slot priority mappings
subject_priority_mapping = {
    'Java': 1,
    'DSA': 2,
    'English': 3,
    'DSD': 4,
    'Calculus': 5
}

slot_priority_mapping = {
    'Java': [(31, 32), (39, 40), (45, 46), (59, 60)],
    'DSA': [(31, 32), (35, 36), (41, 42)],
    'English': [(51, 52), (39, 40), (41, 42)],
    'DSD': [(45, 46), (51, 52), (31, 32)],
    'Calculus': [(39, 40), (31, 32), (59, 60)]
}

def score_solution(solution):
    total_score = 0
    num_slots = 4  # Adjust this if the number of slots changes for any subject
    for subject in list_of_subjects:
        slot = solution[subject]
        index = slot_priority_mapping[subject].index(slot)
        # Calculate score based on index
        score = 1 - (index / (num_slots - 1))  # Scale the score between 0 and 1
        total_score += score
    return total_score

def sort_solutions(solutions):
    return sorted(solutions, key=lambda sol: (-score_solution(sol), [subject_priority_mapping[subject] for subject in list_of_subjects]))

# Sort the solutions
sorted_solutions = sort_solutions(solutions)

# Create a DataFrame for the sorted solutions
output_data = []
for solution in sorted_solutions:
    score = score_solution(solution)
    output_data.append({subject: solution[subject] for subject in list_of_subjects})
    output_data[-1]['Score'] = score

df = pd.DataFrame(output_data)

# Display the DataFrame
print(df)
