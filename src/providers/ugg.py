"""
U.GG Provider
Fetches build data from U.GG's structured API endpoints
"""

import aiohttp
from typing import Optional, Dict, List
from providers.base import BaseProvider, BuildData, RuneData, ItemBuild


class UGGProvider(BaseProvider):
    """Provider for U.GG data"""

    def __init__(self):
        super().__init__()
        self.name = "U.GG"
        self.base_url = "https://stats2.u.gg/lol/1.5"

    async def get_build(self, champion_id: int, role: str, patch: str) -> Optional[BuildData]:
        """
        Fetch build data from U.GG

        Args:
            champion_id: Champion ID
            role: Role (top, jungle, middle, bottom, support)
            patch: Patch version (e.g., '14.1')

        Returns:
            BuildData or None if not found
        """
        role = self.normalize_role(role)

        # U.GG URL format:
        # https://stats2.u.gg/lol/1.5/overview/{patch}/ranked_solo_5x5/{champion_id}/{role}/1.5.0.json
        url = f"{self.base_url}/overview/{patch}/ranked_solo_5x5/{champion_id}/{role}/1.5.0.json"

        try:
            print(f"DEBUG: Fetching from URL: {url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    print(f"DEBUG: Response status: {response.status}")
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"DEBUG: Error response: {error_text[:200]}")
                        return None

                    data = await response.json()
                    print(f"DEBUG: Successfully fetched data")
                    return self._parse_build_data(data)

        except Exception as e:
            print(f"U.GG fetch error: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def get_aram_build(self, champion_id: int, patch: str) -> Optional[BuildData]:
        """
        Fetch ARAM build data from U.GG

        Args:
            champion_id: Champion ID
            patch: Patch version

        Returns:
            BuildData or None if not found
        """
        # U.GG ARAM URL format:
        # https://stats2.u.gg/lol/1.5/overview/{patch}/normal_aram/{champion_id}/1.5.0.json
        url = f"{self.base_url}/overview/{patch}/normal_aram/{champion_id}/1.5.0.json"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None

                    data = await response.json()
                    return self._parse_build_data(data)

        except Exception as e:
            print(f"U.GG ARAM fetch error: {e}")
            return None

    def _parse_build_data(self, data: dict) -> Optional[BuildData]:
        """
        Parse U.GG response into BuildData object

        Args:
            data: Raw U.GG API response

        Returns:
            BuildData object or None if parsing failed
        """
        try:
            # Extract rune data
            runes_data = self._extract_runes(data)
            if not runes_data:
                return None

            # Extract item data
            items_data = self._extract_items(data)
            if not items_data:
                return None

            # Extract summoner spells
            summoner_spells = self._extract_summoner_spells(data)

            return BuildData(
                runes=runes_data,
                items=items_data,
                summoner_spells=summoner_spells
            )

        except Exception as e:
            print(f"U.GG parsing error: {e}")
            return None

    def _extract_runes(self, data: dict) -> Optional[RuneData]:
        """
        Extract rune configuration from U.GG data

        U.GG format stores runes in the 'runes' section with the most popular build
        """
        try:
            # Navigate to runes data
            # Format: data -> runes -> [0] (highest pick rate) -> perks
            runes_section = data.get('runes', [])
            if not runes_section:
                return None

            # Get most popular rune page (first entry)
            best_runes = runes_section[0]

            # Primary tree
            primary_style = best_runes.get('primaryStyle')

            # Secondary tree
            sub_style = best_runes.get('subStyle')

            # Perk selections
            perks = best_runes.get('perks', [])

            if not primary_style or not sub_style or not perks:
                return None

            return RuneData(
                primary_style=primary_style,
                sub_style=sub_style,
                selected_perks=perks
            )

        except Exception as e:
            print(f"Rune extraction error: {e}")
            return None

    def _extract_items(self, data: dict) -> Optional[ItemBuild]:
        """
        Extract item build from U.GG data

        U.GG provides starting items, core build, and full build
        """
        try:
            # Navigate to item data
            # Format: data -> items -> item_builds -> [0] (most popular)
            items_section = data.get('items', {})
            item_builds = items_section.get('item_builds', [])

            if not item_builds:
                return None

            # Get most popular build
            best_build = item_builds[0]

            # Starting items (boots + starter items)
            starting = best_build.get('starting_items', [])

            # Core items
            core = best_build.get('core_items', [])

            # Full build (can be used as situational)
            full_build = best_build.get('item_options', [])

            return ItemBuild(
                starting_items=starting,
                core_items=core,
                situational_items=full_build
            )

        except Exception as e:
            print(f"Item extraction error: {e}")
            return None

    def _extract_summoner_spells(self, data: dict) -> List[int]:
        """
        Extract recommended summoner spells

        Args:
            data: U.GG API response

        Returns:
            List of summoner spell IDs (e.g., [4, 14] for Flash/Ignite)
        """
        try:
            summoner_spells = data.get('summoner_spells', [])
            if summoner_spells:
                # Get most popular spell combination (first entry)
                best_spells = summoner_spells[0]
                return best_spells.get('spells', [])

        except Exception:
            pass

        return []

    async def get_current_patch(self) -> Optional[str]:
        """
        Get the current patch version from U.GG

        Returns:
            Patch string (e.g., '14_1') or None
        """
        try:
            # U.GG has a version endpoint
            url = "https://stats2.u.gg/lol/1.5/current_patch.json"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Format is usually '14_1' (underscore instead of dot)
                        return data.get('patch', None)

        except Exception:
            pass

        # Fallback: use a default recent patch
        return "14_1"
