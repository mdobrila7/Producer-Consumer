"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import currentThread, Lock
import random

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.place_order_lock = Lock()

        self.quantity = queue_size_per_producer
        self.carts = {}
        self.producers = [{}, {}]
        self.product_to_producer = {}

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        rand = random.randint(1, 10000)
        while rand in self.carts:
            rand = random.randint(1, 10000)
        self.producers[0][rand] = []
        self.producers[1][rand] = []
        return rand

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if self.quantity == len(self.producers[0][producer_id]):
            return False
        self.producers[0][producer_id].append(product)
        self.product_to_producer[product] = producer_id
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        rand = random.randint(1, 10000)
        while rand in self.carts:
            rand = random.randint(1, 10000)
        self.carts[rand] = []
        return rand

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        found = False
        for i in self.producers[0]:
            if product in self.producers[0][i]:
                self.carts[cart_id].append(product)
                self.producers[0][i].remove(product)
                found = True
                break
        if found:
            return True
        for i in self.producers[1]:
            removed = self.producers[1][i]
            if product in removed:
                self.carts[cart_id].append(product)
                removed.remove(product)
                found = True
                break
        return found

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.producers[1][self.product_to_producer[product]].append(product)
        self.carts[cart_id].remove(product)
        return True

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        for i in range(len(self.carts[cart_id])):
            self.place_order_lock.acquire()
            print(f"{currentThread().getName()} bought {self.carts[cart_id][i]}")
            self.place_order_lock.release()
