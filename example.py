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
