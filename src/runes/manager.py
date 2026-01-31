"""
Rune Manager
Handles applying runes to the League client
"""

from typing import Optional
from ..lcu.api import LCUAPI
from ..providers.base import BuildData, RuneData


class RuneManager:
    """Manages rune page creation and application"""

    def __init__(self, lcu_api: LCUAPI, provider_name: str = "Auto"):
        self.lcu_api = lcu_api
        self.provider_name = provider_name

    async def apply_build(self, build_data: BuildData, champion_name: str, role: str) -> bool:
        """
        Apply a complete build (runes) to the League client

        Args:
            build_data: BuildData containing runes and items
            champion_name: Name of the champion (for display)
            role: Role being played

        Returns:
            True if successful
        """
        return await self.apply_runes(
            build_data.runes,
            champion_name,
            role
        )

    async def apply_runes(self, runes: RuneData, champion_name: str, role: str) -> bool:
        """
        Apply rune page to League client

        Args:
            runes: RuneData object with rune configuration
            champion_name: Name of the champion
            role: Role being played

        Returns:
            True if successfully applied
        """
        try:
            # Create page name
            page_name = f"{self.provider_name} - {champion_name} {role.capitalize()}"

            # Apply the rune page
            result = await self.lcu_api.apply_rune_page(
                name=page_name,
                primary_style=runes.primary_style,
                sub_style=runes.sub_style,
                selected_perks=runes.selected_perks
            )

            if result:
                print(f"✓ Applied runes: {page_name}")
                return True
            else:
                print(f"✗ Failed to apply runes: {page_name}")
                return False

        except Exception as e:
            print(f"Error applying runes: {e}")
            return False

    async def get_current_runes(self) -> Optional[dict]:
        """Get the currently active rune page"""
        return await self.lcu_api.get_current_rune_page()

    async def cleanup_old_pages(self):
        """Remove old auto-generated rune pages"""
        await self.lcu_api._cleanup_temp_pages()
