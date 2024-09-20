from constraint import *
from pandasPart import list_of_subjects, list_of_slots

problem = Problem()
CONSTRAINTS = []

for a,b in zip(list_of_subjects, list_of_slots):
    problem.addVariable(a, b)

# print(problem._variables)

for i in range(len(list_of_subjects)):
    for j in range(i, len(list_of_subjects)):
        if list_of_subjects[i] != list_of_subjects[j]:
            CONSTRAINTS.append((list_of_subjects[i], list_of_subjects[j]))

print(CONSTRAINTS)

for x,y in CONSTRAINTS:
    problem.addConstraint(lambda x,y: x!=y, (x,y))


for solution in problem.getSolutions():
    print(solution)