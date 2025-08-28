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
        "toothbrush", ProductUnit.EACH, 1, 10)
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


def setup_multiple_products_test():
    """Common setup for multiple products with different offers test."""

    # Create catalog with multiple products
    catalog = FakeCatalog()

    # Product 1: Toothbrush with 3-for-2 offer
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1)

    # Product 2: Apples with 10% discount
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 2)

    # Product 3: Milk with 2-for-amount offer
    milk = Product("milk", ProductUnit.EACH)
    catalog.add_product(milk, 1.50)

    # Product 4: Bread with 5-for-amount offer
    bread = Product("bread", ProductUnit.EACH)
    catalog.add_product(bread, 1)
    
        
    # Product 5: Soap without offer
    soap = Product("soap", ProductUnit.EACH)
    catalog.add_product(soap, 0.50)

    # Create teller and add different offers
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, milk, 2.50)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, bread, 4.00)

    # Create cart with multiple products
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)  # Should get 3-for-2 discount
    cart.add_item_quantity(apples, 2.0)    # Should get 10% discount
    cart.add_item_quantity(milk, 2)        # Should get 2-for-amount discount
    cart.add_item_quantity(bread, 5)       # Should get 5-for-amount discount
    cart.add_item_quantity(soap, 1)       # Should get no offer

    return catalog, toothbrush, apples, milk, bread, soap, cart, teller
