"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.retry_wait_time = retry_wait_time
        self.marketplace = marketplace

        self.carts_ids = []
        self.current_cart = 0

        Thread.__init__(self, **kwargs)

    def run(self):
        commands = ["remove", "add"]
        for i in range(len(self.carts)):
            self.carts_ids.append(self.marketplace.new_cart())
            for j in range(len(self.carts[i])):
                quantity = self.carts[i][j]["quantity"]
                while quantity > 0:
                    command = self.carts[i][j]["product"]
                    if self.carts[i][j]["type"] == commands[0]:
                        if self.marketplace.remove_from_cart(self.carts_ids[self.current_cart],\
                            command):
                            quantity = quantity - 1
                        else:
                            time.sleep(self.retry_wait_time)
                    else:
                        if self.marketplace.add_to_cart(self.carts_ids[self.current_cart], command):
                            quantity = quantity - 1
                        else:
                            time.sleep(self.retry_wait_time)
            self.marketplace.place_order(self.carts_ids[self.current_cart])
            self.current_cart = self.current_cart + 1
