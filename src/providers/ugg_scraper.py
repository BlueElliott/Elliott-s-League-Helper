"""
U.GG Web Scraper Provider
Scrapes U.GG website HTML for build data since their API is not public
"""

import aiohttp
from typing import Optional, List
from bs4 import BeautifulSoup
from providers.base import BaseProvider, BuildData, RuneData, ItemBuild


# Champion ID to name mapping (will expand this)
CHAMPION_NAMES = {
    1: "annie", 2: "olaf", 3: "galio", 4: "twistedfate", 5: "xinzhao",
    6: "urgot", 7: "leblanc", 8: "vladimir", 9: "fiddlesticks", 10: "kayle",
    11: "masteryi", 12: "alistar", 13: "ryze", 14: "sion", 15: "sivir",
    16: "soraka", 17: "teemo", 18: "tristana", 19: "warwick", 20: "nunu",
    21: "missfortune", 22: "ashe", 23: "tryndamere", 24: "jax", 25: "morgana",
    26: "zilean", 27: "singed", 28: "evelynn", 29: "twitch", 30: "karthus",
    31: "chogath", 32: "amumu", 33: "rammus", 34: "anivia", 35: "shaco",
    36: "drmundo", 37: "sona", 38: "kassadin", 39: "irelia", 40: "janna",
    41: "gangplank", 42: "corki", 43: "karma", 44: "taric", 45: "veigar",
    48: "trundle", 50: "swain", 51: "caitlyn", 53: "blitzcrank", 54: "malphite",
    55: "katarina", 56: "nocturne", 57: "maokai", 58: "renekton", 59: "jarvaniv",
    60: "elise", 61: "orianna", 62: "wukong", 63: "brand", 64: "leesin",
    67: "vayne", 68: "rumble", 69: "cassiopeia", 72: "skarner", 74: "heimerdinger",
    75: "nasus", 76: "nidalee", 77: "udyr", 78: "poppy", 79: "gragas",
    80: "pantheon", 81: "ezreal", 82: "mordekaiser", 83: "yorick", 84: "akali",
    85: "kennen", 86: "garen", 89: "leona", 90: "malzahar", 91: "talon",
    92: "riven", 96: "kogmaw", 98: "shen", 99: "lux", 101: "xerath",
    102: "shyvana", 103: "ahri", 104: "graves", 105: "fizz", 106: "volibear",
    107: "rengar", 110: "varus", 111: "nautilus", 112: "viktor", 113: "sejuani",
    114: "fiora", 115: "ziggs", 117: "lulu", 119: "draven", 120: "hecarim",
    121: "khazix", 122: "darius", 126: "jayce", 127: "lissandra", 131: "diana",
    133: "quinn", 134: "syndra", 136: "aurelionsol", 141: "kayn", 142: "zoe",
    143: "zyra", 145: "kaisa", 147: "seraphine", 150: "gnar", 154: "zac",
    157: "yasuo", 161: "velkoz", 163: "taliyah", 164: "camille", 166: "akshan",
    200: "belveth", 201: "braum", 202: "jhin", 203: "kindred", 221: "zeri",
    222: "jinx", 223: "tahmkench", 234: "viego", 235: "senna", 236: "lucian",
    238: "zed", 240: "kled", 245: "ekko", 246: "qiyana", 254: "vi",
    266: "aatrox", 267: "nami", 268: "azir", 350: "yuumi", 360: "samira",
    412: "thresh", 420: "illaoi", 421: "reksai", 427: "ivern", 429: "kalista",
    432: "bard", 497: "rakan", 498: "xayah", 516: "ornn", 517: "sylas",
    518: "neeko", 523: "aphelios", 526: "rell", 555: "pyke", 711: "vex",
    777: "yone", 875: "sett", 876: "lillia", 887: "gwen", 888: "renata",
    895: "nilah", 897: "ksante", 902: "milio", 910: "hwei", 950: "naafiri"
}


class UGGScraperProvider(BaseProvider):
    """Provider that scrapes U.GG website for build data"""

    def __init__(self):
        super().__init__()
        self.name = "U.GG"
        self.base_url = "https://u.gg/lol/champions"

    async def get_build(self, champion_id: int, role: str, patch: str) -> Optional[BuildData]:
        """
        Scrape build data from U.GG website

        Args:
            champion_id: Champion ID
            role: Role (top, jungle, middle, bottom, support)
            patch: Patch version (not used for scraping, we get latest)

        Returns:
            BuildData or None if not found
        """
        champion_name = CHAMPION_NAMES.get(champion_id)
        if not champion_name:
            print(f"Unknown champion ID: {champion_id}")
            return None

        role = self.normalize_role(role)

        # U.GG URL format: https://u.gg/lol/champions/{champion}/build?role={role}
        url = f"{self.base_url}/{champion_name}/build?role={role}"

        try:
            print(f"DEBUG: Scraping URL: {url}")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    print(f"DEBUG: Response status: {response.status}")

                    if response.status != 200:
                        error_text = await response.text()
                        print(f"DEBUG: Error: {error_text[:200]}")
                        return None

                    html = await response.text()
                    return self._parse_html(html)

        except Exception as e:
            print(f"U.GG scraping error: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def get_aram_build(self, champion_id: int, patch: str) -> Optional[BuildData]:
        """Scrape ARAM build data"""
        champion_name = CHAMPION_NAMES.get(champion_id)
        if not champion_name:
            return None

        url = f"{self.base_url}/{champion_name}/build?queueType=normal_aram"

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        return None

                    html = await response.text()
                    return self._parse_html(html)

        except Exception:
            return None

    def _parse_html(self, html: str) -> Optional[BuildData]:
        """
        Parse U.GG HTML to extract runes and items

        Note: This is a simplified parser. U.GG's actual structure may require
        more sophisticated parsing or use of their internal API calls.
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # For now, return hardcoded sample data
            # TODO: Implement actual HTML parsing when we can inspect the structure
            print("DEBUG: HTML received, but parsing not fully implemented yet")
            print("DEBUG: Using fallback sample runes for testing")

            # Sample runes for testing (Electrocute - Domination + Precision)
            sample_runes = RuneData(
                primary_style=8100,  # Domination
                sub_style=8000,      # Precision
                selected_perks=[
                    8112,  # Electrocute (keystone)
                    8143,  # Sudden Impact
                    8138,  # Eyeball Collection
                    8135,  # Treasure Hunter
                    8009,  # Presence of Mind
                    8014,  # Coup de Grace
                    5008,  # Adaptive Force (shard 1)
                    5008,  # Adaptive Force (shard 2)
                    5002   # Armor (shard 3)
                ]
            )

            sample_items = ItemBuild(
                starting_items=[1056, 2003, 2003],  # Doran's Ring + 2 Health Pots
                core_items=[3020, 6653, 3135],       # Sorcerer's Shoes, Luden's, Void Staff
                situational_items=[3157, 3165, 3089] # Zhonya's, Morello, Rabadon's
            )

            return BuildData(
                runes=sample_runes,
                items=sample_items,
                summoner_spells=[4, 14]  # Flash + Ignite
            )

        except Exception as e:
            print(f"HTML parsing error: {e}")
            return None
