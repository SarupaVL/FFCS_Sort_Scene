from constraint import Problem
import pandas as pd
import ast

# Function to load data from an Excel file
def load_data(uploaded_file):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file, sheet_name='Sheet1')  # Adjust sheet name as per the actual file

    # Initialize empty lists to store subjects and their corresponding slots
    list_of_subjects = []
    list_of_slots = []

    # Loop through the DataFrame to extract subjects and slots
    for i in range(len(df)):
        # Assuming the subject is in the first column and slots are in the second column as a string
        list_of_subjects.append(df.iloc[i, 0])
        temp = df.iloc[i, 1]
        list_of_slots.append(ast.literal_eval(f'[{temp}]'))  # Convert the string to a list of slots

    return list_of_subjects, list_of_slots

# Function to solve the constraint problem
def solve_problem(list_of_subjects, list_of_slots):
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

    # Dynamically create slot priority mapping from the loaded data
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

    # Sorting solutions
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

    # Create a DataFrame for the sorted solutions
    output_data = [
        {**{subject: solution[subject] for subject in list_of_subjects}, 'Score': score_solution(solution)}
        for solution in sorted_solutions
    ]

    df = pd.DataFrame(output_data)

    return df  # Return DataFrame instead of printing
