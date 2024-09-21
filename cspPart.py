import pandas as pd
from constraint import *
import ast

# Load the combined Excel file with subjects and teachers data
file_name = r"C:\Users\imrit\OneDrive\Desktop\Projects\FFCS Sorter\TestDataSet.xlsx"  # Replace with your actual path
df = pd.read_excel(file_name)

# Initialize lists for subjects and slots
list_of_subjects = []
list_of_slots = []

# Extract subjects and their corresponding slots from columns A and B
for i in range(len(df)):
    subject = df.iloc[i, 0]
    if pd.notna(subject):  # Check if the subject is not NaN
        list_of_subjects.append(subject)
        temp_slots = df.iloc[i, 1]
        list_of_slots.append(ast.literal_eval(f'[{temp_slots}]'))  # Convert the slot strings to list of tuples

# Create a dictionary to map subjects to their slot priorities
slot_priority_mapping = {
    subject: slots for subject, slots in zip(list_of_subjects, list_of_slots)
}

# Create a nested dictionary to map subjects to their slot-to-teacher mappings
subject_teacher_mapping = {}

# Extract teachers and their corresponding slots from columns D and E
for i in range(len(df)):
    teacher = df.iloc[i, 3]
    if pd.notna(teacher):  # Check if the teacher entry is not NaN
        slot = tuple(map(int, df.iloc[i, 4].replace('(', '').replace(')', '').split(',')))
        subject_name = teacher.split('_')[0]  # Extract the subject prefix from the teacher's name

        if subject_name not in subject_teacher_mapping:
            subject_teacher_mapping[subject_name] = {}

        subject_teacher_mapping[subject_name][slot] = teacher

# Set up the constraint problem
problem = Problem()
CONSTRAINTS = []

# Add variables to the problem with slots from list_of_slots
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

# Function to score solutions
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

# Function to sort solutions
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

# Create DataFrame for sorted solutions, map slots to teacher names, and include the slots
output_data = []
for solution in sorted_solutions:
    solution_data = {}
    for subject in list_of_subjects:
        slot = solution[subject]
        teacher = subject_teacher_mapping.get(subject, {}).get(slot, None)
        solution_data[subject] = teacher  # Map the teacher's name
        solution_data[f'{subject}_Slot'] = slot  # Add the corresponding slot
    solution_data['Score'] = score_solution(solution)
    output_data.append(solution_data)

df_output = pd.DataFrame(output_data)

# Display the DataFrame
print(df_output)
