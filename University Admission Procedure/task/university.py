from typing import List
import statistics as st


def create_ranking(iteration, applist_sorted):
    # physics, chemistry, math, computer science: col 2-5
    # physics and math for the Physics department, chemistry for the Chemistry department,
    # math for the Mathematics , computer science and math for the Engineering
    # chemistry and physics for the Biotech department.
    x = iteration + 6
    bio_candidates = sorted([applicant for applicant in applist_sorted if applicant[x] == "Biotech"], key=lambda x: (min(st.mean([-x[3], -x[2]]), -x[6]), x[0], x[1]))
    chem_candidates = sorted([applicant for applicant in applist_sorted if applicant[x] == "Chemistry"], key=lambda x: (min(-x[3], -x[6]), x[0], x[1]))
    eng_candidates = sorted([applicant for applicant in applist_sorted if applicant[x] == "Engineering"], key=lambda x: (min(st.mean([-x[5], -x[4]]), -x[6]), x[0], x[1]))
    math_candidates = sorted([applicant for applicant in applist_sorted if applicant[x] == "Mathematics"], key=lambda x: (min(-x[4], -x[6]), x[0], x[1]))
    physics_candidates = sorted([applicant for applicant in applist_sorted if applicant[x] == "Physics"], key=lambda x: (min(st.mean([-x[2], -x[4]]), -x[6]), x[0], x[1]))

    return allocate(applist_sorted, bio_candidates, chem_candidates, eng_candidates, math_candidates,
                    physics_candidates)


def printnames(list, col):
    for x in list[:numlines]:
        print(x[0] + ' ' + x[1] + ' ' + str(x[col]))

def writenames(list, col_1, col_2, filename):
    if col_1 == col_2:
        for x in list[:numlines]:
            filename.write(x[0] + ' ' + x[1] + ' ' + str(max(x[col_1], x[6])) + '\n')
    else:
        for x in list[:numlines]:
            filename.write(x[0] + ' ' + x[1] + ' ' + str(max(st.mean([x[col_1], x[col_2]]), x[6])) + '\n')



def update_alloc(bio_alloc, chem_alloc, eng_alloc, math_alloc, physics_alloc):
    bio_alloc_final.extend(bio_alloc)
    chem_alloc_final.extend(chem_alloc)
    eng_alloc_final.extend(eng_alloc)
    math_alloc_final.extend(math_alloc)
    physics_alloc_final.extend(physics_alloc)


def allocate(applist_sorted, bio_candidates, chem_candidates, eng_candidates, math_candidates, physics_candidates):
    bio_alloc = bio_candidates[:capacity[0]]
    chem_alloc = chem_candidates[:capacity[1]]
    eng_alloc = eng_candidates[:capacity[2]]
    math_alloc = math_candidates[:capacity[3]]
    physics_alloc = physics_candidates[:capacity[4]]

    applist_sorted = [x for x in applist_sorted if x not in bio_alloc]
    applist_sorted = [x for x in applist_sorted if x not in chem_alloc]
    applist_sorted = [x for x in applist_sorted if x not in eng_alloc]
    applist_sorted = [x for x in applist_sorted if x not in math_alloc]
    applist_sorted = [x for x in applist_sorted if x not in physics_alloc]

    capacity[0] -= len(bio_alloc)
    capacity[1] -= len(chem_alloc)
    capacity[2] -= len(eng_alloc)
    capacity[3] -= len(math_alloc)
    capacity[4] -= len(physics_alloc)

    update_alloc(bio_alloc, chem_alloc, eng_alloc, math_alloc, physics_alloc)
    return applist_sorted


def print_alloc():
    # applist_sorted = sorted(applist, key=lambda x: (-x[2], x[0], x[1]))
    # physics, chemistry, math, computer science: col 2-5
    print("Biotech")
    printnames(sorted(bio_alloc_final, key=lambda x: (-x[3], x[0], x[1])), 3)
    print('')
    print("Chemistry")
    printnames(sorted(chem_alloc_final, key=lambda x: (-x[3], x[0], x[1])), 3)
    print('')
    print("Engineering")
    printnames(sorted(eng_alloc_final, key=lambda x: (-x[5], x[0], x[1])), 5)
    print('')
    print("Mathematics")
    printnames(sorted(math_alloc_final, key=lambda x: (-x[4], x[0], x[1])), 4)
    print('')
    print("Physics")
    printnames(sorted(physics_alloc_final, key=lambda x: (-x[2], x[0], x[1])), 2)
    print('')

    return applist_sorted

def write_alloc():
    bio_file = open("biotech.txt", 'w')
    writenames(sorted(bio_alloc_final, key=lambda x: (min(st.mean([-x[3], -x[2]]), -x[6]), x[0], x[1])), 3, 2, bio_file)
    bio_file.close()

    chem_file = open("chemistry.txt", 'w')
    writenames(sorted(chem_alloc_final, key=lambda x: (min(-x[3], -x[6]), x[0], x[1])), 3, 3, chem_file)
    chem_file.close()

    eng_file = open("engineering.txt", 'w')
    writenames(sorted(eng_alloc_final, key=lambda x: (min(st.mean([-x[5], -x[4]]), -x[6]), x[0], x[1])), 5, 4, eng_file)
    eng_file.close()

    math_file = open("mathematics.txt", 'w')
    writenames(sorted(math_alloc_final, key=lambda x: (min(-x[4], -x[6]), x[0], x[1])), 4, 4, math_file)
    math_file.close()

    phys_file = open("physics.txt", 'w')
    writenames(sorted(physics_alloc_final, key=lambda x: (min(st.mean([-x[4], -x[2]]), -x[6]), x[0], x[1])), 4, 2, phys_file)
    phys_file.close()


if __name__ == '__main__':
    numlines = int(input("Enter N: "))

    # Biotech, Chemistry, Engineering, Mathematics, Physics,
    capacity = [numlines] * 5
    bio_alloc_final = []
    chem_alloc_final = []
    eng_alloc_final = []
    math_alloc_final = []
    physics_alloc_final = []



    applist = [[]]
    # col 1: first
    # col 2: last
    # col 3: physics
    # col 4: chemistry
    # col 5: math
    # col 6: computer science
    # col 7: admissions test
    # col 8: 1 prio
    # col 9: 2 prio
    # col 10: 3 prio
    with open("/Users/ts/Downloads/applicant_list_7.txt") as file:
        for line in file:
            applicant: list[str] = line.split(' ')
            applicant[2:7] = [float(x) for x in applicant[2:7]]
            applicant[9] = applicant[9].replace('\n', "")
            applist.append(applicant)

    applist.pop(0)
    applist_sorted = sorted(applist, key=lambda x: (x[0], x[1]))

    # first round
    applist_sorted_2 = create_ranking(1, applist_sorted)

    # second round
    if any(x > 0 for x in capacity):
        applist_sorted_3 = create_ranking(2, applist_sorted_2)

    # third round
    if any(x > 0 for x in capacity):
        applist_sorted = create_ranking(3, applist_sorted_3)

    print_alloc()
    write_alloc()
