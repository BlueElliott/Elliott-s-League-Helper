"""
U.GG Web Scraper Provider
Scrapes U.GG website HTML for build data since their API is not public
"""

import aiohttp
import re
import json
from typing import Optional, List
from bs4 import BeautifulSoup
from providers.base import BaseProvider, BuildData, RuneData, ItemBuild
from providers.champion_builds import get_champion_build


# Reverse map: folder name in icon path -> rune ID
# Built from the complete Data Dragon 16.3.1 rune data
RUNE_NAME_TO_ID = {
    # Domination
    "Electrocute": 8112, "DarkHarvest": 8128, "HailOfBlades": 9923,
    "CheapShot": 8126, "TasteOfBlood": 8139, "SuddenImpact": 8143,
    "SixthSense": 8137, "GrislyMementos": 8140, "DeepWard": 8141,
    "TreasureHunter": 8135, "RelentlessHunter": 8105, "UltimateHunter": 8106,
    # Inspiration
    "GlacialAugment": 8351, "UnsealedSpellbook": 8360, "FirstStrike": 8369,
    "HextechFlashtraption": 8306, "MagicalFootwear": 8304, "CashBack": 8321,
    "TripleTonic": 8313, "TimeWarpTonic": 8352, "BiscuitDelivery": 8345,
    "CosmicInsight": 8347, "ApproachVelocity": 8410, "JackOfAllTrades": 8316,
    # Precision
    "PressTheAttack": 8005, "LethalTempo": 8008, "FleetFootwork": 8021,
    "Conqueror": 8010, "AbsorbLife": 9101, "Triumph": 9111,
    "PresenceOfMind": 8009, "LegendAlacrity": 9104, "LegendHaste": 9105,
    "LegendBloodline": 9103, "CoupDeGrace": 8014, "CutDown": 8017, "LastStand": 8299,
    # Resolve
    "GraspOfTheUndying": 8437, "VeteranAftershock": 8439, "Guardian": 8465,
    "Demolish": 8446, "FontOfLife": 8463, "MirrorShell": 8401,
    "Conditioning": 8429, "SecondWind": 8444, "BonePlating": 8473,
    "Overgrowth": 8451, "Revitalize": 8453, "Unflinching": 8242,
    # Sorcery
    "SummonAery": 8214, "ArcaneComet": 8229, "PhaseRush": 8230,
    "NullifyingOrb": 8224, "ManaflowBand": 8226, "NimbusCloak": 8275,
    "Transcendence": 8210, "Celerity": 8234, "AbsoluteFocus": 8233,
    "Scorch": 8237, "Waterwalking": 8232, "GatheringStorm": 8236,
    # Stat shards (icon file names)
    "StatModsAdaptiveForceIcon": 5008, "StatModsAttackSpeedIcon": 5005,
    "StatModsCDRScalingIcon": 5007, "StatModsArmorIcon": 5002,
    "StatModsMagicResIcon": 5003, "StatModsHealthScalingIcon": 5001,
}

# Tree name to style ID
TREE_NAME_TO_ID = {
    "Precision": 8000, "Domination": 8100, "Sorcery": 8200,
    "Inspiration": 8300, "Resolve": 8400,
}


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
        Parse U.GG HTML to extract runes and items.
        Strategy: find rune icon image src paths which encode the rune name,
        then map names -> IDs using our Data Dragon lookup table.
        """
        try:
            runes = self._extract_runes_from_html(html)
            items = self._extract_items_from_html(html)

            if runes:
                print(f"DEBUG: Successfully extracted live runes from U.GG for champion {champion_id}")
                from providers.champion_builds import _get_role_items
                return BuildData(
                    runes=runes,
                    items=items or _get_role_items(role),
                    summoner_spells=self._extract_summoner_spells(html, champion_id)
                )

            print(f"DEBUG: Using champion-specific fallback for champion {champion_id}")
            return get_champion_build(champion_id, role)

        except Exception as e:
            print(f"HTML parsing error: {e}")
            return get_champion_build(champion_id, role)

    def _extract_runes_from_html(self, html: str) -> Optional[RuneData]:
        """
        Extract runes by parsing rune icon image paths.
        U.GG includes rune icon URLs like:
          .../perk-images/Styles/Domination/Electrocute/Electrocute.png
        We read the tree names and rune folder names and map them to IDs.
        """
        # Find all rune-related image src attributes
        perk_pattern = re.compile(
            r'perk-images/Styles/(\w+)/(\w+)/[\w.]+\.png', re.IGNORECASE
        )
        stat_pattern = re.compile(
            r'perk-images/StatMods/(StatMods\w+)(?:Icon)?(?:\.[\w]+)?\.png', re.IGNORECASE
        )

        matches = perk_pattern.findall(html)
        if not matches:
            return None

        # matches = list of (TreeName, RuneFolderName)
        # First occurrence of each tree = keystone of that tree.
        # We need to identify: primary tree, secondary tree, and stat shards.

        trees_seen = {}      # tree_name -> list of rune IDs in order
        primary_tree = None
        sub_tree = None

        for tree_name, rune_folder in matches:
            if tree_name not in ("Precision", "Domination", "Sorcery", "Inspiration", "Resolve"):
                continue
            rune_id = RUNE_NAME_TO_ID.get(rune_folder)
            if rune_id is None:
                continue
            if tree_name not in trees_seen:
                trees_seen[tree_name] = []
            trees_seen[tree_name].append(rune_id)

        if not trees_seen:
            return None

        # Primary tree = the one with the most runes (4: keystone + 3 rows)
        # Secondary tree = the one with 2 runes
        sorted_trees = sorted(trees_seen.items(), key=lambda x: len(x[1]), reverse=True)

        if len(sorted_trees) < 2:
            return None

        primary_tree_name, primary_runes = sorted_trees[0]
        sub_tree_name, sub_runes = sorted_trees[1]

        # Ensure correct count
        primary_runes = primary_runes[:4]
        sub_runes = sub_runes[:2]

        if len(primary_runes) < 4 or len(sub_runes) < 2:
            return None

        # Extract stat shards
        stat_matches = stat_pattern.findall(html)
        shard_ids = []
        for match in stat_matches:
            shard_id = RUNE_NAME_TO_ID.get(match) or RUNE_NAME_TO_ID.get(match + "Icon")
            if shard_id and shard_id not in shard_ids:
                shard_ids.append(shard_id)
        # Pad to 3 shards if needed
        while len(shard_ids) < 3:
            shard_ids.append(5008)  # Adaptive Force default
        shard_ids = shard_ids[:3]

        selected_perks = primary_runes + sub_runes + shard_ids

        return RuneData(
            primary_style=TREE_NAME_TO_ID[primary_tree_name],
            sub_style=TREE_NAME_TO_ID[sub_tree_name],
            selected_perks=selected_perks
        )

    def _extract_items_from_html(self, html: str) -> Optional[ItemBuild]:
        """
        Extract recommended items by parsing item icon image paths.
        U.GG uses img src like: /cdn/16.x.x/img/item/3020.png
        """
        item_pattern = re.compile(r'/img/item/(\d{4,5})\.png')
        item_ids = []
        seen = set()
        for match in item_pattern.finditer(html):
            item_id = int(match.group(1))
            # Filter out consumables and wards
            if item_id not in seen and item_id > 1000 and item_id not in (2003, 2055, 3340, 3364):
                seen.add(item_id)
                item_ids.append(item_id)

        if len(item_ids) < 3:
            return None

        return ItemBuild(
            starting_items=item_ids[:2],
            core_items=item_ids[2:5],
            situational_items=item_ids[5:8] if len(item_ids) >= 8 else item_ids[5:]
        )

    def _extract_summoner_spells(self, html: str, champion_id: int) -> List[int]:
        """Extract summoner spells from page, fallback to champion default"""
        from providers.champion_builds import CHAMPION_BUILDS
        # Spell icon pattern: SummonerFlash.png, SummonerDot.png etc.
        spell_map = {
            "SummonerFlash": 4, "SummonerDot": 14, "SummonerHaste": 6,
            "SummonerHeal": 7, "SummonerExhaust": 3, "SummonerSmite": 11,
            "SummonerTeleport": 12, "SummonerBoost": 1, "SummonerBarrier": 21,
        }
        spell_pattern = re.compile(r'(Summoner\w+)\.png')
        found = []
        seen = set()
        for match in spell_pattern.finditer(html):
            name = match.group(1)
            if name in spell_map and name not in seen:
                seen.add(name)
                found.append(spell_map[name])
            if len(found) == 2:
                return found

        # Fall back to champion-specific or default
        if champion_id in CHAMPION_BUILDS:
            return CHAMPION_BUILDS[champion_id].get('summoner_spells', [4, 14])
        return [4, 14]

    async def get_current_patch(self) -> Optional[str]:
        """Get current patch from Data Dragon"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://ddragon.leagueoflegends.com/api/versions.json", timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 200:
                        versions = await resp.json()
                        return versions[0]  # Latest patch
        except Exception:
            pass
        return "16.3.1"
