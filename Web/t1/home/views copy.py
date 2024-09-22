from django.shortcuts import render
from .solver import solve_problem
import ast  

# In-memory storage for user input
user_subjects = []  # This should be global to maintain state
subject_teacher_mappings = {}

def home_view(request):
    return render(request, 'home.html')

def bck1(request):
    global user_subjects, subject_teacher_mappings
    solutions = []

    if request.method == "POST":
        if 'refresh' in request.POST:
            # Clear the user_subjects list to reset the table
            user_subjects = []
            subject_teacher_mappings = {}
        elif 'submit' not in request.POST:
            subject = request.POST.get('subject', '').strip()
            slots = request.POST.get('slots', '').strip()
            teachers = request.POST.get('teacher', '').strip().split(',')

            if subject and slots:
                try:
                    parsed_slots = ast.literal_eval(slots)
                    if isinstance(parsed_slots, (list, tuple)):
                        # Store subject with both slots and teachers
                        user_subjects.append({subject: {'slots': parsed_slots, 'teachers': teachers}})
                    else:
                        raise ValueError
                except (ValueError, SyntaxError) as e:
                    print("Error parsing slots:", e)

        if 'submit' in request.POST:
            if user_subjects:
                # Check contents of user_subjects before proceeding
                print("User Subjects:", user_subjects)

                subject_slots = {list(entry.keys())[0]: entry[list(entry.keys())[0]] for entry in user_subjects}
                subject_teacher_mappings = {list(entry.keys())[0]: entry[list(entry.keys())[0]]['teachers'] for entry in user_subjects}

                # Proceed with solving the problem
                solutions_df = solve_problem(subject_slots, subject_teacher_mappings)
                solutions = solutions_df.to_dict(orient='records')

    return render(request, 'bck1.html', {'user_subjects': user_subjects, 'solutions': solutions})
