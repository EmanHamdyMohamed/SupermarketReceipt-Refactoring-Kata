from model_objects import Offer
from receipt import Receipt
from offer_handler import OfferHandler


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}
        self.offer_handler = OfferHandler()

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        # Use OfferHandler instead of cart.handle_offers
        self.offer_handler.apply_offers(
            the_cart, self.offers, self.catalog, receipt)

        return receipt
