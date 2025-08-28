import pytest

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from .helpers import (
    setup_five_for_amount_test,
    setup_three_for_two_test,
    setup_two_for_amount_test,
    setup_multiple_products_test
)


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.975 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity


def test_three_for_two_offer():
    """Test that discount is applied on 3 items and pay for 2."""
    _, _, cart, teller = setup_three_for_two_test()

    receipt = teller.checks_out_articles_from(cart)

    # Should pay price for 2 item instead of 3
    assert 2 == receipt.total_price()
    receipt_item = receipt.items[0]
    assert 3 == receipt_item.quantity


def test_two_for_amount_offer():
    _, _, cart, teller = setup_two_for_amount_test()

    receipt = teller.checks_out_articles_from(cart)

    # Should pay price for 1 item instead of 3
    assert 1 == receipt.total_price()
    receipt_item = receipt.items[0]
    assert 3 == receipt_item.quantity


def test_five_for_amount_offer():
    _, _, cart, teller = setup_five_for_amount_test()

    receipt = teller.checks_out_articles_from(cart)

    # Should pay price for 1 item instead of 5
    assert 1 == receipt.total_price()
    receipt_item = receipt.items[0]
    assert 5 == receipt_item.quantity


def test_three_for_two_offer_not_enough_items():
    """Test that discount is not applied when less than 3 items."""
    _, _, cart, teller = setup_three_for_two_test(cart_quantity=2)

    receipt = teller.checks_out_articles_from(cart)

    # Should pay full price for 2 items (no discount)
    assert 2 == receipt.total_price()
    receipt_item = receipt.items[0]
    assert 2 == receipt_item.quantity
    assert 0 == len(receipt.discounts)


def test_two_for_amount_offer_not_enough_items():
    """Test that discount is not applied when less than 2 items."""
    _, _, cart, teller = setup_two_for_amount_test(cart_quantity=1)

    receipt = teller.checks_out_articles_from(cart)

    # Should pay full price for 1 item (no discount)
    assert 1 == receipt.total_price()
    receipt_item = receipt.items[0]
    assert 1 == receipt_item.quantity
    assert 0 == len(receipt.discounts)


def test_five_for_amount_offer_not_enough_items():
    """Test that discount is not applied when less than 5 items."""
    _, _, cart, teller = setup_five_for_amount_test(cart_quantity=3)

    receipt = teller.checks_out_articles_from(cart)

    # Should pay full price for 3 items (no discount)
    assert 3 == receipt.total_price()
    receipt_item = receipt.items[0]
    assert 3 == receipt_item.quantity
    assert 0 == len(receipt.discounts)


def test_apply_offer_multiple_same_product():
    _, _, cart, teller = setup_three_for_two_test(7)

    receipt = teller.checks_out_articles_from(cart)

    # Should pay price for 5 item instead of 7
    assert 5 == receipt.total_price()
    receipt_item = receipt.items[0]
    assert 7 == receipt_item.quantity


def test_three_for_two_boundary():
    _, _, cart, teller = setup_three_for_two_test(2)

    receipt = teller.checks_out_articles_from(cart)

    # Should pay price for 2 item
    assert 2 == receipt.total_price()
    receipt_item = receipt.items[0]
    assert 2 == receipt_item.quantity


def test_multiple_products_different_offers():
    """Test multiple products with different types of offers applied."""
    _, _, _, _, _,_,  cart, teller = setup_multiple_products_test()

    # Process checkout
    receipt = teller.checks_out_articles_from(cart)

    # Verify all items are present
    assert 5 == len(receipt.items)

    # Verify discounts are applied
    assert 4 == len(receipt.discounts)

    # Verify total price calculation
    # Toothbrush: 3 items, pay for 2
    # Apples: 2kg * 2 = 4.00, 10% off = 3.60
    # Milk: 2 items, pay 2.50 instead of 3 = 2.50
    # Bread: 5 items, pay 4 instead of 5 = 4
    # Soap: 1 items, pay .50
    # Total: 2 + 3.60 + 2.50 + 4 = 12.10
    expected_total = 2 + 3.60 + 2.50 + 4 + 0.50
    assert expected_total == receipt.total_price()
