import pandas as pd
from constraint import Problem
import ast

def solve_problem(subject_slots, subject_teacher_mappings):
    print("Subject Slots:", subject_slots)
    print("Subject Teacher Mappings:", subject_teacher_mappings)

    # Create a list of subjects
    list_of_subjects = list(subject_slots.keys())

    # Extract the slots for each subject from the subject_slots dictionary
    list_of_slots = [ast.literal_eval(str(details['slots'])) for details in subject_slots.values()]

    # Create a dictionary to map subjects to their slot priorities
    slot_priority_mapping = {subject: slots for subject, slots in zip(list_of_subjects, list_of_slots)}

    # Initialize the constraint problem
    problem = Problem()

    # Add variables for each subject and their available slots
    for subject, slots in zip(list_of_subjects, list_of_slots):
        problem.addVariable(subject, slots)

    # Prepare a new dictionary to map subjects to (professor, slot) tuples
    subject_slot_teacher_mapping = {subject: [] for subject in list_of_subjects}

    # Populate the mapping with professors and their corresponding slots
    for subject, details in subject_teacher_mappings.items():
        slots = ast.literal_eval(str(subject_slots[subject]['slots']))  # Ensure this matches your structure
        teachers = details  # Assuming details directly contain the list of teachers
        for i, teacher in enumerate(teachers):
            if i < len(slots):
                subject_slot_teacher_mapping[subject].append((teacher, slots[i]))

    # Print the subject_slot_teacher_mapping for debugging
    print("Subject Slot Teacher Mapping:", subject_slot_teacher_mapping)

    # Add constraints to ensure different subjects do not share the same slot
    for i in range(len(list_of_subjects)):
        for j in range(i + 1, len(list_of_subjects)):
            problem.addConstraint(lambda x, y: x != y, (list_of_subjects[i], list_of_subjects[j]))

    # Get all possible solutions
    solutions = problem.getSolutions()

    # Function to score solutions based on slot priority
    def score_solution(solution):
        total_score = 0
        num_slots = max(len(slots) for slots in slot_priority_mapping.values())
        for subject in list_of_subjects:
            slot = solution[subject]
            if slot in slot_priority_mapping[subject]:
                index = slot_priority_mapping[subject].index(slot)
                score = 1 - (index / (num_slots - 1))
            else:
                score = 0
            total_score += score
        return total_score

    # Prepare the output, including teacher mapping and scores
    # Prepare the output, including teacher mapping and scores
    output_data = []
    for solution in solutions:
        score = score_solution(solution)  # Calculate score once per solution
        timetable_entry = {
            'Score': score,
            'Timetable': []  # Create a list to hold subject-slot-teacher tuples
        }
        
        for subject in list_of_subjects:
            slot = solution[subject]
            teachers_for_slot = [teacher for teacher, slot_ in subject_slot_teacher_mapping[subject] if slot_ == slot]
            
            # Append subject, slot, and teachers to the timetable entry
            timetable_entry['Timetable'].append({
                'subject': subject,
                'slot': slot,
                'teachers': ', '.join(teachers_for_slot)
            })
        
        # Append the complete timetable entry to output data
        output_data.append(timetable_entry)

    # Create a DataFrame from the output data
    df_output = pd.DataFrame(output_data)

    # Sort by Score to display the best solutions first
    df_output = df_output.sort_values(by='Score', ascending=False).reset_index(drop=True)

    print("\nCombined Timetable:\n", df_output)
    return df_output  # Return the DataFrame for further use
