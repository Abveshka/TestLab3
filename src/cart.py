from src.product import Product


def _check_quantity(quantity) -> None:
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Количество должно быть целым числом больше 0")


class ShoppingCart:
    """Корзина покупок: хранит пары {id_товара: количество}"""

    def __init__(self):
        self._items: dict[str, int] = {}
        self._products: dict[str, Product] = {}

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

    def total(self) -> float:
        return sum(
            self._products[pid].price * qty for pid, qty in self._items.items()
        )

    def _delete(self, product_id: str) -> None:
        del self._items[product_id]
        del self._products[product_id]