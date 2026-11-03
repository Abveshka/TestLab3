import pytest

from src.cart import ShoppingCart
from src.product import Product


# Добавляем комментарий для теста кеша
@pytest.fixture
def phone():
    return Product("prod_102", "Смартфон", 500, 10)


@pytest.fixture
def case():
    return Product("prod_103", "Чехол", 20, 5)


@pytest.fixture
def cart():
    return ShoppingCart()


def test_product_created():
    p = Product("prod_1", "Книга", 15.5, 3)
    assert (p.id, p.name, p.price, p.stock) == ("prod_1", "Книга", 15.5, 3)


def test_product_negative_price():
    with pytest.raises(ValueError):
        Product("prod_1", "Книга", -1, 3)


def test_product_negative_stock():
    with pytest.raises(ValueError):
        Product("prod_1", "Книга", 10, -1)


def test_add_new_product(cart, phone):
    cart.add(phone, 2)
    assert cart.items == {"prod_102": 2}


def test_add_existing_product_increases_quantity(cart, phone):
    cart.add(phone, 2)
    cart.add(phone, 3)
    assert cart.items == {"prod_102": 5}


def test_add_exactly_stock(cart, phone):
    cart.add(phone, 10)
    assert cart.items["prod_102"] == 10


def test_add_more_than_stock(cart, phone):
    with pytest.raises(ValueError):
        cart.add(phone, 11)
    assert cart.items == {}


def test_add_more_than_stock_with_existing(cart, phone):
    cart.add(phone, 8)
    with pytest.raises(ValueError):
        cart.add(phone, 3)
    assert cart.items == {"prod_102": 8}


@pytest.mark.parametrize("bad", [0, -1, 1.5, "2", None, True])
def test_add_invalid_quantity(cart, phone, bad):
    with pytest.raises(ValueError):
        cart.add(phone, bad)
    assert cart.items == {}
