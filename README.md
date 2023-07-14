# tf2-sku
 A python library that parses TF2 item SKU to the item's name and vice versa

## Features
- Parses SKU to item's name
- Parses item's name to SKU
- Parses SKU to an item object
- Parses an item object to SKU

## Usage
```python
from sku.parser import Sku

sku = Sku()
print(sku.name_to_sku("Vivid Plasma Pyro's Boron Beanie"))  # 30040;5;u16
print(sku.sku_to_name("30040;5;u16"))  # Vivid Plasma Pyro's Boron Beanie

item_object = Sku.sku_to_object("30040;5;u16")
print(item_object)  # prints the object as a JSON string
print(Sku.object_to_sku(item_object))  # 30040;5;u16
```

## Acknowledgements
[idinium96's tf2autobot](https://github.com/TF2Autobot/tf2autobot) for the item name schema\
Inspired by [Niclason's node-tf2-sku](https://github.com/Nicklason/node-tf2-sku) and [TryHardDo's TF2Sku](https://github.com/TryHardDo/TF2Sku/tree/master)
