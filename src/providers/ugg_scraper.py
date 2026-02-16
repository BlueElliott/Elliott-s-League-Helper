"""
U.GG Web Scraper Provider
Scrapes U.GG website HTML for build data since their API is not public
"""

import aiohttp
from typing import Optional, List
from bs4 import BeautifulSoup
from providers.base import BaseProvider, BuildData, RuneData, ItemBuild
from providers.champion_builds import get_champion_build


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
            print(f"Unknown champion ID: {champion_id}, using fallback")
            return get_champion_build(champion_id, role)

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
                        return get_champion_build(champion_id, role)

                    html = await response.text()
                    return self._parse_html(html, champion_id, role)

        except Exception as e:
            print(f"U.GG scraping error: {e}")
            import traceback
            traceback.print_exc()
            return get_champion_build(champion_id, role)

    async def get_aram_build(self, champion_id: int, patch: str) -> Optional[BuildData]:
        """Scrape ARAM build data"""
        champion_name = CHAMPION_NAMES.get(champion_id)
        if not champion_name:
            return get_champion_build(champion_id, 'aram')

        url = f"{self.base_url}/{champion_name}/build?queueType=normal_aram"

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        return get_champion_build(champion_id, 'aram')

                    html = await response.text()
                    return self._parse_html(html, champion_id, 'aram')

        except Exception:
            return get_champion_build(champion_id, 'aram')

    def _parse_html(self, html: str, champion_id: int, role: str) -> Optional[BuildData]:
        """
        Parse U.GG HTML to extract runes and items from window.__SSR_DATA__

        U.GG embeds build data as JSON in script tags via window.__SSR_DATA__
        """
        try:
            import json
            import re

            # Extract window.__SSR_DATA__ from script tags
            ssr_data_match = re.search(r'window\.__SSR_DATA__\s*=\s*({.+?});', html, re.DOTALL)

            if ssr_data_match:
                print("DEBUG: Found window.__SSR_DATA__")
                ssr_data_str = ssr_data_match.group(1)

                try:
                    ssr_data = json.loads(ssr_data_str)
                    print("DEBUG: Successfully parsed SSR data")

                    # Navigate the data structure to find rune recommendations
                    # The structure varies, so we'll look for common patterns
                    runes = self._extract_runes_from_ssr(ssr_data)
                    items = self._extract_items_from_ssr(ssr_data)

                    if runes:
                        print("DEBUG: Successfully extracted runes from SSR data")
                        return BuildData(
                            runes=runes,
                            items=items or self._get_fallback_items(),
                            summoner_spells=[4, 14]  # Flash + most common spell
                        )

                except json.JSONDecodeError as e:
                    print(f"DEBUG: JSON parse error: {e}")

            # Fallback: Use champion-specific build
            print(f"DEBUG: Using champion-specific fallback for champion {champion_id}")
            return get_champion_build(champion_id, role)

        except Exception as e:
            print(f"HTML parsing error: {e}")
            import traceback
            traceback.print_exc()
            return get_champion_build(champion_id, role)

    def _extract_runes_from_ssr(self, ssr_data: dict) -> Optional[RuneData]:
        """Extract rune data from SSR data structure"""
        try:
            # U.GG's structure can vary, look for common patterns
            # Typically nested in data -> ranked_stats or similar

            # Try to find rune data in the structure
            for key, value in ssr_data.items():
                if isinstance(value, dict):
                    data = value.get('data', {})

                    # Look for rune recommendations
                    if 'runes' in str(data).lower() or 'perks' in str(data).lower():
                        # Try to extract perk IDs
                        # This is a simplified extraction - actual structure may vary
                        return self._parse_rune_data(data)

            return None

        except Exception as e:
            print(f"DEBUG: Error extracting runes: {e}")
            return None

    def _parse_rune_data(self, data: dict) -> Optional[RuneData]:
        """Parse rune data from the data structure"""
        # This is a placeholder - actual implementation depends on data structure
        # For now, return None to trigger fallback
        return None

    def _extract_items_from_ssr(self, ssr_data: dict) -> Optional[ItemBuild]:
        """Extract item build from SSR data structure"""
        # Placeholder - will implement after testing rune extraction
        return None

    def _get_fallback_items(self) -> ItemBuild:
        """Get fallback item build"""
        return ItemBuild(
            starting_items=[1056, 2003, 2003],
            core_items=[3020, 6653, 3135],
            situational_items=[3157, 3165, 3089]
        )

    def _get_fallback_build(self) -> BuildData:
        """Get complete fallback build data"""
        sample_runes = RuneData(
            primary_style=8100,  # Domination
            sub_style=8000,      # Precision
            selected_perks=[
                8112,  # Electrocute (keystone)
                8143,  # Sudden Impact
                8120,  # Ghost Poro (changed from 8138 Eyeball Collection)
                8135,  # Treasure Hunter
                8009,  # Presence of Mind
                8014,  # Coup de Grace
                5008,  # Adaptive Force (shard 1)
                5008,  # Adaptive Force (shard 2)
                5002   # Armor (shard 3)
            ]
        )

        return BuildData(
            runes=sample_runes,
            items=self._get_fallback_items(),
            summoner_spells=[4, 14]
        )

    async def get_current_patch(self) -> Optional[str]:
        """
        Get current patch version
        Returns a default patch for now
        """
        # TODO: Fetch actual current patch from Riot API or Data Dragon
        return "14_1"
