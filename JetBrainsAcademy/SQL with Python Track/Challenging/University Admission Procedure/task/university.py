from collections import defaultdict

from collections import defaultdict

n_applicants = int(input())
file_name = "applicants.txt"
all_departments = ["Biotech", "Chemistry", "Engineering", "Mathematics", "Physics"]
applicant_list = list()
department_applicants = defaultdict(list)
extra_exam_result_index = 5

with open(file_name, "r") as input_file:
    applicant_list = [line[:-1].rsplit(' ', 8) for line in input_file]


def get_exam_result_index_by_department(department):
    if department == 'Physics':
        return 1, 3
    elif department == 'Chemistry':
        return 2,
    elif department == 'Biotech':
        return 1, 2
    elif department == 'Mathematics':
        return 3,
    elif department == 'Engineering':
        return 3, 4

    return tuple()


def average(a, b):
    return (float(a) + float(b)) / 2


def average_by_index(the_list, index1, index2):
    return average(the_list[index1], the_list[index2])


def get_max_exam_result(result1, result2):
    return max(float(result1), float(result2))


def get_max_average(the_list, index1, index2):
    result1 = average_by_index(the_list, index1, index2)
    extra_result = the_list[extra_exam_result_index]
    return get_max_exam_result(result1, extra_result)


def get_exam_result_for(the_applicant, index1):
    result1 = the_applicant[index1]
    result2 = the_applicant[extra_exam_result_index]
    return get_max_exam_result(result1, result2)


def get_sorted_applicant_list_by_gpa_for_department(applicant_list, department):
    exam_result_indexes = get_exam_result_index_by_department(department)

    if len(exam_result_indexes):
        if len(exam_result_indexes) == 1:
            return sorted(applicant_list,
                          key=lambda the_applicant: (
                              -get_exam_result_for(the_applicant, exam_result_indexes[0]), the_applicant[6],
                              the_applicant[0], the_applicant[7],
                              the_applicant[8]))
        else:
            return sorted(applicant_list,
                          key=lambda the_applicant: (
                              -get_max_average(the_applicant, *exam_result_indexes),
                              the_applicant[6], the_applicant[0],
                              the_applicant[7], the_applicant[8]))


def format_as_str(number):
    result = str(number)
    return result if '.' in result else result + '.0'


for choice_index in range(6, 9):
    for seat in all_departments:
        applicant_list = get_sorted_applicant_list_by_gpa_for_department(applicant_list, seat)
        for applicant in applicant_list[:]:
            if len(department_applicants[seat]) < n_applicants and applicant[choice_index] == seat:
                department_applicants[seat].append(applicant)
                applicant_list.remove(applicant)

# write the results to the departments's files.
for department in all_departments:
    with open(f"{department}.txt", "w") as out_file:
        exam_result_indexes = get_exam_result_index_by_department(department)

        if len(exam_result_indexes):
            if len(exam_result_indexes) == 1:
                for new_app_data in sorted(department_applicants[department],
                                           key=lambda the_applicant: (
                                           -get_exam_result_for(the_applicant, exam_result_indexes[0]),
                                           the_applicant[0])):
                    out_file.write(' '.join([
                        new_app_data[0], format_as_str(get_exam_result_for(new_app_data, exam_result_indexes[0]))
                    ]))
                    out_file.write('\n')
            else:
                for new_app_data in sorted(department_applicants[department],
                                           key=lambda the_applicant: (
                                           -get_max_average(the_applicant, *exam_result_indexes),
                                           the_applicant[0])):
                    out_file.write(' '.join([
                        new_app_data[0], format_as_str(get_max_average(new_app_data, *exam_result_indexes))
                    ]))
                    out_file.write('\n')
