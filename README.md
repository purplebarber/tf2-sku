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
print(sku.name_to_sku("Non-Craftable Tour of Duty Ticket"))  # 30040;5;u16
print(sku.sku_to_name("725;6;uncraftable"))  # Vivid Plasma Pyro's Boron Beanie

item_object = Sku.sku_to_object("725;6;uncraftable")
print(item_object)  # prints the object as a JSON string
print(Sku.object_to_sku(item_object))  # 30040;5;u16

sku.update_autobot_pricelist()  # Gets item schema from autobot.tf and updates the json file
# this is only needed if you want to update the data file (like after a TF2 game update)
# otherwise, you can just use the data file that comes with the package
```

## Model
```json
{
  "Defindex": 725,
  "Quality": 6,
  "Craftable": false,
  "Killstreak": 0,
  "Australium": false,
  "Festive": false,
  "Effect": null,
  "PaintKit": null,
  "Wear": null,
  "ElevatedQuality": null,
  "Target": null,
  "CraftNum": null,
  "CrateSn": null,
  "Output": null,
  "OutputQuality": null
}
```

## Installation
```bash
pip install tf2-sku-to-name
```

## Acknowledgements
[idinium96's tf2autobot](https://github.com/TF2Autobot/tf2autobot) for the item name schema\
Inspired by [Nicklason's node-tf2-sku](https://github.com/Nicklason/node-tf2-sku) and [TryHardDo's TF2Sku](https://github.com/TryHardDo/TF2Sku/tree/master)
