from typing import Union, TypeAlias
from model_objects import Product, ProductQuantity

ProductQuantities: TypeAlias = dict[Product, Union[int, float]]


class ShoppingCart:

    def __init__(self) -> None:
        self._items: list[ProductQuantity] = []
        self._product_quantities: ProductQuantities = {}

    @property
    def items(self) -> list[ProductQuantity]:
        return self._items

    def add_item(self, product: Product) -> None:
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(
        self
    ) -> dict[Product, Union[int, float]]:
        return self._product_quantities

    def add_item_quantity(
        self,
        product: Product,
        quantity: Union[int, float]
    ) -> None:
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity
