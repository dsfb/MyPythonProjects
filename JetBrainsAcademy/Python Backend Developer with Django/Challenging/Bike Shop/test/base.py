import urllib
import re
import sqlite3
import requests
from hstest import CheckResult, DjangoTest


TEST_FRAMES = [
    ('black', 30),
    ('white', 40),
    ('pink', 0),
]

TEST_SEATS = [
    ('black', 5),
    ('white', 55),
    ('pink', 0),
]

TEST_TIRES = [
    ('city', 2),
    ('road', 0),
    ('country', 0),
]

TEST_BASKET = 40

TEST_BIKES = [
    ('city bike', 2, 1, 1, True, 'Great bike for a city ride!'),
    ('road bike', 1, 2, 1, False, 'Excellent for longer trips in nature!'),
    ('lady bike', 2, 2, 2, False, 'Excellent for ladies!'),
]

TEST_ORDERS = [
    (1, 'P', 'Robin', 'Black', '123456789'),
    (2, 'R', 'Suzie', 'Towson', '987654321'),
]
LI_PATTERN = '<li>(.+?)</li>'
H2_PATTERN = '<h2>(.+?)</h2>'
P_PATTERN = '<p>(.+?)</p>'


class BikeShopTest(DjangoTest):
    use_database = True

    def check_create_frame_model(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.executemany(
                'INSERT INTO shop_frame (`color`, `quantity`) VALUES (?, ?)',
                TEST_FRAMES
            )
            connection.commit()

            cursor.execute('SELECT `color`, `quantity` FROM shop_frame')
            result = cursor.fetchall()

            for frame in TEST_FRAMES:
                if frame not in result:
                    return CheckResult.wrong('Check if your Frame model is defined as per requirements.')
            return CheckResult.correct()

        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def check_create_seat_model(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.executemany(
                'INSERT INTO shop_seat (`color`, `quantity`) VALUES (?, ?)',
                TEST_SEATS
            )
            connection.commit()

            cursor.execute('SELECT `color`, `quantity` FROM shop_seat')
            result = cursor.fetchall()

            for seat in TEST_SEATS:
                if seat not in result:
                    return CheckResult.wrong('Check if your Seat model is defined as per requirements.')
            return CheckResult.correct()

        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def check_create_tire_model(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.executemany(
                'INSERT INTO shop_tire (`type`, `quantity`) VALUES (?, ?)',
                TEST_TIRES
            )
            connection.commit()

            cursor.execute('SELECT `type`, `quantity` FROM shop_tire')
            result = cursor.fetchall()

            for tire in TEST_TIRES:
                if tire not in result:
                    return CheckResult.wrong('Check if your Tire model is defined as per requirements.')
            return CheckResult.correct()

        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def check_create_basket_model(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'INSERT INTO shop_basket (`quantity`) VALUES ({TEST_BASKET})'
            )
            connection.commit()

            cursor.execute('SELECT `quantity` FROM shop_basket')
            result = cursor.fetchone()

            if TEST_BASKET not in result:
                return CheckResult.wrong('Check if your Basket model is defined as per requirements.')
            return CheckResult.correct()

        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def check_create_bike_model(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.executemany(
                'INSERT INTO shop_bike (`name`, `frame_id`, `tire_id`, `seat_id`, `has_basket`, `description`) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                TEST_BIKES
            )
            connection.commit()

            cursor.execute('SELECT `name`, `frame_id`, `tire_id`, `seat_id`, `has_basket`, `description` FROM shop_bike')
            result = cursor.fetchall()

            for bike in TEST_BIKES:
                if bike not in result:
                    return CheckResult.wrong('Check if your Bike model is defined as per requirements.')
            return CheckResult.correct()

        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def check_create_order_model(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.executemany(
                'INSERT INTO shop_order (`bike_id`, `status`, `name`, `surname`, `phone_number`) '
                'VALUES (?, ?, ?, ?, ?)',
                TEST_ORDERS
            )
            connection.commit()

            cursor.execute('SELECT `bike_id`, `status`, `name`, `surname`, `phone_number` FROM shop_order')
            result = cursor.fetchall()

            for order in TEST_ORDERS:
                if order not in result:
                    return CheckResult.wrong('Check if your Order model is defined as per requirements.')
            return CheckResult.correct()

        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def _get_all_bikes(self):
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            bikes = cursor.execute('SELECT `name`, `frame_id`, `tire_id`, `seat_id`, `has_basket`, `description` FROM shop_bike').fetchall()
            return bikes
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))


    def check_bike_list(self) -> CheckResult:
        try:
            page = self.read_page(self.get_url() + 'bikes/')
            li_elements = re.findall(LI_PATTERN, page, re.S)
            p_elements = re.findall(P_PATTERN, page, re.S)
            bikes = self._get_all_bikes()
            for index, bike in enumerate(bikes):
                name = f'{bike[0]}'
                if len(li_elements) == 0:
                    the_list = p_elements
                else:
                    the_list = li_elements
                for element in the_list:
                    if name in element:
                        return CheckResult.correct()
                return CheckResult.wrong(
                    'Main page should include list of all bikes\' names inside "li" or "p" tags.'
                )

        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the /bikes/ page.'
            )

    def _get_bike_info(self, frame_index, tire_index, seat_index):
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            frame_color = cursor.execute(f'SELECT `color` FROM shop_frame WHERE `id` == {frame_index}').fetchone()[0]
            tire_type = cursor.execute(f'SELECT `type` FROM shop_tire WHERE `id` == {tire_index}').fetchone()[0]
            seat_color = cursor.execute(f'SELECT `color` FROM shop_seat WHERE `id` == {seat_index}').fetchone()[0]
            return {'frame_color': frame_color, 'tire_type': tire_type, 'seat_color': seat_color}
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def check_bike_detail(self) -> CheckResult:
        bikes = self._get_all_bikes()
        try:
            for index, bike in enumerate(bikes):
                page_no = str(index + 1)
                page = self.read_page(self.get_url() + f'bikes/{page_no}/')
                h2_elements = re.findall(H2_PATTERN, page, re.S)
                p_elements = re.findall(P_PATTERN, page, re.S)
                name = bike[0]
                frame_index = bike[1]
                tire_index = bike[2]
                seat_index = bike[3]
                bike_info = self._get_bike_info(frame_index, tire_index, seat_index)
                has_basket = bike[4]
                baskets = {True: 'yes',
                           False: 'no'}
                basket_info = baskets[has_basket]
                description = bike[5]
                if name not in h2_elements:
                    return CheckResult.wrong(
                        'The page should include bike\'s name inside a "h2" tag.'
                    )
                if f'frame: {bike_info["frame_color"]}' not in p_elements:
                    return CheckResult.wrong(
                        'The page should include information on bike\'s frame inside a "p" tag.'
                    )
                if f'tires: {bike_info["tire_type"]}' not in p_elements:
                    return CheckResult.wrong(
                        'The page should include information on bike\'s tires inside a "p" tag.'
                    )
                if f'seat: {bike_info["seat_color"]}' not in p_elements:
                    return CheckResult.wrong(
                        'The page should include information on bike\'s seat inside a "p" tag.'
                    )
                if f'basket: {basket_info}' not in p_elements:
                    return CheckResult.wrong(
                        'The page should include information on whether bike has a basket inside a "p" tag.'
                    )
                if f'description: {description}' not in p_elements:
                    return CheckResult.wrong(
                        'The page should include bike\'s description inside "p" tag.'
                    )
            return CheckResult.correct()
        except urllib.error.URLError:
            return CheckResult.wrong(
                    'Cannot connect to the page.'
                )

    def check_bike_links(self) -> CheckResult:
        try:
            page = self.read_page(self.get_url() + 'bikes/')
            li_elements = re.findall(LI_PATTERN, page, re.S)
            p_elements = re.findall(P_PATTERN, page, re.S)
            bikes = self._get_all_bikes()
            for index, bike in enumerate(bikes):
                link = f'/bikes/{index + 1}'
                if len(li_elements) == 0:
                    the_list = p_elements
                else:
                    the_list = li_elements
                for element in the_list:
                    if link in element:
                        return CheckResult.correct()
                return CheckResult.wrong(
                    'Each bike\'s name listed on /bikes/ page should be a hyperlink to the relevant bike page!'
                )
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the /bikes/ page.'
            )

    def _check_bike_parts_quantities(self, index, bike):
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            frame_quantity = cursor.execute(f'SELECT `quantity` FROM shop_frame WHERE `id` == {bike[1]}').fetchone()[0]
            tire_quantity = cursor.execute(f'SELECT `quantity` FROM shop_tire WHERE `id` == {bike[2]}').fetchone()[0]
            seat_quantity = cursor.execute(f'SELECT `quantity` FROM shop_seat WHERE `id` == {bike[3]}').fetchone()[0]
            has_basket = cursor.execute(f'SELECT `has_basket` FROM shop_bike WHERE `id` == {index + 1}').fetchone()[0]
            basket_quantity = cursor.execute('SELECT `quantity` FROM shop_basket').fetchone()[0]
            return {'frame': frame_quantity, 'tire': tire_quantity, 'seat': seat_quantity, 'has_basket': has_basket, 'basket': basket_quantity}
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def _check_enough_parts(self, index, bike):
        parts = self._check_bike_parts_quantities(index, bike)
        if parts['has_basket'] and parts['basket'] < 1:
            return False
        elif parts['frame'] < 1 or parts['tire'] < 2 or parts['seat'] < 1:
            return False
        else:
            return True

    def _check_field(self, page, field_name):
        return all(x in page.lower() for x in ["<input", f'name="{field_name.lower()}"'])

    def _check_button(self, page, button_value):
        button = f'{button_value}'.lower()
        return button in page.lower()

    def check_form_enough_parts(self) -> CheckResult:
        try:
            bikes = self._get_all_bikes()
            for index, bike in enumerate(bikes):
                page_no = str(index + 1)
                page = self.read_page(self.get_url() + f'bikes/{page_no}/')
                enough_parts = self._check_enough_parts(index, bike)
                p_tags = re.findall(P_PATTERN, page, re.S)
                if enough_parts:
                    form_p_tags = p_tags[-3:]
                    labels = ('name', 'surname', 'phone number')
                    for ind, label in enumerate(labels):
                        value = f'your {label}'
                        try:
                            if value not in form_p_tags[ind]:
                                return CheckResult.wrong(f'Field "{label}" is to have label "{value}"')
                        except IndexError:
                            return CheckResult.wrong(
                                'Make sure the form is correct. Check if "p" tags are used to display form elements and the form has three fields.')
                        except AttributeError:
                            return CheckResult.wrong('Make sure all the fields are present in the form')
                    if self._check_field(page, "name") and \
                            self._check_field(page, "surname") and \
                            self._check_field(page, "phone_number"):
                        if self._check_button(page, "Order"):
                            return CheckResult.correct()
                        else:
                            return CheckResult.wrong(
                                'The form should include "Order" button.'
                            )
                    else:
                        return CheckResult.wrong(
                            'The form should include three fields - name, surname and phone number.'
                        )
                else:
                    sentence = "Unfortunately, this bike is currently not available"
                    if not any(sentence in p_tag for p_tag in p_tags):
                        return CheckResult.wrong(
                            'If bike parts are not available, the page should have text "Unfortunately this bike is currently not available" in bold inside a <p> tag.'
                        )
            return CheckResult.correct()
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the page.'
            )

    def _order_object_created(self):
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT `name`, `surname`, `phone_number` FROM shop_order')
            result = cursor.fetchall()
            if ('Susan', 'Brown', '123456789') in result:
                return True
            else:
                return CheckResult.wrong(
                    'Order object should be created once button "Order" is clicked.'
                )
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def _bike_parts_quantities_updated(self, preorder_parts, updated_parts):
        if (updated_parts['frame'] == preorder_parts['frame'] - 1) and (updated_parts['tire'] == preorder_parts['tire'] - 2) and \
                (updated_parts['seat'] == preorder_parts['seat'] - 1) and (updated_parts['basket'] == preorder_parts['basket'] - 1 if preorder_parts['has_basket'] else updated_parts['basket'] == preorder_parts['basket']):
            return True
        else:
            return False

    def check_order_processing(self) -> CheckResult:
        bikes = self._get_all_bikes()
        for index, bike in enumerate(bikes):
            if self._check_enough_parts(index, bike):
                try:
                    page_no = str(index + 1)
                    bike_page = requests.get(self.get_url(f'bikes/{page_no}/'))
                except urllib.error.URLError:
                    return CheckResult.wrong(
                        'Cannot connect to the bike page.'
                    )
                preorder_parts = self._check_bike_parts_quantities(index, bike)
                requests.post(self.get_url(f'bikes/{page_no}/'), cookies={"csrftoken": bike_page.cookies.get("csrftoken")},
                                  data={"csrfmiddlewaretoken": bike_page.cookies.get("csrftoken"),
                                        "name": "Susan", "surname": "Brown", "phone_number": "123456789"})
                updated_parts = self._check_bike_parts_quantities(index, bike)
                order_object_created = self._order_object_created()
                bike_parts_updated = self._bike_parts_quantities_updated(preorder_parts, updated_parts)
                if not order_object_created:
                    return CheckResult.wrong(
                        'Check if order object is created correctly.'
                    )
                elif not bike_parts_updated:
                    return CheckResult.wrong(
                        'Check if bike parts get updated once an order is made.'
                    )
        return CheckResult.correct()

    def _get_all_orders(self):
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            orders = cursor.execute('SELECT `bike_id`, `status`, `name`, `surname`, `phone_number` FROM shop_order').fetchall()
            return orders
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def check_order_page_created(self):
        orders = self._get_all_orders()
        for index, order in enumerate(orders):
            order_no = str(index + 1)
            try:
                order_page = self.read_page(self.get_url() + f'order/{order_no}/')
                h2_elements = re.findall(H2_PATTERN, order_page, re.S)
                p_elements = re.findall(P_PATTERN, order_page, re.S)
                if 'Thanks for your order!' not in h2_elements:
                    return CheckResult.wrong(
                        'Order page should include "h2" tag with text "Thanks for your order!"'
                    )
                elif f"Your order number is {order_no}. We will call you once your bike is ready!" not in p_elements:
                    return CheckResult.wrong(
                        'Order page should include "p" tag with text "Your order number is order_no. We will call you once your bike is ready!"'
                    )
                else:
                    return CheckResult.correct()
            except urllib.error.URLError:
                return CheckResult.wrong(
                    'Cannot connect to the order page.'
                )
