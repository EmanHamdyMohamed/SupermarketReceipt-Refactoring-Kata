import math
from model_objects import SpecialOfferType, Discount


class OfferHandler:
    OFFER_TYPE_AMOUNTS = {
        SpecialOfferType.THREE_FOR_TWO: 3,
        SpecialOfferType.TWO_FOR_AMOUNT: 2,
        SpecialOfferType.FIVE_FOR_AMOUNT: 5,
        SpecialOfferType.TEN_PERCENT_DISCOUNT: 1
    }
    
    def _handle_three_for_two(self, product, quantity, unit_price, offer, offer_amount):
        if int(quantity) <= 2:
            return None
        qualified_offer_count = math.floor(int(quantity) / offer_amount)
        discount_amount = quantity * unit_price - (
                    (qualified_offer_count * 2 * unit_price) + int(quantity) % 3 * unit_price)
        disc_description = "3 for 2"
        discount = Discount(product, disc_description, -discount_amount)
        return discount

    def _handle_two_for_amount(self, product, quantity, unit_price, offer, offer_amount):
        quantity_as_int = int(quantity)
        if quantity_as_int < offer_amount:
            return None
        total = offer.argument * (quantity_as_int / offer_amount) + quantity_as_int % 2 * unit_price
        discount_n = unit_price * quantity - total
        disc_description = "2 for " + str(offer.argument)
        discount = Discount(product, disc_description, -discount_n)
        return discount

    def _handle_five_for_amount(self, product, quantity, unit_price, offer, offer_amount):
        quantity_as_int = int(quantity)
        if quantity_as_int < 5:
            return None
        qualified_offer_count = math.floor(int(quantity) / offer_amount)
        discount_total = unit_price * quantity - (
                    offer.argument * qualified_offer_count + quantity_as_int % 5 * unit_price)
        disc_description = str(offer_amount) + " for " + str(offer.argument)
        discount = Discount(product, disc_description, -discount_total)
        return discount

    def _handle_ten_percent_discount(self, product, quantity, unit_price, offer, offer_amount):
        disc_description = str(offer.argument) + "% off"
        discount = Discount(product, disc_description, -quantity * unit_price * offer.argument / 100.0)
        return discount

    def apply_offers(self, cart, offers, catalog, receipt):                    
        offer_discount_handler = {
            SpecialOfferType.TWO_FOR_AMOUNT: self._handle_two_for_amount,
            SpecialOfferType.THREE_FOR_TWO: self._handle_three_for_two,
            SpecialOfferType.TEN_PERCENT_DISCOUNT: self._handle_ten_percent_discount,
            SpecialOfferType.FIVE_FOR_AMOUNT: self._handle_five_for_amount
        }
        for p, quantity in cart.product_quantities.items():
            offer = offers.get(p)
            if not offer:
                continue
            unit_price = catalog.unit_price(p)
            offer_amount = self.OFFER_TYPE_AMOUNTS.get(offer.offer_type, 1)
            calculate_discount = offer_discount_handler.get(offer.offer_type)
            discount = calculate_discount(p, quantity, unit_price, offer, offer_amount)
            if discount:
                receipt.add_discount(discount)
