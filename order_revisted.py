class Order:
    """Representation of a restaurant order."""

    def __init__(self) -> None:
        self.menu_items: list[MenuItem] = []

    def add_item(self, item: "MenuItem") -> None:
        """Add items to the list."""
        self.menu_items.append(item)

    def show(self) -> list[str]:
        """
        Returns a readable list of items.

        Converts each item in the order to a string.
        """
        return [str(item) for item in self.menu_items]
    
    def __len__(self) -> int:
        """Get the length of the order."""
        return len(self.menu_items)
    
    def __iter__(self):
        return iter(self.menu_items)

    def calculate_bill(self) -> float:
        """
        Calculates the total cost of the order.

        Returns the sum of the total price of all items.
        """
        return sum(item.get_total_price() for item in self.menu_items)

    def apply_discount(self, discount: float) -> float:
        """
        Applies a discount to the total order cost.

        Args:
            discount: The discount percentage as a decimal (e.g., 0.1 for 10%).

        Returns:
            The total cost after applying the discount.
        """
        total = self.calculate_bill()
        return total * (1 - discount)


class MenuItem:
    """Representation of a menu item."""

    def __init__(self, name: str, price: float, quantity: int) -> None:
        self.name = name
        self.price = price
        if self.price < 0:
            raise ValueError("Price cannot be negative!")
        self.quantity = quantity
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero!")

    def get_total_price(self) -> float:
        """Calculates and returns the total price of this item."""
        return self.price * self.quantity

    def change_price(self, fee: float) -> None:
        """
        Adjusts the price of an item.

        Args:
            fee: A multiplier factor to adjust the price.
        """
        self.price *= fee

    def __lt__(self, menuitem: "MenuItem") -> bool:
        if self.price < menuitem.price:
            return True
        elif self.price == menuitem.price:
            if self.quantity < menuitem.quantity:
                return True
            else:
                return False
        else:
            return False


class Appetizer(MenuItem):
    """Representation of an appetizer."""

    def __init__(
        self,
        name: str,
        price: float,
        quantity: int,
        for_sharing: bool
    ) -> None:
        super().__init__(name, price, quantity)
        self.for_sharing = for_sharing
        if self.for_sharing:
            self.change_price(0.95)

    def __str__(self) -> str:
        """Returns the name of the appetizer as a string."""
        return self.name


class MainCourse(MenuItem):
    """Representation of a main course."""

    def __init__(
        self,
        name: str,
        price: float,
        quantity: int,
        is_meet: bool
    ) -> None:
        super().__init__(name, price, quantity)
        self.is_meet = is_meet
        if self.is_meet:
            self.change_price(1.05)

    def __str__(self) -> str:
        """Returns the name of the main course as a string."""
        return self.name


class Beverage(MenuItem):
    """Representation of a beverage."""

    def __init__(
        self,
        name: str,
        price: float,
        quantity: int,
        size: str,
        has_sugar: bool
    ) -> None:
        super().__init__(name, price, quantity)
        self.size = size
        self.has_sugar = has_sugar
        if self.has_sugar:
            self.change_price(1.05)

    def __str__(self) -> str:
        """Returns the name of the beverage as a string."""
        return self.name


class Dessert(MenuItem):
    """Representation of a dessert."""

    def __init__(
        self,
        name: str,
        price: float,
        quantity: int,
        on_season: bool
    ) -> None:
        super().__init__(name, price, quantity)
        self.on_season = on_season
        if self.on_season:
            self.change_price(0.95)

    def __str__(self) -> str:
        """Returns the name of the dessert as a string."""
        return self.name
    
class MenuIterable:
    """Implements an iterator with all items in an order."""
    def __init__(self, order: "Order", method: int) -> None:
        self.order = order
        self.method = method

    def __iter__(self):
        """Returns the iterator instance."""
        if self.method == 1:
            return MenuMainIterator(self.order)
        else:
            return MenuSecondIterator(self.order)

class MenuMainIterator:
    def __init__(self, order: "Order") -> None:
        """Initializes the iterator instance."""
        self.order = order
        self.current_item_index = 0
    
    def __next__(self):
        if self.current_item_index == len(self.order):
            raise StopIteration
        actual = self.order.menu_items[self.current_item_index]
        self.current_item_index += 1
        return actual

    def __iter__(self):
        return self
    
class MenuSecondIterator:
    def __init__(self, order: "Order") -> None:
        """Initializes the iterator instance."""
        self.order = order
        self.current_item_index = 0
        self.list = self.order.menu_items.sort()
        print(f"###########{self.list}")
    
    def __next__(self):
        if self.current_item_index == len(self.order):
            raise StopIteration
        actual = self.order.menu_items[self.current_item_index]
        self.current_item_index += 1
        return f"{actual.name:<20} | {actual.price:>6.2f} | {actual.quantity:^5}"

    def __iter__(self):
        return self


if __name__ == '__main__':
    # Crear una nueva orden
    order = Order()

    # Agregar 10 elementos de diferentes categorías
    items = [
        Appetizer(name="Nachos", price=5.50, quantity=2, for_sharing=True),
        Appetizer(name="Spring Rolls", price=4.00, quantity=3, for_sharing=False),
        MainCourse(name="Steak", price=15.00, quantity=1, is_meet=True),
        MainCourse(name="Vegetarian Pasta", price=12.00, quantity=2, is_meet=False),
        Beverage(name="Coca Cola", price=2.50, quantity=2, size="Medium", has_sugar=True),
        Beverage(name="Orange Juice", price=3.00, quantity=1, size="Large", has_sugar=False),
        Dessert(name="Cheesecake", price=6.00, quantity=1, on_season=True),
        Dessert(name="Chocolate Cake", price=5.50, quantity=1, on_season=False),
        Appetizer(name="Garlic Bread", price=3.50, quantity=1, for_sharing=True),
        Beverage(name="Latte", price=4.00, quantity=1, size="Small", has_sugar=False)
    ]
    for item in items:
        order.add_item(item)

    # Mostrar los elementos en la orden
    print('*'*20)
    print("Impresión reto 3:")
    print('*'*20)
    print(order.show())


    # Nuevo ejercicio de iteradores e iterables
    print("-" * 35)
    print("Impresión reto 8:")
    print("ITEMS EN LA ORDEN:")
    print("Nombre               | Precio | Cant ")
    print("-" * 35)
    iterable = MenuIterable(order, method=2)
    for i in iterable:
        print(i)

    # Clase Order como iterable
    print('*'*20)
    print("Clase Order como iterable:")
    print("ITEMS EN LA ORDEN:")
    print('*'*20)
    for item in order:
        print(item)

