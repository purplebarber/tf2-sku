from sku.models import itemClass as itemClass
from typing import List
from collections import deque
import requests
from bs4 import BeautifulSoup as bs
import sqlite3
import pkg_resources

DB_FILE = pkg_resources.resource_filename(__name__, 'data/data.db')


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
    def _create_tables_if_not_exist(conn):
        cursor = conn.cursor()
        # Create the "sku" and "name" tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sku (
                sku TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS name (
                name TEXT PRIMARY KEY,
                sku TEXT NOT NULL
            )
        """)
        conn.commit()

    @staticmethod
    def get_json_data(sku: str = str(), name: str = str()) -> str:
        conn = sqlite3.connect(DB_FILE)
        Sku._create_tables_if_not_exist(conn)  # Ensure tables exist
        cursor = conn.cursor()

        if sku:
            cursor.execute("SELECT name FROM sku WHERE sku=?", (sku,))
            result = cursor.fetchone()
            return result[0] if result else ""

        if name:
            cursor.execute("SELECT sku FROM name WHERE name=?", (name,))
            result = cursor.fetchone()
            return result[0] if result else ""

        conn.close()
        return ""

    @staticmethod
    def update_json_data(sku: str, name: str) -> None:
        conn = sqlite3.connect(DB_FILE)
        Sku._create_tables_if_not_exist(conn)  # Ensure tables exist
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO sku (sku, name) VALUES (?, ?)", (sku, name))
            cursor.execute("INSERT INTO name (name, sku) VALUES (?, ?)", (name, sku))
        except sqlite3.IntegrityError:
            # If the name already exists, update the corresponding sku instead of inserting
            cursor.execute("UPDATE name SET sku=? WHERE name=?", (sku, name))

        conn.commit()
        conn.close()

    @staticmethod
    def update_autobot_pricelist() -> None:
        req = requests.get("https://autobot.tf/json/pricelist-array").json()

        conn = sqlite3.connect(DB_FILE)
        Sku._create_tables_if_not_exist(conn)  # Ensure tables exist
        cursor = conn.cursor()

        for item in req.get("items"):
            name = item.get("name")
            sku = item.get("sku")

            # Check if the name already exists in the database
            cursor.execute("SELECT sku FROM name WHERE name=?", (name,))
            existing_sku = cursor.fetchone()

            # If the name exists, update the existing entry
            if existing_sku:
                existing_sku = existing_sku[0]
                if existing_sku != sku:
                    # Update the SKU for the existing name
                    cursor.execute("UPDATE name SET sku=? WHERE name=?", (sku, name))
            else:
                # If the name doesn't exist, insert a new entry
                cursor.execute("INSERT OR IGNORE INTO name (name, sku) VALUES (?, ?)", (name, sku))
                cursor.execute("INSERT OR IGNORE INTO sku (sku, name) VALUES (?, ?)", (sku, name))

        conn.commit()
        conn.close()
