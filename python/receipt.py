
from typing import Union
from model_objects import Product, Discount


class ReceiptItem:
    def __init__(
        self,
        product: Product,
        quantity: Union[int, float],
        price: Union[int, float],
        total_price: Union[int, float]
    ) -> None:
        self.product: Product = product
        self.quantity: Union[int, float] = quantity
        self.price: Union[int, float] = price
        self.total_price: Union[int, float] = total_price


class Receipt:
    def __init__(self) -> None:
        self._items: list[ReceiptItem] = []
        self._discounts: list[Discount] = []

    def total_price(self) -> Union[int, float]:
        total = 0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    def add_product(
        self,
        product: Product,
        quantity: Union[int, float],
        price: Union[int, float],
        total_price: Union[int, float]
    ) -> None:
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount: Discount) -> None:
        self._discounts.append(discount)

    @property
    def items(self) -> list[ReceiptItem]:
        return self._items[:]

    @property
    def discounts(self) -> list[Discount]:
        return self._discounts[:]
