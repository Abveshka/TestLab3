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


def test_remove_whole_product_without_quantity(cart, phone):
    cart.add(phone, 4)
    cart.remove("prod_102")
    assert cart.items == {}


def test_remove_partially(cart, phone):
    cart.add(phone, 5)
    cart.remove("prod_102", 2)
    assert cart.items == {"prod_102": 3}


def test_remove_exact_quantity_removes_product(cart, phone):
    cart.add(phone, 3)
    cart.remove("prod_102", 3)
    assert cart.items == {}


def test_remove_more_than_in_cart_removes_product(cart, phone):
    cart.add(phone, 3)
    cart.remove("prod_102", 100)
    assert cart.items == {}


def test_remove_missing_product(cart):
    with pytest.raises(KeyError):
        cart.remove("unknown")


@pytest.mark.parametrize("bad", [0, -2, 1.5, "1", True])
def test_remove_invalid_quantity(cart, phone, bad):
    cart.add(phone, 3)
    with pytest.raises(ValueError):
        cart.remove("prod_102", bad)
    assert cart.items == {"prod_102": 3}


def test_total_empty_cart(cart):
    assert cart.total() == 0


def test_total_several_products(cart, phone, case):
    cart.add(phone, 2)  # 1000
    cart.add(case, 3)  # 60
    assert cart.total() == 1060


def test_total_after_remove(cart, phone, case):
    cart.add(phone, 2)
    cart.add(case, 3)
    cart.remove("prod_103")
    assert cart.total() == 1000


def test_items_returns_copy(cart, phone):
    cart.add(phone, 1)
    cart.items["prod_102"] = 999
    assert cart.items == {"prod_102": 1}


def test_promo_default_is_none(cart):
    assert cart.promo is None


def test_subtotal_ignores_promo(cart, phone):
    cart.add(phone, 2)
    cart.apply_promo("SALE10")
    assert cart.subtotal() == 1000


def test_apply_promo_discounts_total(cart, phone):
    cart.add(phone, 2)
    cart.apply_promo("SALE10")
    assert cart.promo == "SALE10"
    assert cart.total() == 900


def test_promo_is_case_and_space_insensitive(cart, phone):
    cart.add(phone, 2)
    cart.apply_promo("  sale20 ")
    assert cart.promo == "SALE20"
    assert cart.total() == 800


def test_promo_applies_to_items_added_later(cart, phone, case):
    cart.apply_promo("HALF")
    cart.add(phone, 2)
    cart.add(case, 5)
    assert cart.total() == 550


def test_new_promo_replaces_old(cart, phone):
    cart.add(phone, 2)
    cart.apply_promo("SALE10")
    cart.apply_promo("SALE20")
    assert cart.total() == 800


def test_remove_promo(cart, phone):
    cart.add(phone, 2)
    cart.apply_promo("SALE10")
    cart.remove_promo()
    assert cart.promo is None
    assert cart.total() == 1000


def test_promo_on_empty_cart(cart):
    cart.apply_promo("SALE10")
    assert cart.total() == 0


def test_total_is_rounded_to_cents(cart):
    cart.add(Product("prod_1", "Книга", 19.99, 5), 1)
    cart.apply_promo("SALE10")
    assert cart.total() == 17.99


@pytest.mark.parametrize("bad", ["UNKNOWN", "", "   ", "SALE", None, 10])
def test_apply_invalid_promo(cart, phone, bad):
    cart.add(phone, 2)
    cart.apply_promo("SALE10")
    with pytest.raises(ValueError):
        cart.apply_promo(bad)
    # неудачная попытка не сбрасывает прежний промокод
    assert cart.promo == "SALE10"
    assert cart.total() == 900
