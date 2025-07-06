import json
import time
import requests
from typing import Dict, Optional
from pathlib import Path


class Schema:
    PAINT_MAPPINGS = {
        '(paint: color no. 216-190-216)': 3100495,
        '(paint: a color similar to slate)': 3100495,
        '(paint: indubitably green)': 7511618,
        '(paint: color no. 729e42)': 7511618,
        '(paint: zepheniah\'s greed)': 4345659,
        '(paint: color no. 424f3b)': 4345659,
        '(paint: noble hatter\'s violet)': 5322826,
        '(paint: color no. 51384a)': 5322826,
        '(paint: color no. 483838)': 5322826,
        '(paint: a deep commitment to purple)': 8208497,
        '(paint: color no. 7d4071)': 8208497,
        '(paint: mann co. orange)': 12377523,
        '(paint: color no. cf7336)': 12377523,
        '(paint: muskelmannbraun)': 10843461,
        '(paint: color no. a57545)': 10843461,
        '(paint: peculiarly drab tincture)': 12955537,
        '(paint: color no. c5af91)': 12955537,
        '(paint: radigan conagher brown)': 6901050,
        '(paint: color no. 694d3a)': 6901050,
        '(paint: ye olde rustic colour)': 8154199,
        '(paint: color no. 7c6c57)': 8154199,
        '(paint: australium gold)': 15185211,
        '(paint: color no. e7b53b)': 15185211,
        '(paint: aged moustache grey)': 8289918,
        '(paint: color no. 7e7e7e)': 8289918,
        '(paint: an extraordinary abundance of tinge)': 15132390,
        '(paint: color no. e6e6e6)': 15132390,
        '(paint: a distinctive lack of hue)': 1315860,
        '(paint: color no. 141414)': 1315860,
        '(paint: pink as hell)': 16738740,
        '(paint: color no. ff69b4)': 16738740,
        '(paint: the bitter taste of defeat and lime)': 3329330,
        '(paint: color no. 32cd32)': 3329330,
        '(paint: the color of a gentlemann\'s business pants)': 15787660,
        '(paint: color no. f0e68c)': 15787660,
        '(paint: dark salmon injustice)': 15308410,
        '(paint: color no. e9967a)': 15308410,
        '(paint: a mann\'s mint)': 12377306,
        '(paint: color no. bcddb3)': 12377306,
        '(paint: after eight)': 2960676,
        '(paint: color no. 2d2d24)': 2960676,
        '(paint: legacy paint)': 5801378,
        '(paint: waterlogged lab coat)': 11049612,
        '(paint: color no. a89a8c)': 11049612,
        '(paint: balaclavas are forever)': 3874595,
        '(paint: color no. 3b1f23)': 3874595,
        '(paint: an air of debonair)': 6637376,
        '(paint: color no. 654740)': 6637376,
        '(paint: the value of teamwork)': 8400928,
        '(paint: color no. 803020)': 8400928,
        '(paint: cream spirit)': 12807213,
        '(paint: color no. c36c2d)': 12807213,
        '(paint: operator\'s overalls)': 4732984,
        '(paint: color no. 483838)': 4732984,
        '(paint: drably olive)': 8421376,
        '(paint: color no. 808000)': 8421376,
    }
    
    MUNITION_CRATES = {
        82: 5734, 83: 5735, 84: 5742, 85: 5752,
        90: 5781, 91: 5802, 92: 5803, 103: 5859
    }
    
    PISTOL_SKINS = {
        0: 15013, 18: 15018, 35: 15035, 41: 15041, 46: 15046,
        56: 15056, 61: 15061, 63: 15060, 69: 15100, 70: 15101,
        74: 15102, 78: 15126, 81: 15148
    }
    
    ROCKET_LAUNCHER_SKINS = {
        1: 15014, 6: 15006, 28: 15028, 43: 15043, 52: 15052,
        57: 15057, 60: 15081, 69: 15104, 70: 15105, 76: 15129,
        79: 15130, 80: 15150
    }
    
    MEDIGUN_SKINS = {
        2: 15010, 5: 15008, 25: 15025, 39: 15039, 50: 15050,
        65: 15078, 72: 15097, 76: 15120, 78: 15121, 79: 15122,
        81: 15145, 83: 15146
    }
    
    REVOLVER_SKINS = {
        3: 15011, 27: 15027, 42: 15042, 51: 15051, 63: 15064,
        64: 15062, 65: 15063, 72: 15103, 76: 15127, 77: 15128,
        81: 15149
    }
    
    STICKYBOMB_SKINS = {
        4: 15012, 8: 15009, 24: 15024, 38: 15038, 45: 15045,
        48: 15048, 60: 15082, 62: 15083, 63: 15084, 68: 15113,
        76: 15137, 78: 15138, 81: 15155
    }
    
    SNIPER_RIFLE_SKINS = {
        7: 15007, 14: 15000, 19: 15019, 23: 15023, 33: 15033,
        59: 15059, 62: 15070, 64: 15071, 65: 15072, 76: 15135,
        66: 15111, 67: 15112, 78: 15136, 82: 15154
    }
    
    FLAME_THROWER_SKINS = {
        9: 15005, 17: 15017, 30: 15030, 34: 15034, 49: 15049,
        54: 15054, 60: 15066, 61: 15068, 62: 15067, 66: 15089,
        67: 15090, 76: 15115, 80: 15141
    }
    
    MINIGUN_SKINS = {
        10: 15004, 20: 15020, 26: 15026, 31: 15031, 40: 15040,
        55: 15055, 61: 15088, 62: 15087, 63: 15086, 70: 15098,
        73: 15099, 76: 15123, 77: 15125, 78: 15124, 84: 15147
    }
    
    SCATTERGUN_SKINS = {
        11: 15002, 15: 15015, 21: 15021, 29: 15029, 36: 15036,
        53: 15053, 61: 15069, 63: 15065, 69: 15106, 72: 15107,
        74: 15108, 76: 15131, 83: 15157, 85: 15151
    }
    
    SHOTGUN_SKINS = {
        12: 15003, 16: 15016, 44: 15044, 47: 15047, 60: 15085,
        72: 15109, 76: 15132, 78: 15133, 86: 15152
    }
    
    SMG_SKINS = {
        13: 15001, 22: 15022, 32: 15032, 37: 15037, 58: 15058,
        65: 15076, 69: 15110, 79: 15134, 81: 15153
    }
    
    WRENCH_SKINS = {
        60: 15074, 61: 15073, 64: 15075, 75: 15114,
        77: 15140, 78: 15139, 82: 15156
    }
    
    GRENADE_LAUNCHER_SKINS = {
        60: 15077, 63: 15079, 67: 15091, 68: 15092,
        76: 15116, 77: 15117, 80: 15142, 84: 15158
    }
    
    KNIFE_SKINS = {
        64: 15080, 69: 15094, 70: 15095, 71: 15096,
        77: 15119, 78: 15118, 81: 15143, 82: 15144
    }
    
    EXCLUSIVE_GENUINE = {
        810: 831, 811: 832, 812: 833, 813: 834, 814: 835,
        815: 836, 816: 837, 817: 838, 30720: 30740,
        30721: 30741, 30724: 30739
    }
    
    EXCLUSIVE_GENUINE_REVERSED = {
        831: 810, 832: 811, 833: 812, 834: 813, 835: 814,
        836: 815, 837: 816, 838: 817, 30740: 30720,
        30741: 30721, 30739: 30724
    }
    
    RETIRED_KEYS = {
        '5049': {'defindex': 5049, 'name': 'Festive Winter Crate Key'},
        '5067': {'defindex': 5067, 'name': 'Refreshing Summer Cooler Key'},
        '5072': {'defindex': 5072, 'name': 'Naughty Winter Crate Key'},
        '5073': {'defindex': 5073, 'name': 'Nice Winter Crate Key'},
        '5079': {'defindex': 5079, 'name': 'Scorched Key'},
        '5081': {'defindex': 5081, 'name': 'Fall Key'},
        '5628': {'defindex': 5628, 'name': 'Eerie Key'},
        '5631': {'defindex': 5631, 'name': 'Naughty Winter Crate Key 2012'},
        '5632': {'defindex': 5632, 'name': 'Nice Winter Crate Key 2012'},
        '5713': {'defindex': 5713, 'name': 'Spooky Key'},
        '5716': {'defindex': 5716, 'name': 'Naughty Winter Crate Key 2013'},
        '5717': {'defindex': 5717, 'name': 'Nice Winter Crate Key 2013'},
        '5762': {'defindex': 5762, 'name': 'Limited Late Summer Crate Key'},
        '5791': {'defindex': 5791, 'name': 'Naughty Winter Crate Key 2014'},
        '5792': {'defindex': 5792, 'name': 'Nice Winter Crate Key 2014'}
    }
    
    CACHE_DIR = Path.home() / '.tf2_sku_cache'
    SCHEMA_CACHE_FILE = CACHE_DIR / 'schema.json'
    CACHE_DURATION = 24 * 60 * 60 * 30 # 30 days
    
    def __init__(self, data: Optional[Dict] = None, api_key: Optional[str] = None, use_autobot: bool = True):
        self.api_key = api_key
        self.use_autobot = use_autobot
        
        if data:
            self.version = data.get('version')
            self.raw = data.get('raw')
            self.time = data.get('time', int(time.time() * 1000))
        else:
            # Load from cache or fetch new schema
            if not self._load_from_cache():
                self._fetch_schema()
        
        self._set_properties_data()
    
    def _set_properties_data(self):
        self.crate_series_list = self._get_crate_series_list()
        self.qualities = self._get_qualities()
        self.effects = self._get_particle_effects()
        self.paintkits = self._get_paint_kits()
        self.paints = self._get_paints()
    
    def _load_from_cache(self) -> bool:
        if not self.SCHEMA_CACHE_FILE.exists():
            return False
        
        try:
            with open(self.SCHEMA_CACHE_FILE, 'r') as f:
                data = json.load(f)
            
            if time.time() * 1000 - data.get('time', 0) > self.CACHE_DURATION * 1000:
                return False
            
            self.version = data.get('version')
            self.raw = data.get('raw')
            self.time = data.get('time')
            return True
        except Exception:
            return False
    
    def _save_to_cache(self):
        try:
            self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.SCHEMA_CACHE_FILE, 'w') as f:
                json.dump({
                    'version': self.version,
                    'raw': self.raw,
                    'time': self.time
                }, f)
        except Exception:
            pass  # Ignore cache write errors
    
    def _fetch_schema(self):
        if self.use_autobot:
            self._fetch_from_autobot()
        else:
            if not self.api_key:
                raise ValueError("API key required for Steam API schema fetch")
            self._fetch_from_steam()
    
    def _fetch_from_autobot(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get('https://schema.autobot.tf/schema', headers=headers)
            response.raise_for_status()
            data = response.json()
            
            self.version = data.get('version')
            self.raw = data.get('raw')
            self.time = data.get('time', int(time.time() * 1000))
            
            self._save_to_cache()
        except Exception as e:
            raise ValueError(f"Failed to fetch schema from autobot.tf: {e}")
    
    def _fetch_from_steam(self):
        raise NotImplementedError("Steam API schema fetching not yet implemented")
    
    def get_item_by_defindex(self, defindex: int) -> Optional[Dict]:
        items = self.raw['schema']['items']
        
        start, end = 0, len(items) - 1
        while start <= end:
            mid = (start + end) // 2
            if items[mid]['defindex'] < defindex:
                start = mid + 1
            elif items[mid]['defindex'] > defindex:
                end = mid - 1
            else:
                return items[mid]
        
        for item in items:
            if item['defindex'] == defindex:
                return item
        
        return None
    
    def get_item_by_item_name(self, name: str) -> Optional[Dict]:
        name_lower = name.lower()
        
        for item in self.raw['schema']['items']:
            if name_lower == item['item_name'].lower():
                if item['item_name'] == 'Name Tag' and item['defindex'] == 2093:
                    continue
                
                if item.get('item_quality', 0) == 0:
                    continue
                
                return item
        
        return None
    
    def get_item_by_item_name_with_the(self, name: str) -> Optional[Dict]:
        name_lower = name.lower()
        
        if 'the ' in name_lower:
            name_lower = name_lower.replace('the ', '').strip()
        
        for item in self.raw['schema']['items']:
            item_name = item['item_name'].lower()
            
            if 'the ' in item_name:
                item_name = item_name.replace('the ', '').strip()
            
            if name_lower == item_name:
                if item['item_name'] == 'Name Tag' and item['defindex'] == 2093:
                    continue

                if item.get('item_quality', 0) == 0:
                    continue
                
                return item
        
        return None
    
    def get_quality_by_id(self, quality_id: int) -> Optional[str]:
        qualities = self.raw['schema']['qualities']
        quality_names = self.raw['schema']['qualityNames']
        
        for name, qid in qualities.items():
            if qid == quality_id:
                return quality_names.get(name)
        
        return None
    
    def get_quality_id_by_name(self, name: str) -> Optional[int]:
        qualities = self.raw['schema']['qualities']
        quality_names = self.raw['schema']['qualityNames']
        
        name_lower = name.lower()
        for key, quality_name in quality_names.items():
            if quality_name.lower() == name_lower:
                return qualities.get(key)
        
        return None
    
    def get_effect_by_id(self, effect_id: int) -> Optional[str]:
        particles = self.raw['schema']['attribute_controlled_attached_particles']
        
        start, end = 0, len(particles) - 1
        while start <= end:
            mid = (start + end) // 2
            if particles[mid]['id'] < effect_id:
                start = mid + 1
            elif particles[mid]['id'] > effect_id:
                end = mid - 1
            else:
                return particles[mid]['name']
        
        for particle in particles:
            if particle['id'] == effect_id:
                return particle['name']
        
        return None
    
    def get_effect_id_by_name(self, name: str) -> Optional[int]:
        particles = self.raw['schema']['attribute_controlled_attached_particles']
        name_lower = name.lower()
        
        for particle in particles:
            if particle['name'].lower() == name_lower:
                return particle['id']
        
        return None
    
    def get_skin_by_id(self, skin_id: int) -> Optional[str]:
        paintkits = self.raw['schema'].get('paintkits', {})
        return paintkits.get(str(skin_id))
    
    def get_skin_id_by_name(self, name: str) -> Optional[int]:
        paintkits = self.raw['schema'].get('paintkits', {})
        name_lower = name.lower()
        
        for sid, skin_name in paintkits.items():
            if skin_name.lower() == name_lower:
                return int(sid)
        
        return None
    
    def get_paint_name_by_decimal(self, decimal: int) -> Optional[str]:
        if decimal == 5801378:
            return 'Legacy Paint'
        
        paint_cans = [item for item in self.raw['schema']['items'] 
                     if 'Paint Can' in item.get('name', '') and item.get('name') != 'Paint Can']
        
        for paint in paint_cans:
            if 'attributes' not in paint:
                continue
            
            for attr in paint['attributes']:
                if attr.get('value') == decimal:
                    return paint['item_name']
        
        return None
    
    def get_paint_decimal_by_name(self, name: str) -> Optional[int]:
        if name == 'Legacy Paint':
            return 5801378
        
        paint_cans = [item for item in self.raw['schema']['items'] 
                     if 'Paint Can' in item.get('name', '') and item.get('name') != 'Paint Can']
        
        name_lower = name.lower()
        for paint in paint_cans:
            if paint['item_name'].lower() == name_lower:
                if 'attributes' in paint and paint['attributes']:
                    return paint['attributes'][0]['value']
        
        return None
    
    def _get_crate_series_list(self) -> Dict[int, int]:
        crate_series = {}
        
        for item in self.raw['schema']['items']:
            if 'attributes' in item:
                for attr in item['attributes']:
                    if attr.get('name') == 'set supply crate series':
                        crate_series[item['defindex']] = attr['value']
                        break
        
        if 'items_game' in self.raw:
            items = self.raw['items_game'].get('items', {})
            for defindex, item_data in items.items():
                if 'static_attrs' in item_data:
                    series_attr = item_data['static_attrs'].get('set supply crate series')
                    if series_attr:
                        value = series_attr.get('value', series_attr) if isinstance(series_attr, dict) else series_attr
                        crate_series[int(defindex)] = int(value)
        
        return crate_series
    
    def _get_qualities(self) -> Dict[str, int]:
        qualities_raw = self.raw['schema']['qualities']
        quality_names = self.raw['schema']['qualityNames']
        
        return {quality_names[key]: value for key, value in qualities_raw.items() if key in quality_names}
    
    def _get_particle_effects(self) -> Dict[str, int]:
        effects = {}
        previous = ''
        
        for particle in self.raw['schema']['attribute_controlled_attached_particles']:
            name = particle['name']
            if name and name != previous:
                effects[name] = particle['id']
                
                if name == 'Eerie Orbiting Fire':
                    effects.pop('Orbiting Fire', None)
                    effects['Orbiting Fire'] = 33
                elif name == 'Nether Trail':
                    effects.pop('Ether Trail', None)
                    effects['Ether Trail'] = 103
                elif name == 'Refragmenting Reality':
                    effects.pop('Fragmenting Reality', None)
                    effects['Fragmenting Reality'] = 141
                
                previous = name
        
        effects.pop('', None)
        return effects
    
    def _get_paint_kits(self) -> Dict[str, int]:
        paintkits = self.raw['schema'].get('paintkits', {})
        return {name: int(kit_id) for kit_id, name in paintkits.items()}
    
    def _get_paints(self) -> Dict[str, int]:
        paints = {}
        
        paint_cans = [item for item in self.raw['schema']['items'] 
                     if 'Paint Can' in item.get('name', '') and item.get('name') != 'Paint Can']
        
        for paint in paint_cans:
            if 'attributes' in paint and paint['attributes']:
                paints[paint['item_name']] = paint['attributes'][0]['value']
        
        paints['Legacy Paint'] = 5801378
        return paints
    
    def check_existence(self, item: Dict) -> bool:
        schema_item = self.get_item_by_defindex(item['defindex'])
        if not schema_item:
            return False
        
        if schema_item.get('item_quality') in [0, 3, 5, 11]:
            if item.get('quality') != schema_item['item_quality']:
                return False
        
        if ((item.get('quality') != 1 and item['defindex'] in self.EXCLUSIVE_GENUINE_REVERSED) or
            (item.get('quality') == 1 and item['defindex'] in self.EXCLUSIVE_GENUINE)):
            return False
        
        if str(item['defindex']) in self.RETIRED_KEYS:
            if item['defindex'] in [5713, 5716, 5717, 5762]:
                if item.get('craftable', True):
                    return False
            elif item['defindex'] not in [5791, 5792]:
                if not item.get('craftable', True):
                    return False
        
        if schema_item.get('item_class') == 'supply_crate' and not item.get('crateseries'):
            if item['defindex'] not in [5739, 5760, 5737, 5738]:
                return False
            
            if (item.get('quality', 6) != 6 or item.get('killstreak', 0) != 0 or
                item.get('australium', False) or item.get('effect') or
                item.get('festive', False) or item.get('paintkit') or
                item.get('wear') or item.get('quality2') or
                item.get('craftnumber') or item.get('target') or
                item.get('output') or item.get('outputQuality') or
                item.get('paint')):
                return False
        
        if item.get('crateseries'):
            valid_series = [
                1, 3, 7, 12, 13, 18, 19, 23, 26, 31, 34, 39, 43, 47, 54, 57, 75,
                2, 4, 8, 11, 14, 17, 20, 24, 27, 32, 37, 42, 44, 49, 56, 71, 76,
                5, 9, 10, 15, 16, 21, 25, 28, 29, 33, 38, 41, 45, 55, 59, 77,
                30, 40, 50, 82, 83, 84, 85, 90, 91, 92, 103
            ]
            
            if item['crateseries'] not in valid_series:
                if item['crateseries'] not in self.crate_series_list.values():
                    return False
                
                if item['crateseries'] != self.crate_series_list.get(item['defindex']):
                    return False
            else:
                series = item['crateseries']
                defindex = item['defindex']
                
                valid = False
                if series in [1, 3, 7, 12, 13, 18, 19, 23, 26, 31, 34, 39, 43, 47, 54, 57, 75]:
                    valid = defindex == 5022
                elif series in [2, 4, 8, 11, 14, 17, 20, 24, 27, 32, 37, 42, 44, 49, 56, 71, 76]:
                    valid = defindex == 5041
                elif series in [5, 9, 10, 15, 16, 21, 25, 28, 29, 33, 38, 41, 45, 55, 59, 77]:
                    valid = defindex == 5045
                elif series in [30, 40, 50]:
                    valid = defindex == 5068
                elif series in self.MUNITION_CRATES:
                    valid = defindex == self.MUNITION_CRATES[series]
                
                if not valid:
                    return False
        
        return True
    
    def get_name(self, item: Dict, proper: bool = True, use_pipe_for_skin: bool = False, 
                 scm_format: bool = False) -> Optional[str]:
        schema_item = self.get_item_by_defindex(item['defindex'])
        if not schema_item:
            return None
        
        name = ''
        
        if not scm_format and not item.get('tradable', True):
            name = 'Non-Tradable '
        
        if not scm_format and not item.get('craftable', True):
            name += 'Non-Craftable '
        
        if item.get('quality2'):
            quality2_name = self.get_quality_by_id(item['quality2'])
            elevated_suffix = '(e)' if not scm_format and (item.get('wear') or item.get('paintkit')) else ''
            name += f"{quality2_name}{elevated_suffix} "
        
        should_add_quality = (
            (item.get('quality') == 6 and item.get('quality2')) or
            (item.get('quality') not in [6, 15, 5]) or
            (item.get('quality') == 5 and not item.get('effect')) or
            (item.get('quality') == 5 and scm_format) or
            schema_item.get('item_quality') == 5
        )
        
        if should_add_quality:
            name += f"{self.get_quality_by_id(item.get('quality', 6))} "
        
        if not scm_format and item.get('effect'):
            name += f"{self.get_effect_by_id(item['effect'])} "
        
        if item.get('festive'):
            name += 'Festivized '
        
        if item.get('killstreak', 0) > 0:
            ks_names = ['Killstreak', 'Specialized Killstreak', 'Professional Killstreak']
            name += f"{ks_names[item['killstreak'] - 1]} "
        
        if item.get('target'):
            target_item = self.get_item_by_defindex(item['target'])
            if target_item:
                name += f"{target_item['item_name']} "
        
        if item.get('outputQuality') and item['outputQuality'] != 6:
            name = f"{self.get_quality_by_id(item['outputQuality'])} {name}"
        
        if item.get('output'):
            output_item = self.get_item_by_defindex(item['output'])
            if output_item:
                name += f"{output_item['item_name']} "
        
        if item.get('australium'):
            name += 'Australium '
        
        if item.get('paintkit'):
            skin_name = self.get_skin_by_id(item['paintkit'])
            if skin_name:
                separator = ' | ' if use_pipe_for_skin else ' '
                name += f"{skin_name}{separator}"
        
        if proper and not name and schema_item.get('proper_name'):
            name = 'The '
        
        if str(item['defindex']) in self.RETIRED_KEYS:
            name += self.RETIRED_KEYS[str(item['defindex'])]['name']
        else:
            name += schema_item['item_name']
        
        if item.get('wear'):
            wear_names = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle Scarred']
            name += f" ({wear_names[item['wear'] - 1]})"
        
        if item.get('crateseries'):
            has_attr = (schema_item.get('attributes') and 
                       schema_item['attributes'][0].get('class') == 'supply_crate_series')
            if scm_format:
                if has_attr:
                    name += f" Series %23{item['crateseries']}"
            else:
                name += f" #{item['crateseries']}"
        elif item.get('craftnumber'):
            name += f" #{item['craftnumber']}"
        
        if not scm_format and item.get('paint'):
            paint_name = self.get_paint_name_by_decimal(item['paint'])
            if paint_name:
                name += f" (Paint: {paint_name})"
        
        if scm_format and item.get('wear') and item.get('effect') and item.get('quality') == 15:
            name = f"Unusual {name}"
        
        return name 