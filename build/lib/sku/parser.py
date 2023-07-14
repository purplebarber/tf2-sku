from sku.models import itemClass as itemClass
from typing import List
from collections import deque
import requests
from bs4 import BeautifulSoup as bs
from json import load, dump
import pkg_resources

DATA_FILE = pkg_resources.resource_filename(__name__, 'data/data.json')


class Sku:
    @staticmethod
    def object_to_sku(item: itemClass) -> str:
        sku_parts: List[str] = [str(item.Defindex), str(int(item.Quality))]

        if item.Effect is not None:
            sku_parts.append(f"u{item.Effect}")

        if item.Australium:
            sku_parts.append("australium")

        if not item.Craftable:
            sku_parts.append("uncraftable")

        if item.Wear is not None:
            sku_parts.append(f"w{item.Wear}")

        if item.PaintKit is not None:
            sku_parts.append(f"pk{item.PaintKit}")

        if item.ElevatedQuality == 11:
            sku_parts.append("strange")

        if item.Killstreak != 0:
            sku_parts.append(f"kt-{item.Killstreak}")

        if item.Target is not None:
            sku_parts.append(f"td-{item.Target}")

        if item.Festive:
            sku_parts.append("festive")

        if item.CraftNum is not None:
            sku_parts.append(f"n{item.CraftNum}")

        if item.CrateSn is not None:
            sku_parts.append(f"c{item.CrateSn}")

        if item.Output is not None:
            sku_parts.append(f"od-{item.Output}")

        if item.OutputQuality is not None:
            sku_parts.append(f"oq-{item.OutputQuality}")

        return ";".join(sku_parts)

    @staticmethod
    def sku_to_object(sku: str) -> itemClass:
        item = itemClass()
        sku_parts = deque(sku.split(';'))

        if sku_parts and sku_parts[0].isdigit():
            item.Defindex = int(sku_parts.popleft())

        if sku_parts and sku_parts[0].isdigit():
            item.Quality = int(sku_parts.popleft())

        while sku_parts:
            Sku.change_attribute(sku_parts.popleft(), item)

        return item

    @staticmethod
    def change_attribute(attribute: str, item: itemClass) -> None:
        attr = attribute.replace("-", "")

        if attr == "uncraftable":
            item.Craftable = False

        elif attr == "australium":
            item.Australium = True

        elif attr == "festive":
            item.Festive = True

        elif attr == "strange":
            item.ElevatedQuality = 11

        elif attr.startswith("kt") and attr[2:].isdigit():
            item.Killstreak = int(attr[2:])

        elif attr.startswith("u") and attr[1:].isdigit():
            item.Effect = int(attr[1:])

        elif attr.startswith("pk") and attr[2:].isdigit():
            item.PaintKit = int(attr[2:])

        elif attr.startswith("w") and attr[1:].isdigit():
            item.Wear = int(attr[1:])

        elif attr.startswith("td") and attr[2:].isdigit():
            item.Target = int(attr[2:])

        elif attr.startswith("n") and attr[1:].isdigit():
            item.CraftNum = int(attr[1:])

        elif attr.startswith("c") and attr[1:].isdigit():
            item.CrateSn = int(attr[1:])

        elif attr.startswith("od") and attr[2:].isdigit():
            item.Output = int(attr[2:])

        elif attr.startswith("oq") and attr[2:].isdigit():
            item.OutputQuality = int(attr[2:])

    @staticmethod
    def sku_to_name(sku: str) -> str:
        json_data = Sku.get_json_data(sku=sku)
        if json_data:
            return json_data

        req = requests.get(f"https://www.tf2autobot.com/items/{sku}")
        title = bs(req.text, "html.parser").find("title").text

        Sku.update_json_data(sku, title.lstrip())
        return title.lstrip()

    @staticmethod
    def name_to_sku(name: str) -> str:
        json_data = Sku.get_json_data(name=name)
        if json_data:
            return json_data

        req = requests.get(f"https://www.tf2autobot.com/items/{name}")
        title = bs(req.text, "html.parser").find("h3").text

        Sku.update_json_data(title.lstrip(), name)
        return title.lstrip()

    @staticmethod
    def get_json_data(sku: str = str(), name: str = str()) -> str:
        with open(DATA_FILE, "r") as f:
            data = load(f)

        if sku:
            return data.get("sku").get(sku)

        if name:
            return data.get("name").get(name)

        return str()

    @staticmethod
    def update_json_data(sku: str, name: str) -> None:
        with open(DATA_FILE, "r") as f:
            data = load(f)

        data.get("sku").update({sku: name})
        data.get("name").update({name: sku})

        with open(DATA_FILE, "w") as f:
            dump(data, f, indent=2)

    @staticmethod
    def update_autobot_pricelist() -> None:
        req = requests.get("https://autobot.tf/json/pricelist-array").json()
        new_data_dict = {
            "name": dict(),
            "sku": dict()
        }

        for item in req.get("items"):
            name = item.get("name")
            sku = item.get("sku")
            new_data_dict.get("name").update({name: sku})
            new_data_dict.get("sku").update({sku: name})

        with open(DATA_FILE, "w") as f:
            dump(new_data_dict, f, indent=2)
