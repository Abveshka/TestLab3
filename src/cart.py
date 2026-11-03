from src.product import Product


PROMO_CODES = {
    "SALE10": 10,
    "SALE20": 20,
    "HALF": 50,
}


def _check_quantity(quantity) -> None:
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Количество должно быть целым числом больше 0")


class ShoppingCart:
    """Хранит пары {id_товара: количество}"""

    def __init__(self):
        self._items: dict[str, int] = {}
        self._products: dict[str, Product] = {}
        self._promo: str | None = None

    @property
    def items(self) -> dict[str, int]:
        """Копия содержимого корзины (чтобы снаружи её нельзя было испортить)"""
        return dict(self._items)

    def add(self, product: Product, quantity: int) -> None:
        _check_quantity(quantity)
        new_quantity = self._items.get(product.id, 0) + quantity
        if new_quantity > product.stock:
            raise ValueError(
                f"Нельзя добавить {quantity} шт.: на складе только {product.stock}"
            )
        self._items[product.id] = new_quantity
        self._products[product.id] = product

    def remove(self, product_id: str, quantity: int | None = None) -> None:
        if product_id not in self._items:
            raise KeyError(f"Товара {product_id} нет в корзине")

        if quantity is None:
            self._delete(product_id)
            return

        _check_quantity(quantity)
        current = self._items[product_id]
        if quantity >= current:
            self._delete(product_id)
        else:
            self._items[product_id] = current - quantity

    @property
    def promo(self) -> str | None:
        return self._promo

    def apply_promo(self, code: str) -> None:
        if not isinstance(code, str):
            raise ValueError("Промокод должен быть строкой")
        normalized = code.strip().upper()
        if normalized not in PROMO_CODES:
            raise ValueError(f"Неизвестный промокод: {code}")
        self._promo = normalized

    def remove_promo(self) -> None:
        self._promo = None

    def subtotal(self) -> float:
        return sum(
            self._products[pid].price * qty for pid, qty in self._items.items()
        )

    def total(self) -> float:
        subtotal = self.subtotal()
        if self._promo is None:
            return subtotal
        discount = PROMO_CODES[self._promo]
        return round(subtotal * (100 - discount) / 100, 2)

    def _delete(self, product_id: str) -> None:
        del self._items[product_id]
        del self._products[product_id]
