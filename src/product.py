class Product:
    def __init__(self, id: str, name: str, price: float, stock: int):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if stock < 0:
            raise ValueError("Остаток на складе не может быть отрицательным")
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
