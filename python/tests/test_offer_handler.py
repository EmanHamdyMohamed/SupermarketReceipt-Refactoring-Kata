from model_objects import Offer, ProductUnit, SpecialOfferType
from offer_handler import OfferHandler
from receipt import Receipt
from shopping_cart import ShoppingCart
from .helpers import create_catalog_with_product


def test_offer_handler():
    catalog, toothbrush = create_catalog_with_product(
        "toothbrush", ProductUnit.EACH, 1, 1
    )
    # Create test data
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)

    offers = {toothbrush: Offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)}

    receipt = Receipt()

    # Test the handler directly
    offer_handler = OfferHandler()
    offer_handler.apply_offers(cart, offers, catalog, receipt)

    # Assertions
    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].discount_amount == -1


def test_zero_quantity():
    """Test that offers don't apply to zero quantities."""
    catalog, toothbrush = create_catalog_with_product(
        "toothbrush",
        ProductUnit.EACH, 1, 1
    )
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 0)  # Zero quantity

    offers = {toothbrush: Offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)}
    receipt = Receipt()

    offer_handler = OfferHandler()
    offer_handler.apply_offers(cart, offers, catalog, receipt)

    assert len(receipt.discounts) == 0
