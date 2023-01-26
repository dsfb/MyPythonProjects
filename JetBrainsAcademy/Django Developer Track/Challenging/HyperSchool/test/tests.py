# -*- coding: utf-8 -*-
from hstest import dynamic_test

from .base import HyperSchoolTest


class HyperSchoolTestRunner(HyperSchoolTest):

    funcs = [
        # 1 task
        HyperSchoolTest.check_create_courses,
        # 2 task
        HyperSchoolTest.check_main_page_header,
        HyperSchoolTest.check_main_search_courses,
        HyperSchoolTest.check_link_to_course,
        HyperSchoolTest.check_main_courses_count,
        # 3 task
        HyperSchoolTest.check_links_course_page,
        HyperSchoolTest.check_course_info_displayed,
        HyperSchoolTest.check_links_teacher_page,
        # 4 task
        HyperSchoolTest.check_link_add_to_course,
        # 5 task
        HyperSchoolTest.check_main_page_login_link,
        HyperSchoolTest.check_main_page_signup_link,
        HyperSchoolTest.check_signup,
        HyperSchoolTest.check_login,
        # 6 task
        HyperSchoolTest.check_list_of_students

    ]

    @dynamic_test(data=funcs)
    def test(self, func):
        return func(self)


if __name__ == '__main__':
    HyperSchoolTestRunner().run_tests()