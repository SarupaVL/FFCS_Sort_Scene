import pandas as pd
from constraint import *
from pandasPart import list_of_subjects, list_of_slots  # Assuming these are loaded in your other file

# Load the teacher-slot mapping from the new Excel file
teacher_slot_df = pd.read_excel('TeachersAndSlots.xlsx')

# Create a nested dictionary mapping subjects to their respective slot-to-teacher mappings
subject_teacher_mapping = {}
for index, row in teacher_slot_df.iterrows():
    teacher = row['Teacher']
    slot = tuple(map(int, row['Slots'].replace('(', '').replace(')', '').split(',')))
    subject_name = teacher.split('_')[0]  # Extract the subject name prefix from the teacher's name
    
    if subject_name not in subject_teacher_mapping:
        subject_teacher_mapping[subject_name] = {}
    
    subject_teacher_mapping[subject_name][slot] = teacher

# Existing problem setup
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

# Create a slot priority mapping dynamically from the loaded data
slot_priority_mapping = {
    subject: slots for subject, slots in zip(list_of_subjects, list_of_slots)
}

# Scoring function for solutions
def score_solution(solution):
    total_score = 0
    num_slots = max(len(slots) for slots in slot_priority_mapping.values())  # Determine the maximum number of slots
    for subject in list_of_subjects:
        slot = solution[subject]
        if slot in slot_priority_mapping[subject]:
            index = slot_priority_mapping[subject].index(slot)
            score = 1 - (index / (num_slots - 1))  # Scale the score between 0 and 1
        else:
            score = 0  # If slot is not found, score it as 0
        total_score += score
    return total_score

# Sort solutions
def sort_solutions(solutions):
    subject_priority_mapping = {
        'Java': 1,
        'DSA': 2,
        'English': 3,
        'DSD': 4,
        'Calculus': 5
    }
    return sorted(
        solutions,
        key=lambda sol: (-score_solution(sol), [subject_priority_mapping.get(subject, 0) for subject in list_of_subjects])
    )

# Sort the solutions
sorted_solutions = sort_solutions(solutions)

# Create DataFrame for sorted solutions and map slots to the correct teacher names based on the subject
output_data = []
for solution in sorted_solutions:
    solution_data = {
        subject: subject_teacher_mapping.get(subject, {}).get(solution[subject], solution[subject])
        for subject in list_of_subjects
    }
    solution_data['Score'] = score_solution(solution)
    output_data.append(solution_data)

df = pd.DataFrame(output_data)

# Display the DataFrame
print(df)
