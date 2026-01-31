"""
LCU API Wrapper
Provides convenient methods for interacting with League Client API
"""

from typing import Optional, List, Dict
from lcu.connector import LCUConnector


class LCUAPI:
    """High-level API wrapper for common LCU operations"""

    def __init__(self, connector: LCUConnector):
        self.connector = connector

    # === Summoner Info ===

    async def get_current_summoner(self) -> Optional[dict]:
        """Get current summoner information"""
        return await self.connector.get('/lol-summoner/v1/current-summoner')

    # === Rune Pages ===

    async def get_rune_pages(self) -> Optional[List[dict]]:
        """Get all rune pages"""
        return await self.connector.get('/lol-perks/v1/pages')

    async def get_current_rune_page(self) -> Optional[dict]:
        """Get currently selected rune page"""
        return await self.connector.get('/lol-perks/v1/currentpage')

    async def create_rune_page(self, rune_page: dict) -> Optional[dict]:
        """
        Create a new rune page

        Args:
            rune_page: Rune page data with format:
            {
                "name": "Page Name",
                "primaryStyleId": 8200,
                "subStyleId": 8000,
                "selectedPerkIds": [8214, 8224, 8233, 8237, 8345, 8347, 5008, 5008, 5001],
                "current": true
            }

        Returns:
            Created rune page or None if failed
        """
        return await self.connector.post('/lol-perks/v1/pages', json=rune_page)

    async def delete_rune_page(self, page_id: int) -> bool:
        """
        Delete a rune page

        Args:
            page_id: ID of the page to delete

        Returns:
            True if successful
        """
        result = await self.connector.delete(f'/lol-perks/v1/pages/{page_id}')
        return result is not None

    async def apply_rune_page(self, name: str, primary_style: int, sub_style: int,
                             selected_perks: List[int]) -> Optional[dict]:
        """
        Apply a new rune page (creates and sets as active)

        Args:
            name: Display name for the rune page
            primary_style: Primary tree ID (e.g., 8200 for Sorcery)
            sub_style: Secondary tree ID
            selected_perks: List of 9 perk IDs [keystone, slot1, slot2, slot3, sub1, sub2, shard1, shard2, shard3]

        Returns:
            Created rune page or None if failed
        """
        # First, try to delete old temporary pages to avoid hitting the 25 page limit
        await self._cleanup_temp_pages()

        rune_page = {
            "name": name,
            "primaryStyleId": primary_style,
            "subStyleId": sub_style,
            "selectedPerkIds": selected_perks,
            "current": True  # Set as active page
        }

        return await self.create_rune_page(rune_page)

    async def _cleanup_temp_pages(self):
        """
        Delete temporary rune pages created by the app
        Keeps only permanent user pages
        """
        pages = await self.get_rune_pages()
        if not pages:
            return

        # Delete pages that look like they were auto-generated
        # (you can customize this logic based on your naming convention)
        temp_prefixes = ['U.GG', 'OP.GG', 'Lolalytics', 'Auto']

        for page in pages:
            # Skip if it's the only page (can't delete all pages)
            if len(pages) <= 1:
                break

            # Skip if it's a default page
            if page.get('isDefaultPage', False):
                continue

            # Delete if it matches our naming pattern
            page_name = page.get('name', '')
            if any(page_name.startswith(prefix) for prefix in temp_prefixes):
                await self.delete_rune_page(page['id'])

    # === Champion Select ===

    async def get_champ_select_session(self) -> Optional[dict]:
        """
        Get current champion select session data
        Returns None if not in champion select
        """
        return await self.connector.get('/lol-champ-select/v1/session')

    async def get_local_player_cell_id(self) -> Optional[int]:
        """Get the local player's cell ID in champion select"""
        session = await self.get_champ_select_session()
        if not session:
            return None
        return session.get('localPlayerCellId')

    async def get_selected_champion(self) -> Optional[dict]:
        """
        Get currently selected/locked champion for local player

        Returns:
            {
                'championId': int,
                'assignedPosition': str (e.g., 'top', 'jungle', 'middle', 'bottom', 'utility')
            }
            or None if not in champ select or no champion selected
        """
        session = await self.get_champ_select_session()
        if not session:
            return None

        cell_id = session.get('localPlayerCellId')
        if cell_id is None:
            return None

        # Find local player in myTeam
        my_team = session.get('myTeam', [])
        for player in my_team:
            if player.get('cellId') == cell_id:
                champion_id = player.get('championId', 0)
                if champion_id == 0:  # No champion selected yet
                    return None

                return {
                    'championId': champion_id,
                    'assignedPosition': player.get('assignedPosition', ''),
                    'cellId': cell_id
                }

        return None

    # === Game Session ===

    async def get_gameflow_phase(self) -> Optional[str]:
        """
        Get current gameflow phase
        Possible values: 'None', 'Lobby', 'Matchmaking', 'CheckedIntoTournament',
                        'ReadyCheck', 'ChampSelect', 'GameStart', 'InProgress',
                        'WaitingForStats', 'PreEndOfGame', 'EndOfGame'
        """
        result = await self.connector.get('/lol-gameflow/v1/gameflow-phase')
        if isinstance(result, str):
            return result
        return None

    async def is_in_champ_select(self) -> bool:
        """Check if currently in champion select"""
        phase = await self.get_gameflow_phase()
        return phase == 'ChampSelect'

    # === Summoner Spells ===

    async def get_summoner_spells(self) -> Optional[List[dict]]:
        """Get available summoner spells"""
        return await self.connector.get('/lol-game-data/assets/v1/summoner-spells.json')
