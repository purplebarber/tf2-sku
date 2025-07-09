from sku.models import itemClass
from sku.schema import Schema
from typing import List
from collections import deque
import re

# Initialize schema (will load from cache or fetch from autobot.tf by default)
_schema = None

def get_schema(api_key=None, use_autobot=True):
    """Get or initialize the schema instance"""
    global _schema
    if _schema is None:
        _schema = Schema(api_key=api_key, use_autobot=use_autobot)
    return _schema


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
    def sku_to_name(sku: str, proper_name: bool = True) -> str:
        """Convert SKU to item name using the schema"""
        item = Sku.sku_to_object(sku)
        schema = get_schema()
        
        item_dict = {
            'defindex': item.Defindex,
            'quality': item.Quality,
            'craftable': item.Craftable,
            'australium': item.Australium,
            'festive': item.Festive,
            'killstreak': item.Killstreak,
            'effect': item.Effect,
            'paintkit': item.PaintKit,
            'wear': item.Wear,
            'quality2': item.ElevatedQuality,
            'target': item.Target,
            'craftnumber': item.CraftNum,
            'crateseries': item.CrateSn,
            'output': item.Output,
            'outputQuality': item.OutputQuality,
            'tradable': True,  # SKUs don't track tradability
            'paint': None  # SKUs don't track paint
        }
        
        name = schema.get_name(item_dict, proper_name)
        if not name:
            raise ValueError(f"Failed to get name from SKU: {sku}")

        return name

    @staticmethod
    def name_to_sku(name: str) -> str:
        schema = get_schema()
        
        # Convert name to lowercase for processing
        name = name.strip()
        name_lower = name.lower()
        
        # Initialize item dict
        item = {
            'defindex': None,
            'quality': None,
            'craftable': True,
            'australium': False,
            'festive': False,
            'killstreak': 0,
            'effect': None,
            'paintkit': None,
            'wear': None,
            'quality2': None,
            'target': None,
            'craftnumber': None,
            'crateseries': None,
            'output': None,
            'outputQuality': None,
            'tradable': True,
            'paint': None
        }
        
        if any(x in name_lower for x in ['strange part:', 'strange cosmetic part:', 'strange filter:', 
                                         'strange count transfer tool', 'strange bacon grease']):
            schema_item = schema.get_item_by_item_name(name)
            if schema_item:
                item['defindex'] = schema_item['defindex']
                item['quality'] = schema_item.get('item_quality', 6)
                return Sku._dict_to_sku(item)
        
        # Process wear
        wears = {
            '(factory new)': 1,
            '(minimal wear)': 2,
            '(field-tested)': 3,
            '(well-worn)': 4,
            '(battle scarred)': 5
        }
        
        for wear_text, wear_value in wears.items():
            if wear_text in name_lower:
                name_lower = name_lower.replace(wear_text, '').strip()
                item['wear'] = wear_value
                break
        
        if 'strange(e)' in name_lower:
            item['quality2'] = 11
            name_lower = name_lower.replace('strange(e)', '').strip()
        
        if 'strange' in name_lower:
            item['quality'] = 11
            name_lower = name_lower.replace('strange', '').strip()
        
        name_lower = name_lower.replace('uncraftable', 'non-craftable')
        if 'non-craftable' in name_lower:
            name_lower = name_lower.replace('non-craftable', '').strip()
            item['craftable'] = False
        
        name_lower = name_lower.replace('untradeable', 'non-tradable').replace('untradable', 'non-tradable')
        if 'non-tradable' in name_lower:
            name_lower = name_lower.replace('non-tradable', '').strip()
            item['tradable'] = False
        
        if 'unusualifier' in name_lower:
            name_lower = name_lower.replace('unusual ', '').replace(' unusualifier', '').strip()
            item['defindex'] = 9258
            item['quality'] = 5
            
            schema_item = schema.get_item_by_item_name(name_lower)
            if schema_item:
                item['target'] = schema_item['defindex']
            
            return Sku._dict_to_sku(item)
        
        killstreaks = {
            'professional killstreak': 3,
            'specialized killstreak': 2,
            'killstreak': 1
        }
        
        for ks_text, ks_value in killstreaks.items():
            if ks_text in name_lower:
                name_lower = name_lower.replace(ks_text + ' ', '').strip()
                item['killstreak'] = ks_value
                break
        
        if 'australium' in name_lower and 'australium gold' not in name_lower:
            name_lower = name_lower.replace('australium', '').strip()
            item['australium'] = True
        
        if 'festivized' in name_lower and 'festivized formation' not in name_lower:
            name_lower = name_lower.replace('festivized', '').strip()
            item['festive'] = True
        
        exception = [
            'haunted ghosts', 'haunted phantasm jr', 'haunted phantasm', 'haunted metal scrap',
            'haunted hat', 'unusual cap', 'vintage tyrolean', 'vintage merryweather',
            'haunted kraken', 'haunted forever!', 'haunted cremation', 'haunted wick'
        ]
        
        quality_search = name_lower
        for ex in exception:
            if ex in name_lower:
                quality_search = name_lower.replace(ex, '').strip()
                break
        
        if quality_search not in exception:
            for quality_name, quality_id in schema.qualities.items():
                quality_lower = quality_name.lower()
                
                if quality_lower == "collector's" and "collector's" in quality_search and 'chemistry set' in quality_search:
                    continue
                
                if quality_lower == 'community' and quality_search.startswith('community sparkle'):
                    continue
                
                if quality_search.startswith(quality_lower):
                    name_lower = name_lower.replace(quality_lower, '').strip()
                    item['quality2'] = item['quality']
                    item['quality'] = quality_id
                    break
        
        for effect_name, effect_id in schema.effects.items():
            effect_lower = effect_name.lower()

            if effect_lower == 'stardust' and 'starduster' in name_lower:
                if 'starduster' in name_lower.replace('stardust', ''):
                    continue
            
            if effect_lower == 'showstopper' and 'taunt: ' not in name_lower and 'shred alert' not in name_lower:
                continue
            
            if effect_lower == 'smoking' and ('smoking skid lid' in name_lower or name_lower in ['smoking jacket', 'the smoking skid lid']):
                if not name_lower.startswith('smoking smoking'):
                    continue
            
            if effect_lower in ['haunted ghosts', 'pumpkin patch', 'stardust'] and item['wear']:
                continue
            
            if effect_lower == 'atomic' and ('subatomic' in name_lower or any(x in name_lower for x in ['bonk! atomic punch', 'atomic accolade'])):
                continue
            
            if effect_lower == 'spellbound' and ('taunt:' in name_lower or 'shred alert' in name_lower):
                continue
            
            if effect_lower == 'accursed' and 'accursed apparition' in name_lower:
                continue
            
            if effect_lower == 'haunted' and 'haunted kraken' in name_lower:
                continue
            
            if effect_lower == 'frostbite' and 'frostbite bonnet' in name_lower:
                continue
            
            if effect_lower == 'hot' and not item['wear']:
                continue
            
            if effect_lower == 'cool' and not item['wear']:
                continue
            
            if effect_lower in name_lower:
                name_lower = name_lower.replace(effect_lower, '').strip()
                item['effect'] = effect_id
                
                if effect_id == 4:  # Community Sparkle
                    if not item['quality']:
                        item['quality'] = 5
                elif item['quality'] != 5:
                    item['quality2'] = item['quality'] or item['quality2']
                    item['quality'] = 5
                
                break
        
        if item['wear']:
            for paintkit_name, paintkit_id in schema.paintkits.items():
                paintkit_lower = paintkit_name.lower()
                
                if 'mk.ii' in name_lower and 'mk.ii' not in paintkit_lower:
                    continue
                
                if '(green)' in name_lower and '(green)' not in paintkit_lower:
                    continue
                
                if 'chilly' in name_lower and 'chilly' not in paintkit_lower:
                    continue
                
                if paintkit_lower in name_lower:
                    name_lower = name_lower.replace(paintkit_lower, '').replace(' | ', '').strip()
                    item['paintkit'] = paintkit_id
                    
                    if item['effect'] is not None:
                        if item['quality'] == 5 and item['quality2'] == 11:
                            if 'strange(e)' not in name.lower():
                                item['quality'] = 11
                                item['quality2'] = None
                            else:
                                item['quality'] = 15
                        elif item['quality'] == 5 and not item['quality2']:
                            item['quality'] = 15
                    
                    if not item['quality']:
                        item['quality'] = 15
                    
                    break
            
            if 'war paint' not in name_lower and item['paintkit']:
                Sku._handle_weapon_skins(name_lower, item, schema)
        
        if '(paint: ' in name_lower:
            name_lower = name_lower.replace('(paint: ', '').replace(')', '').strip()
            
            paint_key = f"(paint: {name_lower})"
            if paint_key in schema.PAINT_MAPPINGS:
                item['paint'] = schema.PAINT_MAPPINGS[paint_key]
                # Remove paint name from name_lower
                for paint_name, paint_value in schema.paints.items():
                    if paint_value == item['paint'] and paint_name.lower() in name_lower:
                        name_lower = name_lower.replace(paint_name.lower(), '').strip()
                        break

        name_lower = Sku._process_special_items(name_lower, item, schema)
        
        name_lower = name_lower.replace(' series ', ' ').replace(' series#', ' #')
        
        if 'salvaged mann co. supply crate #' in name_lower:
            item['crateseries'] = int(name_lower[32:])
            item['defindex'] = 5068
            item['quality'] = 6
            return Sku._dict_to_sku(item)
        
        elif 'select reserve mann co. supply crate #' in name_lower:
            item['defindex'] = 5660
            item['crateseries'] = 60
            item['quality'] = 6
            return Sku._dict_to_sku(item)
        
        elif 'mann co. supply crate #' in name_lower:
            crateseries = int(name_lower[23:])
            
            if crateseries in [1, 3, 7, 12, 13, 18, 19, 23, 26, 31, 34, 39, 43, 47, 54, 57, 75]:
                item['defindex'] = 5022
            elif crateseries in [2, 4, 8, 11, 14, 17, 20, 24, 27, 32, 37, 42, 44, 49, 56, 71, 76]:
                item['defindex'] = 5041
            elif crateseries in [5, 9, 10, 15, 16, 21, 25, 28, 29, 33, 38, 41, 45, 55, 59, 77]:
                item['defindex'] = 5045
            
            item['crateseries'] = crateseries
            item['quality'] = 6
            return Sku._dict_to_sku(item)
        
        elif 'mann co. supply munition #' in name_lower:
            crateseries = int(name_lower[26:])
            item['defindex'] = schema.MUNITION_CRATES.get(crateseries)
            item['crateseries'] = crateseries
            item['quality'] = 6
            return Sku._dict_to_sku(item)
        
        number = None
        if '#' in name_lower:
            match = re.search(r'#(\d+)', name_lower)
            if match:
                number = match.group(1)
                name_lower = re.sub(r'#\d+', '', name_lower).strip()
        
        retired_key_names = [key['name'].lower() for key in schema.RETIRED_KEYS.values()]
        if name_lower in retired_key_names:
            for key in schema.RETIRED_KEYS.values():
                if key['name'].lower() == name_lower:
                    item['defindex'] = key['defindex']
                    item['quality'] = item['quality'] or 6
                    return Sku._dict_to_sku(item)
        
        schema_item = schema.get_item_by_item_name_with_the(name_lower)
        if not schema_item:
            raise ValueError(f"Failed to get SKU from name: {name}")
        
        item['defindex'] = schema_item['defindex']
        item['quality'] = item['quality'] or schema_item.get('item_quality', 6)
        
        if item['quality'] == 1 and item['defindex'] in schema.EXCLUSIVE_GENUINE:
            item['defindex'] = schema.EXCLUSIVE_GENUINE[item['defindex']]
        
        if schema_item.get('item_class') == 'supply_crate':
            item['crateseries'] = schema.crate_series_list.get(item['defindex'])
        elif number:
            item['craftnumber'] = int(number)
        
        return Sku._dict_to_sku(item)

    @staticmethod
    def _process_special_items(name_lower: str, item: dict, schema: Schema) -> str:

        if 'kit fabricator' in name_lower and item['killstreak'] > 1:
            name_lower = name_lower.replace('kit fabricator', '').strip()
            item['defindex'] = 20003 if item['killstreak'] > 2 else 20002
            
            if name_lower:
                schema_item = schema.get_item_by_item_name(name_lower)
                if schema_item:
                    item['target'] = schema_item['defindex']
                    item['quality'] = item['quality'] or schema_item.get('item_quality', 6)
            
            if not item['quality']:
                item['quality'] = 6
            
            item['output'] = 6526 if item['killstreak'] > 2 else 6523
            item['outputQuality'] = 6
        
        elif (("collector's" not in name_lower or 'strangifier chemistry set' not in name_lower) and 
              'chemistry set' in name_lower):
            name_lower = name_lower.replace("collector's ", '').replace('chemistry set', '').strip()
            
            if 'festive' in name_lower and 'a rather festive tree' not in name_lower:
                item['defindex'] = 20007
            else:
                item['defindex'] = 20006
            
            schema_item = schema.get_item_by_item_name(name_lower)
            if schema_item:
                item['output'] = schema_item['defindex']
                item['outputQuality'] = 14
                item['quality'] = item['quality'] or schema_item.get('item_quality', 6)
        
        elif 'strangifier chemistry set' in name_lower:
            name_lower = name_lower.replace('strangifier chemistry set', '').strip()
            
            schema_item = schema.get_item_by_item_name(name_lower)
            if schema_item:
                item['defindex'] = 20000
                item['target'] = schema_item['defindex']
                item['quality'] = 6
                item['output'] = 6522
                item['outputQuality'] = 6
        
        elif 'strangifier' in name_lower:
            name_lower = name_lower.replace('strangifier', '').strip()
            item['defindex'] = 6522
            
            schema_item = schema.get_item_by_item_name(name_lower)
            if schema_item:
                item['target'] = schema_item['defindex']
                item['quality'] = item['quality'] or schema_item.get('item_quality', 6)
        
        elif 'kit' in name_lower and item['killstreak']:
            name_lower = name_lower.replace('kit', '').strip()
            
            if item['killstreak'] == 1:
                item['defindex'] = 6527
            elif item['killstreak'] == 2:
                item['defindex'] = 6523
            elif item['killstreak'] == 3:
                item['defindex'] = 6526
            
            if name_lower:
                schema_item = schema.get_item_by_item_name(name_lower)
                if schema_item:
                    item['target'] = schema_item['defindex']
            
            if not item['quality']:
                item['quality'] = 6
        
        elif item['paintkit'] and 'war paint' in name_lower:
            name_lower = f"Paintkit {item['paintkit']}"
            if not item['quality']:
                item['quality'] = 15
            
            for schema_item in schema.raw['schema']['items']:
                if schema_item.get('name') == name_lower:
                    item['defindex'] = schema_item['defindex']
                    break
        
        return name_lower

    @staticmethod
    def _handle_weapon_skins(name_lower: str, item: dict, schema: Schema):
        """Handle weapon skin defindex mapping"""
        if 'pistol' in name_lower and item['paintkit'] in schema.PISTOL_SKINS:
            item['defindex'] = schema.PISTOL_SKINS[item['paintkit']]
        elif 'rocket launcher' in name_lower and item['paintkit'] in schema.ROCKET_LAUNCHER_SKINS:
            item['defindex'] = schema.ROCKET_LAUNCHER_SKINS[item['paintkit']]
        elif 'medi gun' in name_lower and item['paintkit'] in schema.MEDIGUN_SKINS:
            item['defindex'] = schema.MEDIGUN_SKINS[item['paintkit']]
        elif 'revolver' in name_lower and item['paintkit'] in schema.REVOLVER_SKINS:
            item['defindex'] = schema.REVOLVER_SKINS[item['paintkit']]
        elif 'stickybomb launcher' in name_lower and item['paintkit'] in schema.STICKYBOMB_SKINS:
            item['defindex'] = schema.STICKYBOMB_SKINS[item['paintkit']]
        elif 'sniper rifle' in name_lower and item['paintkit'] in schema.SNIPER_RIFLE_SKINS:
            item['defindex'] = schema.SNIPER_RIFLE_SKINS[item['paintkit']]
        elif 'flame thrower' in name_lower and item['paintkit'] in schema.FLAME_THROWER_SKINS:
            item['defindex'] = schema.FLAME_THROWER_SKINS[item['paintkit']]
        elif 'minigun' in name_lower and item['paintkit'] in schema.MINIGUN_SKINS:
            item['defindex'] = schema.MINIGUN_SKINS[item['paintkit']]
        elif 'scattergun' in name_lower and item['paintkit'] in schema.SCATTERGUN_SKINS:
            item['defindex'] = schema.SCATTERGUN_SKINS[item['paintkit']]
        elif 'shotgun' in name_lower and item['paintkit'] in schema.SHOTGUN_SKINS:
            item['defindex'] = schema.SHOTGUN_SKINS[item['paintkit']]
        elif 'smg' in name_lower and item['paintkit'] in schema.SMG_SKINS:
            item['defindex'] = schema.SMG_SKINS[item['paintkit']]
        elif 'grenade launcher' in name_lower and item['paintkit'] in schema.GRENADE_LAUNCHER_SKINS:
            item['defindex'] = schema.GRENADE_LAUNCHER_SKINS[item['paintkit']]
        elif 'wrench' in name_lower and item['paintkit'] in schema.WRENCH_SKINS:
            item['defindex'] = schema.WRENCH_SKINS[item['paintkit']]
        elif 'knife' in name_lower and item['paintkit'] in schema.KNIFE_SKINS:
            item['defindex'] = schema.KNIFE_SKINS[item['paintkit']]

    @staticmethod
    def _dict_to_sku(item: dict) -> str:
        """Convert item dict to SKU string"""
        item_obj = itemClass()
        item_obj.Defindex = item['defindex']
        item_obj.Quality = item['quality']
        item_obj.Craftable = item['craftable']
        item_obj.Australium = item['australium']
        item_obj.Festive = item['festive']
        item_obj.Killstreak = item['killstreak']
        item_obj.Effect = item['effect']
        item_obj.PaintKit = item['paintkit']
        item_obj.Wear = item['wear']
        item_obj.ElevatedQuality = item['quality2']
        item_obj.Target = item['target']
        item_obj.CraftNum = item['craftnumber']
        item_obj.CrateSn = item['crateseries']
        item_obj.Output = item['output']
        item_obj.OutputQuality = item['outputQuality']
        
        return Sku.object_to_sku(item_obj)

    @staticmethod
    def update_schema(api_key: str = None, use_autobot: bool = True):
        global _schema
        cache_file = Schema.SCHEMA_CACHE_FILE
        if cache_file.exists():
            cache_file.unlink()
        _schema = Schema(api_key=api_key, use_autobot=use_autobot)
