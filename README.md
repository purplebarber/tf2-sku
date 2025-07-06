# tf2-sku

A Python library for parsing Team Fortress 2 item SKUs to item names and vice versa.

## Features
- Convert SKUs to item names
- Convert item names to SKUs

## Installation

```bash
pip install tf2-sku-to-name
```

## Quick Start

```python
from sku import Sku

# Convert SKU to name
sku = "5021;6"
name = Sku.sku_to_name(sku)
print(name)  # Output: Mann Co. Supply Crate Key

# Convert name to SKU
name = "Burning Flames Team Captain"
sku = Sku.name_to_sku(name)
print(sku)  # Output: 378;5;u13

# Working with item objects
from sku import itemClass

item = itemClass()
item.Defindex = 424
item.Quality = 11
item.Killstreak = 3

sku = Sku.object_to_sku(item)
print(sku)  # Output: 424;11;kt-3
```

## Advanced Usage

### Schema Management

The library automatically manages TF2 schema data:

```python
from sku import get_schema, update_schema

# Get the current schema instance
schema = get_schema()

# Access schema data
item = schema.get_item_by_defindex(5021)
print(item['item_name'])  # Mann Co. Supply Crate Key

# Force update schema (by default uses autobot.tf)
update_schema()

# Or use Steam API (requires API key)
update_schema(api_key="YOUR_STEAM_API_KEY", use_autobot=False)
```

## Installation
```bash
pip install tf2-sku-to-name
```

## Acknowledgements
[TF2Autobot's node-tf2-schema](https://github.com/TF2Autobot/node-tf2-schema) for the original JavaScript implementation\
[idinium96's tf2autobot](https://github.com/TF2Autobot/tf2autobot) for the item name schema\
Inspired by [Nicklason's node-tf2-sku](https://github.com/Nicklason/node-tf2-sku) and [TryHardDo's TF2Sku](https://github.com/TryHardDo/TF2Sku/tree/master)
