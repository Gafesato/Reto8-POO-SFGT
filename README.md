# Reto8-POO-SFGT

Esta solución tiene el objetivo de implementar el patrón Iterable-Iterador a la clase Order la cual contiene una lista de items, que son los elementos de la orden.

## Clases Principales

### **1. `Order`**
La clase `Order` representa un pedido en el restaurante. Actúa como una colección de elementos (`MenuItem`) y permite iterar sobre ellos utilizando la clase `MenuIterable`.

**Métodos importantes:**
- `add_item(item: MenuItem)`: Agrega un ítem a la orden.
- `calculate_bill()`: Calcula el total del pedido sumando los precios de todos los ítems.
- `apply_discount(discount: float)`: Aplica un descuento al total del pedido.
- `__len__()`: Devuelve la cantidad de elementos en la orden. Lo cual esta la tuve que agregar para este reto y así poder hacer este código:
```python
def __next__(self):
        if self.current_item_index == len(self.order):      # <----
            raise StopIteration
        actual = self.order.menu_items[self.current_item_index]
        self.current_item_index += 1
        return actual
```

**Ejemplo de uso:**
Esta es la misma entrada de elementos que usé en el Reto 3.
```python
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
```

---

### **2. `MenuIterable`**
Esta clase permite iterar sobre los elementos de la orden utilizando dos iteradores diferentes que he creado.
En el constructor, llamo a un argumento el cual define el iterador que se usará.

**Constructor:**
```python
MenuIterable(order: Order, method: int)
```
- `order`: La orden que se recorrerá.
- `method`: Determina qué iterador se usará.
  - `1` → Usa `MenuMainIterator`
  - `2 u otro número` → Usa `MenuSecondIterator`

**Código**
```python
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
```

---

### **3. `MenuMainIterator`**
Este iterador recorre los elementos de la orden y los devuelve en su forma de objeto `MenuItem`.

**Código**
```python
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
```
---
### **4. `MenuSecondIterator`**
Este iterador devuelve los elementos de la orden en un formato más legible, similar a una tabla de datos. En esencia es el mismo que el anterior, solo que además itera los elementos por orden de precio.
Por lo que en la clase `MenuItem` se tuvo que añadir el método `__lt__()` que se vió en clase para poder establecer un orden entre las clases, en este caso, será quien tenga menor precio el más pequeño.
**Impresión formateada**
```python
return f"{actual.name:<20} | {actual.price:>6.2f} | {actual.quantity:^5}"
```
**Método __lt__()**
```python
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
```
**Salida**
```bash
Impresión reto 8:
ITEMS EN LA ORDEN:
Nombre               | Precio | Cant
-----------------------------------
###########None
Coca Cola            |   2.62 |   2
Orange Juice         |   3.00 |   1
Garlic Bread         |   3.32 |   1
Latte                |   4.00 |   1
Spring Rolls         |   4.00 |   3
Nachos               |   5.22 |   2
Chocolate Cake       |   5.50 |   1
Cheesecake           |   5.70 |   1
Vegetarian Pasta     |  12.00 |   2
Steak                |  15.75 |   1
```

**Segundo iterador**
```python
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
```

---

## `Order` como un Iterable
La clase `Order` por sí misma no es iterable, pero al añadir el método `__iter__()` , se puede recorrer utilizando `for` como si fuera una lista.

**Método en Order**
```python
def __iter__(self):
    return iter(self.menu_items)
```
**Recorriendo Order con un bucle**
Aquí podemos ver que la impresión es por orden a como se agregó a la clase Order, donde el iterador personalizado si hace un buen sorting...
```python
for item in order:
    print(item)
```
```bash
********************
Clase Order como iterable:
ITEMS EN LA ORDEN:
********************
Nachos
Spring Rolls
Steak
Vegetarian Pasta
Coca Cola
Orange Juice
Cheesecake
Chocolate Cake
Garlic Bread
Latte
```
---
