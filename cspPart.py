from constraint import *
from pandasPart import list_of_subjects, list_of_slots

# Your existing problem setup
problem = Problem()
CONSTRAINTS = []

for a, b in zip(list_of_subjects, list_of_slots):
    problem.addVariable(a, b)

# Creating constraints to ensure different subjects have different slots
for i in range(len(list_of_subjects)):
    for j in range(i + 1, len(list_of_subjects)):
        if list_of_subjects[i] != list_of_subjects[j]:
            CONSTRAINTS.append((list_of_subjects[i], list_of_subjects[j]))

for x, y in CONSTRAINTS:
    problem.addConstraint(lambda x, y: x != y, (x, y))

# Get all solutions
solutions = problem.getSolutions()

# Define the subject priority mapping
subject_priority_mapping = {
    'Java': 1,
    'DSA': 2,
    'English': 3,
    'DSD': 4,
    'Calculus': 5
}

# Define the slot priority mapping
slot_priority_mapping = {
    'Java': [(31, 32), (39, 40), (45, 46), (59, 60)],
    'DSA': [(31, 32), (35, 36), (41, 42)],
    'English': [(51, 52), (39, 40), (41, 42)],
    'DSD': [(45, 46), (51, 52), (31, 32)],
    'Calculus': [(39, 40), (31, 32), (59, 60)]
}

# Function to sort solutions based on score and subject priority
def sort_solutions(solutions):
    return sorted(solutions, key=lambda sol: (
        -score_solution(sol),  # Negative for descending order
        [subject_priority_mapping[subject] for subject in list_of_subjects]
    ))

# Function to score each solution
def score_solution(solution):
    score = 0
    for subject in list_of_subjects:
        slot = solution[subject]
        # Increase score based on slot's index in the priority list
        score += len(slot_priority_mapping[subject]) - slot_priority_mapping[subject].index(slot)
    return score

# Sort the solutions
sorted_solutions = sort_solutions(solutions)

# Print headers
header = " | ".join(subject_priority_mapping.keys()) + " | Score"
print(header)
print("-" * (len(header) + 6))  # Adjust the length for the score column

# Print sorted solutions with scores
for solution in sorted_solutions:
    score = score_solution(solution)
    row = " | ".join(f"{subject}: {solution[subject]}" for subject in sorted(subject_priority_mapping.keys(), key=lambda s: subject_priority_mapping[s]))
    print(f"{row} | {score}")
