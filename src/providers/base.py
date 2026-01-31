"""
Base provider class
Defines the interface for data providers (U.GG, OP.GG, etc.)
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, List


class RuneData:
    """Data structure for rune information"""

    def __init__(self, primary_style: int, sub_style: int, selected_perks: List[int]):
        self.primary_style = primary_style
        self.sub_style = sub_style
        self.selected_perks = selected_perks  # List of 9 perk IDs

    def to_dict(self) -> dict:
        """Convert to LCU API format"""
        return {
            'primaryStyleId': self.primary_style,
            'subStyleId': self.sub_style,
            'selectedPerkIds': self.selected_perks
        }


class ItemBuild:
    """Data structure for item build information"""

    def __init__(self, starting_items: List[int], core_items: List[int],
                 situational_items: Optional[List[int]] = None):
        self.starting_items = starting_items  # List of item IDs
        self.core_items = core_items  # List of item IDs
        self.situational_items = situational_items or []  # Optional items

    def to_dict(self) -> dict:
        """Convert to item set file format"""
        return {
            'starting_items': self.starting_items,
            'core_items': self.core_items,
            'situational_items': self.situational_items
        }


class BuildData:
    """Combined rune and item build data"""

    def __init__(self, runes: RuneData, items: ItemBuild, summoner_spells: Optional[List[int]] = None):
        self.runes = runes
        self.items = items
        self.summoner_spells = summoner_spells or []


class BaseProvider(ABC):
    """
    Abstract base class for build data providers
    Each provider (U.GG, OP.GG, etc.) implements this interface
    """

    def __init__(self):
        self.name = "BaseProvider"

    @abstractmethod
    async def get_build(self, champion_id: int, role: str, patch: str) -> Optional[BuildData]:
        """
        Fetch build data for a champion

        Args:
            champion_id: Champion ID (e.g., 103 for Ahri)
            role: Role/position (e.g., 'middle', 'top', 'jungle', 'bottom', 'support')
            patch: Patch version (e.g., '14.1')

        Returns:
            BuildData object or None if not found
        """
        pass

    @abstractmethod
    async def get_aram_build(self, champion_id: int, patch: str) -> Optional[BuildData]:
        """
        Fetch ARAM build data for a champion

        Args:
            champion_id: Champion ID
            patch: Patch version

        Returns:
            BuildData object or None if not found
        """
        pass

    def normalize_role(self, role: str) -> str:
        """
        Normalize role names to match provider's format

        Args:
            role: Role from LCU (e.g., 'JUNGLE', 'middle', 'utility')

        Returns:
            Normalized role name
        """
        role_map = {
            'top': 'top',
            'jungle': 'jungle',
            'middle': 'middle',
            'mid': 'middle',
            'bottom': 'bottom',
            'adc': 'bottom',
            'utility': 'support',
            'support': 'support'
        }

        normalized = role_map.get(role.lower(), role.lower())
        return normalized
