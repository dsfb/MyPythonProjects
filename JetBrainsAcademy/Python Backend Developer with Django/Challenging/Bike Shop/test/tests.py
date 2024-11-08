from hstest import dynamic_test

from .base import BikeShopTest


class BikeShopTestRunner(BikeShopTest):

    funcs = [
        # 1 stage
        BikeShopTest.check_create_frame_model,
        BikeShopTest.check_create_seat_model,
        BikeShopTest.check_create_tire_model,
        BikeShopTest.check_create_basket_model,
        BikeShopTest.check_create_bike_model,
        BikeShopTest.check_create_order_model,

        # 2 stage
        BikeShopTest.check_bike_list,

        # 3 stage
        BikeShopTest.check_bike_detail,
        BikeShopTest.check_bike_links,

        # 4 stage
        BikeShopTest.check_form_enough_parts,

        # 5 stage
        BikeShopTest.check_order_processing,
        BikeShopTest.check_order_page_created
    ]

    @dynamic_test(data=funcs)
    def test(self, func):
        return func(self)


if __name__ == '__main__':
    BikeShopTestRunner().run_tests()
