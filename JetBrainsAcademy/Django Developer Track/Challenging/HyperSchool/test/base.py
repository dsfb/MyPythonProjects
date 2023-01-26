# -*- coding: utf-8 -*-
import http.cookiejar
import io
import os
import re
import sqlite3
import urllib
import requests

import requests

from hstest import CheckResult, DjangoTest, WrongAnswer

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

INITIAL_TEACHERS = [
    (1, 'John', 'Doe', 35, 'many interesting facts'),
    (2, 'Sheldon', 'Cooper', 15, 'greatest man ever, real scientist'),
]
INITIAL_COURSES = [
    (1, 'Python-developer', 'info1', 12, 950),
    (2, 'Frontend-developer', 'info2', 11, 890),
    (3, 'Go-developer', 'info3', 8, 780),
]

INITIAL_STUDENTS = [
    (1, 'Rajesh', 'Coothrapali', 18),
    (2, 'Leonard', 'Hofsteder', 18),
    (3, 'James', 'Jameson', 31),
    (4, 'Christina', 'Banks', 28),
    (5, 'Toby', 'Flanderson', 40),
    (6, 'Tommy', 'Jones', 18)
]

INITIAL_COURSE_TEACHERS = [
    (1, 1, 1),
    (2, 2, 1),
    (3, 3, 2),
]

INITIAL_STUDENT_COURSES = [
    (1, 1, 1),
    (2, 2, 1),
    (3, 3, 2),
    (4, 4, 3),
    (5, 5, 3),
    (6, 6, 2),
]


class HyperSchoolTest(DjangoTest):
    use_database = True
    H2_PATTERN = '<h2>(.+?)</h2>'
    DIV_PATTERN = '<div>(.+?)</div>'
    TEXT_LINK_PATTERN = '''<a[^>]+href=['"][a-zA-Z\d/_]+['"][^>]*>(.+?)</a>'''
    COMMON_LINK_PATTERN = '''<a[^>]+href=['"]([a-zA-Z\d/_]+)['"][^>]*>'''
    LINK_WITH_TEXT_PATTERN = '''<a[^>]+href=['"]([a-zA-Z\d/_?=]+)['"][^>]*>(.+?)</a>'''
    PARAGRAPH_PATTERN = '<p>(.+?)</p>'
    SRC_PATTERN = '''<source[^>]+src=['"]([a-zA-Z\d/_.]+)['"][^>]*>'''
    CSRF_PATTERN = b'<input[^>]+name="csrfmiddlewaretoken" ' \
                   b'value="(?P<csrf>\w+)"[^>]*>'
    cookie_jar = http.cookiejar.CookieJar()
    USERNAME = 'Test'
    PASSWORD = 'TestPassword46'
    NAME = 'Ivan'
    SURNAME = 'Petrov'
    AGE = 18
    COURSE = 1

    def __stripped_list(self, list):
        return [item.strip() for item in list]

    def __stripped_list_with_tuple(self, list):
        return [(item[0].strip(), item[1].strip()) for item in list]

    # stage 1
    def check_create_courses(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.executemany(
                'INSERT INTO schedule_teacher (`id`, `name`, `surname`, `age`, `about`) '
                'VALUES (?, ?, ?, ?, ?)',
                INITIAL_TEACHERS
            )

            cursor.executemany(
                'INSERT INTO schedule_course (`id`, `title`, `info`, `duration_months`, `price`) '
                'VALUES (?, ?, ?, ?, ?)',
                INITIAL_COURSES
            )

            cursor.executemany(
                'INSERT INTO schedule_student (`id`,`name`, `surname`, `age`) '
                'VALUES (?, ?, ?, ?)',
                INITIAL_STUDENTS
            )

            cursor.executemany(
                'INSERT INTO schedule_course_teacher (`id`,`course_id`, `teacher_id`) '
                'VALUES (?, ?, ?)',
                INITIAL_COURSE_TEACHERS
            )

            cursor.executemany(
                'INSERT INTO schedule_student_course (`id`,`student_id`, `course_id`) '
                'VALUES (?, ?, ?)',
                INITIAL_STUDENT_COURSES
            )

            connection.commit()

            cursor.execute(
                'SELECT `id`, `name`, `surname`, `age`, `about` FROM schedule_teacher')
            teachers = cursor.fetchall()

            if teachers != INITIAL_TEACHERS:
                return CheckResult.wrong('Check your Teacher model')

            cursor.execute(
                'SELECT `id`,`title`, `info`, `duration_months`, `price` FROM schedule_course')
            courses = cursor.fetchall()

            if courses != INITIAL_COURSES:
                return CheckResult.wrong('Check your Course model')

            cursor.execute(
                'SELECT `id`,`name`, `surname`, `age` FROM schedule_student')
            students = cursor.fetchall()

            if students != INITIAL_STUDENTS:
                return CheckResult.wrong('Check your Student model')

            return CheckResult.correct()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    # stage 2

    def check_main_page_header(self) -> CheckResult:
        try:
            page = self.read_page(self.get_url() + 'schedule/main/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        h2_headers = re.findall(self.H2_PATTERN, page, re.S)
        h2_headers = self.__stripped_list(h2_headers)
        main_header = 'HyperSchool'

        is_main_header = False
        for h2_header in h2_headers:
            if main_header in h2_header:
                is_main_header = True
                break

        if not is_main_header:
            return CheckResult.wrong(
                'Main page should contain <h2> element with text "HyperSchool"'
            )

        return CheckResult.correct()

    def check_main_search_courses(self):
        q = 'python'
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT `id`, `title` FROM schedule_course WHERE title "
                f"LIKE '%{q}%'"
            )
            searched_courses = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        searched_course_links_with_titles_from_db = \
            [(f'/schedule/course_details/{x[0]}', x[1]) for x in searched_courses]

        try:
            cursor.execute(
                f"SELECT `id`, `title` FROM schedule_course WHERE title "
                f"NOT LIKE '%{q}%'"
            )
            unsearched_courses = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        unsearched_course_links_with_titles_from_db = \
            [(f'/schedule/course_details/{x[0]}', x[1]) for x in unsearched_courses]

        try:
            page = self.read_page(self.get_url() + f'schedule/main/?q={q}')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        titles_in_links_from_page = re.findall(self.LINK_WITH_TEXT_PATTERN, page, re.S)
        titles_in_links_from_page = self.__stripped_list_with_tuple(titles_in_links_from_page)

        for searched_course_link in searched_course_links_with_titles_from_db:
            if searched_course_link not in titles_in_links_from_page:
                return CheckResult.wrong('Main page should contain links to courses '
                                         'according to keywords in search form')

        for unsearched_course_link in unsearched_course_links_with_titles_from_db:
            if unsearched_course_link in titles_in_links_from_page:
                return CheckResult.wrong('Main page should not contain links to courses'
                                         'not searched')

        return CheckResult.correct()

    def check_link_to_course(self) -> CheckResult:
        course_link = '/schedule/course_details/1'

        try:
            page = self.read_page(
                self.get_url() + 'schedule/main/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if course_link not in links_from_page:
            return CheckResult.wrong(
                f'Course details page should contain <a> element with href {course_link}'
            )

        return CheckResult.correct()

    def check_main_courses_count(self):
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                'SELECT count(*) FROM schedule_course')
            course_count = str(cursor.fetchall()[0][0])
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        try:
            page = self.read_page(self.get_url() + 'schedule/main/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        paragraphs_from_page = re.findall(self.PARAGRAPH_PATTERN, page, re.S)
        paragraphs_from_page = self.__stripped_list(paragraphs_from_page)

        quantity_in_paragraphs = False
        for paragraph in paragraphs_from_page:
            if course_count in paragraph:
                quantity_in_paragraphs = True
                break

        if not quantity_in_paragraphs:
            return CheckResult.wrong(
                f'Main page should contain <p> element with quantity of courses'
            )

        return CheckResult.correct()

    # stage 3
    def check_links_course_page(self) -> CheckResult:
        main_link = '/schedule/main/'
        teacher_details_link = '/schedule/teacher_details/1'

        try:
            page = self.read_page(
                self.get_url() + 'schedule/course_details/1')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the course_details page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if main_link not in links_from_page:
            return CheckResult.wrong(
                f'Course details page should contain <a> element with href {main_link}'
            )
        elif teacher_details_link not in links_from_page:
            return CheckResult.wrong(
                f'Course details page should contain <a> element with href {teacher_details_link}'
            )

        return CheckResult.correct()

    def check_course_info_displayed(self):
        try:
            page = self.read_page(
                self.get_url() + 'schedule/course_details/1')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the course_details page.'
            )

        h2_headers = re.findall(self.H2_PATTERN, page, re.S)
        h2_headers = self.__stripped_list(h2_headers)
        main_header = 'Python-developer'

        is_main_header = False
        for h2_header in h2_headers:
            if main_header in h2_header:
                is_main_header = True
                break

        if not is_main_header:
            return CheckResult.wrong(
                f'Course_details page should contain information about course'
            )

        return CheckResult.correct()

        paragraphs_from_page = re.findall(self.PARAGRAPH_PATTERN, page, re.S)
        paragraphs_from_page = self.__stripped_list(paragraphs_from_page)

        for paragraph in paragraphs_from_page:
            if INITIAL_COURSES[0][2] not in paragraph:
                return CheckResult.wrong(
                    f'Main page should contain <p> element with information about course'
                )
            if INITIAL_COURSES[0][3] not in paragraph:
                return CheckResult.wrong(
                    f'Main page should contain <p> element with course duration'
                )
            if INITIAL_COURSES[0][4] not in paragraph:
                return CheckResult.wrong(
                    f'Main page should contain <p> element with course price'
                )
        return CheckResult.correct()

    def check_links_teacher_page(self) -> CheckResult:
        main_link = '/schedule/main/'

        try:
            page = self.read_page(
                self.get_url() + 'schedule/teacher_details/1')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the teacher_details page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if main_link not in links_from_page:
            return CheckResult.wrong(
                f'Course details page should contain <a> element with href {main_link}'
            )

        return CheckResult.correct()

    # stage 4
    def check_link_add_to_course(self) -> CheckResult:
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar))
        try:
            add_course_page_response = opener.open(
                self.get_url() + 'schedule/add_course/')
        except urllib.error.URLError:
            return CheckResult.wrong('Cannot connect to the page for applying to course.')

        add_course_page = add_course_page_response.read()

        csrf_options = re.findall(self.CSRF_PATTERN, add_course_page)

        if not csrf_options:
            return CheckResult.wrong(
                'Missing csrf_token in the upload page form')

        new_applying_to_course = {
            'name': self.NAME,
            'surname': self.SURNAME,
            'age': self.AGE,
            'course': self.COURSE,
            'csrfmiddlewaretoken': csrf_options[0],
        }

        add_course_page_response = requests.post(
            self.get_url() + 'schedule/add_course/',
            cookies=self.cookie_jar, data=new_applying_to_course
        )

        if add_course_page_response.url != self.get_url() + 'schedule/add_course/':
            return CheckResult.wrong(
                'After adding to the course you should be stay at the /schedule/add_course/ '
                'page')

        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT count(*) FROM schedule_student "
                f"WHERE name = '{self.NAME}' AND surname = '{self.SURNAME}' AND age = '{self.AGE}'"
            )
            students = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        if students[0][0] != 1:
            return CheckResult.wrong(
                'After applying to the course data is not saved in database')

        return CheckResult.correct()

    # stage 5
    def check_main_page_login_link(self):
        login_link = '/login/'
        try:
            page = self.read_page(self.get_url() + 'schedule/main/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if login_link not in links_from_page:
            return CheckResult.wrong(
                f'Main page should contain <a> element with href {login_link}'
            )

        return CheckResult.correct()

    def check_main_page_signup_link(self):
        signup_link = '/signup/'
        try:
            page = self.read_page(self.get_url() + 'schedule/main/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if signup_link not in links_from_page:
            return CheckResult.wrong(
                f'Main page should contain <a> element with href {signup_link}'
            )

        return CheckResult.correct()

    def check_signup(self) -> CheckResult:
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        try:
            response = opener.open(self.get_url() + 'signup/')
        except urllib.error.URLError:
            return CheckResult.wrong('Cannot connect to the signup page.')

        csrf_options = re.findall(
            b'<input[^>]+value="(?P<csrf>\w+)"[^>]*>', response.read()
        )
        if not csrf_options:
            return CheckResult.wrong('Missing csrf_token in the form')

        try:
            response = opener.open(
                self.get_url() + 'signup/',
                data=urllib.parse.urlencode({
                    'csrfmiddlewaretoken': csrf_options[0],
                    'username': self.USERNAME,
                    'password1': self.PASSWORD,
                    'password2': self.PASSWORD,
                }).encode()
            )

            if f'schedule' in response.url:
                return CheckResult.correct()
            return CheckResult.wrong('Cannot signup: problems with form')
        except urllib.error.URLError as err:
            return CheckResult.wrong(f'Cannot signup: {err.reason}')

    def check_login(self) -> CheckResult:
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar))
        try:
            response = opener.open(self.get_url() + 'login/')
        except urllib.error.URLError:
            return CheckResult.wrong('Cannot connect to the login page.')

        csrf_options = re.findall(
            b'<input[^>]+value="(?P<csrf>\w+)"[^>]*>', response.read()
        )
        if not csrf_options:
            return CheckResult.wrong('Missing csrf_token in the form')

        try:
            response = opener.open(
                self.get_url() + 'login/',
                data=urllib.parse.urlencode({
                    'csrfmiddlewaretoken': csrf_options[0],
                    'username': self.USERNAME,
                    'password': self.PASSWORD,
                }).encode(),
            )
            if 'login' not in response.url:
                return CheckResult.correct()
            return CheckResult.wrong('Cannot login: problems with form')
        except urllib.error.URLError as err:
            return CheckResult.wrong(f'Cannot login: {err.reason}')

    # stage 6
    def check_list_of_students(self):
        try:
            page = self.read_page(self.get_url() + 'schedule/course_details/1')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the course_details page.'
            )

        paragraphs_from_page = re.findall(self.PARAGRAPH_PATTERN, page, re.S)
        paragraphs_from_page = self.__stripped_list(paragraphs_from_page)

        for paragraph in paragraphs_from_page:
            if INITIAL_STUDENTS[0][1] in paragraph and INITIAL_STUDENTS[0][2] in paragraph:
                break
            if INITIAL_STUDENTS[1][1] in paragraph and INITIAL_STUDENTS[1][2] in paragraph:
                break
            if INITIAL_STUDENTS[2][1] in paragraph and INITIAL_STUDENTS[2][2]:
                return CheckResult.wrong(
                    'Check your list of student')

        return CheckResult.correct()

