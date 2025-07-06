from sku import Sku, itemClass, get_schema

# Example 1: Convert SKU to item name
print("=== SKU to Name Examples ===")
sku1 = "5021;6"  # Mann Co. Supply Crate Key
name1 = Sku.sku_to_name(sku1)
print(f"SKU: {sku1} -> Name: {name1}")

sku2 = "30469;5;u14"  # Unusual Horace with Nuts n' Bolts effect
name2 = Sku.sku_to_name(sku2)
print(f"SKU: {sku2} -> Name: {name2}")

sku3 = "211;11;australium"  # Strange Australium Grenade Launcher
name3 = Sku.sku_to_name(sku3)
print(f"SKU: {sku3} -> Name: {name3}")

# Example 2: Convert item name to SKU
print("\n=== Name to SKU Examples ===")
name4 = "Burning Flames Team Captain"
sku4 = Sku.name_to_sku(name4)
print(f"Name: {name4} -> SKU: {sku4}")

name5 = "Hot Professional Killstreak Polter-Guised Tomislav (Factory New)"
sku5 = Sku.name_to_sku(name5)
print(f"Name: {name5} -> SKU: {sku5}")

# Example 3: Working with itemClass objects
print("\n=== Working with itemClass ===")
item = itemClass()
item.Defindex = 424  # Tomislav
item.Quality = 11    # Strange
item.Killstreak = 3  # Professional Killstreak
item.Australium = False
item.Craftable = True

sku6 = Sku.object_to_sku(item)
print(f"Item object -> SKU: {sku6}")

# Convert back
item_back = Sku.sku_to_object(sku6)
print(f"Defindex: {item_back.Defindex}, Quality: {item_back.Quality}, Killstreak: {item_back.Killstreak}")

# Example 4: Non-standard items
print("\n=== Special Items ===")
# Decorated weapon
sku7 = "15003;15;u14;w2;pk47"
name7 = Sku.sku_to_name(sku7)
print(f"Decorated weapon SKU: {sku7} -> Name: {name7}")

# Chemistry Set
name8 = "Collector's Professional Killstreak Phlogistinator Chemistry Set"
sku8 = Sku.name_to_sku(name8)
print(f"Chemistry Set Name: {name8} -> SKU: {sku8}")

# Example 5: Getting schema information
print("\n=== Schema Information ===")
schema = get_schema()
print(f"Schema version: {schema.version}")
print(f"Number of items in schema: {len(schema.raw['schema']['items'])}")
print(f"Number of particle effects: {len(schema.effects)}")
print(f"Number of paint kits: {len(schema.paintkits)}")

# Example 6: Looking up specific items in schema
print("\n=== Schema Lookups ===")
# Get item by defindex
item_data = schema.get_item_by_defindex(5021)
if item_data:
    print(f"Item with defindex 5021: {item_data['item_name']}")

# Get quality name
quality_name = schema.get_quality_by_id(11)
print(f"Quality ID 11 is: {quality_name}")

# Get effect name
effect_name = schema.get_effect_by_id(13)
print(f"Effect ID 13 is: {effect_name}")

# Example 7: Updating schema (optional)
# Note: By default, schema is loaded from cache or autobot.tf
# You can force an update like this:
# update_schema()  # Uses autobot.tf by default
# update_schema(api_key="YOUR_STEAM_API_KEY", use_autobot=False)  # Use Steam API

print("\n=== Configuration ===")
print(f"Schema cache location: {schema.SCHEMA_CACHE_FILE}")
print(f"Cache duration: {schema.CACHE_DURATION} seconds ({schema.CACHE_DURATION / 3600} hours)")
