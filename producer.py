"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.products = products
        self.republish_wait_time = republish_wait_time
        self.marketplace = marketplace

        Thread.__init__(self, **kwargs)

    def run(self):
        id_prod = self.marketplace.register_producer()
        for _ in range(100000):
            for i in range(len(self.products)):
                prod_type, quantity, rest_time = self.products[i]
                for j in range(quantity):
                    if self.marketplace.publish(id_prod, prod_type):
                        time.sleep(rest_time)
                    else:
                        time.sleep(self.republish_wait_time)
                        j = j - 1
