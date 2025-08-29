import math
from typing import Any, Optional, Union
from model_objects import SpecialOfferType, Discount, Product, Offer


class OfferHandler:
    def __init__(self) -> None:
        self.offers_config: dict[SpecialOfferType, dict[str, Any]] = {
            SpecialOfferType.THREE_FOR_TWO: {
                "quantity": 3,
                "calculation_handler": self._handle_three_for_two,
                "description_temp": "3 for 2"
            },
            SpecialOfferType.TWO_FOR_AMOUNT: {
                "quantity": 2,
                "calculation_handler": self._handle_two_for_amount,
                "description_temp": "2 for {argument}"
            },
            SpecialOfferType.FIVE_FOR_AMOUNT: {
                "quantity": 5,
                "calculation_handler": self._handle_five_for_amount,
                "description_temp": "5 for {argument}"
            },
            SpecialOfferType.TEN_PERCENT_DISCOUNT: {
                "quantity": 1,
                "calculation_handler": self._handle_ten_percent_discount,
                "description_temp": "{argument}% off"
            }
        }

    def get_offer_config(self, offer_type: SpecialOfferType) -> dict[str, Any]:
        return self.offers_config.get(offer_type, {})

    def format_description(
        self,
        offer_type: SpecialOfferType,
        offer_argument: Union[int, float],
        offer_amount: int
    ) -> str:
        offer_config = self.get_offer_config(offer_type)
        temp = offer_config.get('description_temp', 'Special offer')
        try:
            return temp.format(
                argument=offer_argument, 
                offer_amount=offer_amount
            )
        except (KeyError, ValueError):
            return temp

    def _handle_three_for_two(
        self,
        quantity: Union[int, float],
        unit_price: Union[int, float],
        argument: Union[int, float],
        offer_amount: int
    ) -> Optional[float]:
        if int(quantity) <= 2:
            return None
        qualified_offer_count = math.floor(int(quantity) / offer_amount)
        discount_amount = quantity * unit_price - (
                    (qualified_offer_count * 2 * unit_price) + int(quantity) % 3 * unit_price)
        return -discount_amount

    def _handle_two_for_amount(
        self,
        quantity: Union[int, float],
        unit_price: Union[int, float],
        argument: Union[int, float],
        offer_amount: int
    ) -> Optional[float]:
        quantity_as_int = int(quantity)
        if quantity_as_int < offer_amount:
            return None
        total = argument * (quantity_as_int / offer_amount) + quantity_as_int % 2 * unit_price
        discount_n = unit_price * quantity - total
        return (-discount_n)

    def _handle_five_for_amount(
        self,
        quantity: Union[int, float],
        unit_price: Union[int, float],
        argument: Union[int, float],
        offer_amount: int
    ) -> Optional[float]:
        quantity_as_int = int(quantity)
        if quantity_as_int < 5:
            return None
        qualified_offer_count = math.floor(int(quantity) / offer_amount)
        discount_total = unit_price * quantity - (
                    argument * qualified_offer_count + quantity_as_int % 5 * unit_price)
        return (-discount_total)

    def _handle_ten_percent_discount(
        self,
        quantity: Union[int, float],
        unit_price: Union[int, float],
        argument: Union[int, float],
        offer_amount: int
    ) -> float:
        discount_amount = -quantity * unit_price * argument / 100.0
        return discount_amount

    def apply_offers(
        self,
        cart: Any,
        offers: dict[Product, Offer],
        catalog: Any,
        receipt: Any
    ) -> None:
        for p, quantity in cart.product_quantities.items():
            offer = offers.get(p)
            if not offer:
                continue

            unit_price = catalog.unit_price(p)
            offer_config = self.get_offer_config(offer.offer_type)
            offer_amount = offer_config['quantity']
            calculate_discount = offer_config['calculation_handler']
            discount_amount = calculate_discount(
                quantity, unit_price, offer.argument, offer_amount
            )
            disc_description = self.format_description(
                offer.offer_type, offer.argument, offer_amount
            )
            if discount_amount:
                receipt.add_discount(Discount(p, disc_description, discount_amount))
