"""
Item Set Writer
Creates item set files for the League client
"""

import json
import os
from pathlib import Path
from typing import Optional, List
from ..providers.base import ItemBuild


class ItemSetWriter:
    """Writes item sets to the League client's file system"""

    def __init__(self, league_path: Optional[str] = None):
        """
        Initialize ItemSetWriter

        Args:
            league_path: Path to League of Legends installation
                        If None, will try to auto-detect
        """
        self.league_path = league_path or self._find_league_path()

    def _find_league_path(self) -> Optional[str]:
        """
        Auto-detect League of Legends installation path

        Returns:
            Path to League installation or None
        """
        # Common installation paths
        possible_paths = [
            "C:/Riot Games/League of Legends",
            "C:/Program Files/Riot Games/League of Legends",
            "C:/Program Files (x86)/Riot Games/League of Legends",
        ]

        # Check environment variable
        if 'LEAGUE_PATH' in os.environ:
            possible_paths.insert(0, os.environ['LEAGUE_PATH'])

        for path in possible_paths:
            if os.path.exists(path):
                return path

        return None

    def write_item_set(self, champion_key: str, champion_name: str, role: str,
                      items: ItemBuild, source: str = "Auto") -> bool:
        """
        Write an item set file for a champion

        Args:
            champion_key: Champion key (e.g., 'Ahri', 'MonkeyKing')
            champion_name: Display name
            role: Role (for title)
            items: ItemBuild object
            source: Source name (e.g., 'U.GG')

        Returns:
            True if successful
        """
        if not self.league_path:
            print("League of Legends path not found")
            return False

        try:
            # Create directory path
            # Format: {LeaguePath}/Config/Champions/{ChampionKey}/Recommended/
            config_dir = Path(self.league_path) / "Config" / "Champions" / champion_key / "Recommended"
            config_dir.mkdir(parents=True, exist_ok=True)

            # Create item set data
            item_set = self._create_item_set_json(
                champion_name=champion_name,
                role=role,
                items=items,
                source=source
            )

            # Write to file
            filename = f"{source}_{role}.json"
            file_path = config_dir / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(item_set, f, indent=2)

            print(f"✓ Created item set: {file_path}")
            return True

        except Exception as e:
            print(f"Error writing item set: {e}")
            return False

    def _create_item_set_json(self, champion_name: str, role: str,
                             items: ItemBuild, source: str) -> dict:
        """
        Create item set JSON structure

        Args:
            champion_name: Champion display name
            role: Role
            items: ItemBuild object
            source: Source name

        Returns:
            Item set dict in League's format
        """
        blocks = []

        # Starting items block
        if items.starting_items:
            blocks.append({
                "type": "Starting Items",
                "items": [{"id": str(item_id), "count": 1}
                         for item_id in items.starting_items]
            })

        # Core build block
        if items.core_items:
            blocks.append({
                "type": "Core Build",
                "recMath": False,
                "items": [{"id": str(item_id), "count": 1}
                         for item_id in items.core_items]
            })

        # Situational items block
        if items.situational_items:
            blocks.append({
                "type": "Situational Items",
                "recMath": False,
                "items": [{"id": str(item_id), "count": 1}
                         for item_id in items.situational_items]
            })

        return {
            "title": f"{source} - {champion_name} {role.capitalize()}",
            "associatedMaps": [11],  # Summoner's Rift
            "associatedChampions": [],  # Leave empty to apply to champion
            "blocks": blocks,
            "map": "SR",
            "mode": "CLASSIC",
            "priority": False,
            "sortrank": 0,
            "startedFrom": "blank",
            "type": "custom"
        }

    def write_aram_item_set(self, champion_key: str, champion_name: str,
                           items: ItemBuild, source: str = "Auto") -> bool:
        """
        Write an ARAM item set

        Args:
            champion_key: Champion key
            champion_name: Display name
            items: ItemBuild object
            source: Source name

        Returns:
            True if successful
        """
        if not self.league_path:
            return False

        try:
            config_dir = Path(self.league_path) / "Config" / "Champions" / champion_key / "Recommended"
            config_dir.mkdir(parents=True, exist_ok=True)

            # Create ARAM item set
            item_set = self._create_aram_item_set_json(champion_name, items, source)

            filename = f"{source}_ARAM.json"
            file_path = config_dir / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(item_set, f, indent=2)

            print(f"✓ Created ARAM item set: {file_path}")
            return True

        except Exception as e:
            print(f"Error writing ARAM item set: {e}")
            return False

    def _create_aram_item_set_json(self, champion_name: str, items: ItemBuild,
                                   source: str) -> dict:
        """Create ARAM item set JSON"""
        blocks = []

        # ARAM starting items
        if items.starting_items:
            blocks.append({
                "type": "ARAM Starting Items",
                "items": [{"id": str(item_id), "count": 1}
                         for item_id in items.starting_items]
            })

        # Core build
        if items.core_items:
            blocks.append({
                "type": "Core Build",
                "recMath": False,
                "items": [{"id": str(item_id), "count": 1}
                         for item_id in items.core_items]
            })

        return {
            "title": f"{source} - {champion_name} ARAM",
            "associatedMaps": [12],  # ARAM
            "associatedChampions": [],
            "blocks": blocks,
            "map": "HA",
            "mode": "ARAM",
            "priority": False,
            "sortrank": 0,
            "startedFrom": "blank",
            "type": "custom"
        }
