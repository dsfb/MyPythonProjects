from hstest import StageTest, CheckResult, WrongAnswer, TestCase
from .application_list import application_list as application_list

input_1 = ["5"]
input_2 = ["23"]
input_3 = ["10"]
input_4 = ["15"]


class TestAdmissionProcedure(StageTest):
    def generate(self):
        return [
            TestCase(stdin=input_1, attach=input_1, files={'applicants.txt': application_list}),
            TestCase(stdin=input_2, attach=input_2, files={'applicants.txt': application_list}),
            TestCase(stdin=input_3, attach=input_3, files={'applicants.txt': application_list}),
            TestCase(stdin=input_4, attach=input_4, files={'applicants.txt': application_list})
        ]

    @staticmethod
    def sort_by_priority(applicants, priority_n, departments_names, departments_lists, max_students, exams):

        def mean(numbers):
            return sum(numbers) / len(numbers)

        accepted_students = []
        for n, dep in enumerate(departments_names):
            dep_list = departments_lists[n]
            exam_numbers = exams[n]
            if len(dep_list) == max_students:
                continue
            students_needed = max_students - len(dep_list)
            dep_applicants = []
            for applicant in applicants:
                if applicant[-1][priority_n] != dep:
                    continue
                mean_exam_score = mean([applicant[exam_n + 1] for exam_n in exam_numbers])
                best_score = float(max([mean_exam_score, applicant[-2]]))
                dep_applicants.append([applicant[0], best_score])

            dep_applicants = sorted(dep_applicants, key=lambda x: (-x[1], x[0]))[:students_needed]
            departments_lists[n].extend(dep_applicants)
            accepted_students.extend([appl[0] for appl in dep_applicants])
        applicants = [applicant for applicant in applicants if applicant[0] not in accepted_students]
        return applicants, departments_lists

    @staticmethod
    def get_admission_lists(max_students):
        applicants = application_list.strip().split('\n')
        departments = {'Mathematics': [2], 'Physics': [0, 2], 'Biotech': [1, 0], 'Chemistry': [1],
                       'Engineering': [3, 2]}
        exams = [departments[dep] for dep in sorted(departments)]
        departments = sorted(departments)
        applicants_data = []
        for line in applicants:
            line = line.split()
            line = [line[0] + ' ' + line[1]] + [float(element) for element in line[2:-3]] + [line[-3:]]
            applicants_data.append(line)
        departments_lists = [[] for _ in departments]
        for i in range(len(applicants_data[-1][-1])):
            applicants_data, departments_lists = TestAdmissionProcedure.sort_by_priority(applicants_data,
                                                                                         i, departments,
                                                                                         departments_lists,
                                                                                         max_students, exams)
        departments_lists = [[' '.join([str(el) for el in applicant])
                              for applicant in sorted(dep, key=lambda x: (-x[1], x[0]))]
                             for dep in departments_lists]
        return departments, departments_lists

    def check(self, reply: str, attach: list):
        n = int(attach[0])
        department_names, admission_lists = self.get_admission_lists(n)
        for i, department_name in enumerate(department_names):
            filename = department_name.lower() + ".txt"
            try:
                with open(filename, "r", encoding="utf-8") as fh:
                    output_applicants = fh.read()
            except FileNotFoundError:
                raise WrongAnswer("The file {0} is not found.\n"
                                  "Please make sure that you output results to files\n"
                                  "and specify the correct paths for them.".format(filename))

            if not output_applicants:
                raise WrongAnswer("The file for the {0} department is empty.".format(department_name))
            output_applicants = output_applicants.strip().split('\n')
            output_applicants = [line for line in output_applicants if line.strip()]
            correct_applicants = admission_lists[i]
            if len(correct_applicants) != len(output_applicants):
                raise WrongAnswer("The file for the {0} department is expected to contain {1} line(s).\n"
                                  "However, {2} lines are found.".format(department_name, len(correct_applicants),
                                                                         len(output_applicants)))

            for j, applicant in enumerate(correct_applicants):
                applicant_name, applicant_surname, score = applicant.split()
                applicant_name = "{0} {1}".format(applicant_name, applicant_surname)
                score = round(float(score), 2)
                output_applicant = output_applicants[j].strip().split(' ')
                if len(output_applicant) != 3:
                    raise WrongAnswer("Line {0} for the {1} department "
                                      "does not seem to contain three elements: first name, last name and score.\n"
                                      "Make sure you separate them "
                                      "with one whitespace character.".format(j + 1,
                                                                              department_name))
                output_applicant_name = "{0} {1}".format(output_applicant[0], output_applicant[1])
                try:
                    output_score = round(float(output_applicant[-1]), 2)
                except ValueError:
                    raise WrongAnswer("The second element in line {0} for the {1} department\n"
                                      "does not seem to be a number: \"{2}\". \n"
                                      "Make sure you format the output "
                                      "as stated in the example.".format(j + 1,
                                                                         department_name,
                                                                         output_applicant[1]))
                if applicant_name.lower().strip() not in output_applicant_name.lower():
                    raise WrongAnswer("The first element in line {0} for the {1} department\n"
                                      "does not seem to contain the correct name of the student ({2}).\n"
                                      "Instead, it is equal to \"{3}\"".format(j + 1, department_name,
                                                                               applicant_name,
                                                                               output_applicant_name))

                if score != output_score:
                    raise WrongAnswer("The second element in line {0} for the {1} department\n"
                                      "does not seem to contain the correct score of the student ({2}).\n"
                                      "Instead, it is equal to \"{3}\"".format(j + 1, department_name,
                                                                               score,
                                                                               output_score))

        return CheckResult.correct()


if __name__ == '__main__':
    TestAdmissionProcedure().run_tests()
