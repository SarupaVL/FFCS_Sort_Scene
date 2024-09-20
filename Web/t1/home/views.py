from django.shortcuts import render
from django.http import JsonResponse
from .solver import load_data, solve_problem
from django.core.files.storage import FileSystemStorage

def home_view(request):
    return render(request, 'home.html')

def bck1(request):
    if request.method == 'POST' and request.FILES.get('file'):
        # Retrieve uploaded file
        uploaded_file = request.FILES['file']

        # Save the file (optional, if you need to save it)
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        # Load the data from the Excel file
        list_of_subjects, list_of_slots = load_data(uploaded_file)

        # Solve the constraint problem
        solutions_df = solve_problem(list_of_subjects, list_of_slots)

        # Convert DataFrame to a list of dictionaries
        solutions_list = solutions_df.to_dict(orient='records')

        # Pass the solutions to the template for rendering
        return render(request, 'solutions_table.html', {'solutions': solutions_list})

    return render(request, 'bck1.html')
