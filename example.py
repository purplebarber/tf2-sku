from sku.parser import Sku

sku = Sku()
print(sku.name_to_sku("Vivid Plasma Pyro's Boron Beanie"))  # 30040;5;u16
print(sku.sku_to_name("30040;5;u16"))  # Vivid Plasma Pyro's Boron Beanie

item_object = Sku.sku_to_object("30040;5;u16")
print(item_object)  # prints the object as a JSON string
print(Sku.object_to_sku(item_object))  # 30040;5;u16
