from model_objects import Product, ProductUnit, SpecialOfferType
from tests.fake_catalog import FakeCatalog
from shopping_cart import ShoppingCart
from teller import Teller


def create_catalog_with_product(product_name, unit, price, quantity=1):
    """Create a catalog with a product added multiple times."""
    catalog = FakeCatalog()
    product = Product(product_name, unit)
    for _ in range(quantity):
        catalog.add_product(product, price)
    return catalog, product


def create_cart_with_product(product, quantity):
    """Create a shopping cart with a specific product and quantity."""
    cart = ShoppingCart()
    cart.add_item_quantity(product, quantity)
    return cart


def create_teller_with_offer(catalog, offer_type, product, argument):
    """Create a teller with a special offer."""
    teller = Teller(catalog)
    teller.add_special_offer(offer_type, product, argument)
    return teller


def setup_three_for_two_test(cart_quantity=3):
    """Common setup for three-for-two offer tests."""
    catalog, toothbrush = create_catalog_with_product(
        "toothbrush", ProductUnit.EACH, 1, 4)
    cart = create_cart_with_product(toothbrush, cart_quantity)
    teller = create_teller_with_offer(
        catalog, SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
    return catalog, toothbrush, cart, teller


def setup_two_for_amount_test(cart_quantity=3):
    """Common setup for two-for-amount offer tests."""
    catalog, toothbrush = create_catalog_with_product(
        "toothbrush", ProductUnit.EACH, 1, 4)
    cart = create_cart_with_product(toothbrush, cart_quantity)
    teller = create_teller_with_offer(
        catalog, SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 0)
    return catalog, toothbrush, cart, teller


def setup_five_for_amount_test(cart_quantity=5):
    """Common setup for five-for-amount offer tests."""
    catalog, toothbrush = create_catalog_with_product(
        "toothbrush", ProductUnit.EACH, 1, 5)
    cart = create_cart_with_product(toothbrush, cart_quantity)
    teller = create_teller_with_offer(
        catalog, SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 1)
    return catalog, toothbrush, cart, teller
