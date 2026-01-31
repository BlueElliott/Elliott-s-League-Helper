"""
Elliott's League Helper
Main application entry point
"""

import asyncio
import signal
import sys
from typing import Optional

from lcu.connector import LCUConnector
from lcu.websocket import LCUWebSocket
from lcu.api import LCUAPI
from providers.ugg import UGGProvider
from runes.manager import RuneManager
from items.writer import ItemSetWriter


# Champion ID to name mapping (partial - will be expanded with Data Dragon)
CHAMPION_NAMES = {
    1: "Annie", 2: "Olaf", 3: "Galio", 4: "TwistedFate", 5: "XinZhao",
    6: "Urgot", 7: "LeBlanc", 8: "Vladimir", 9: "Fiddlesticks", 10: "Kayle",
    # Add more as needed or fetch from Data Dragon
    103: "Ahri", 84: "Akali", 12: "Alistar", 32: "Amumu", 34: "Anivia",
    # This will be replaced with full Data Dragon integration
}


class LeagueHelper:
    """Main application class"""

    def __init__(self):
        self.connector = LCUConnector()
        self.api: Optional[LCUAPI] = None
        self.websocket: Optional[LCUWebSocket] = None
        self.provider = UGGProvider()
        self.rune_manager: Optional[RuneManager] = None
        self.item_writer = ItemSetWriter()
        self.running = False
        self.current_patch = "14_1"  # Will be updated on startup

    async def start(self):
        """Start the application"""
        print("=" * 50)
        print("Elliott's League Helper")
        print("=" * 50)
        print()

        # Connect to League client
        print("Waiting for League of Legends client...")
        while not await self.connector.connect():
            await asyncio.sleep(5)

        print("✓ Connected to League client")
        print()

        # Initialize components
        self.api = LCUAPI(self.connector)
        self.rune_manager = RuneManager(self.api, provider_name="U.GG")

        # Get summoner info
        summoner = await self.api.get_current_summoner()
        if summoner:
            print(f"Welcome, {summoner.get('displayName', 'Summoner')}!")
            print()

        # Get current patch
        patch = await self.provider.get_current_patch()
        if patch:
            self.current_patch = patch
            print(f"Current patch: {patch}")
            print()

        # Setup WebSocket
        self.websocket = LCUWebSocket(self.connector.port, self.connector.token)
        if await self.websocket.connect():
            print("✓ WebSocket connected")
            print()

            # Register event handler for champion select
            self.websocket.on('/lol-champ-select/v1/session', self.on_champion_select)

            # Start listening for events
            self.running = True
            print("Listening for champion selections...")
            print("(Press Ctrl+C to exit)")
            print()

            await self.websocket.listen()

    async def stop(self):
        """Stop the application"""
        print("\nShutting down...")
        self.running = False

        if self.websocket:
            await self.websocket.disconnect()

        if self.connector:
            await self.connector.disconnect()

        print("Goodbye!")

    async def on_champion_select(self, data: dict):
        """
        Handle champion selection event

        Args:
            data: Champion select session data
        """
        if not data:
            return

        try:
            # Get local player's selection
            cell_id = data.get('localPlayerCellId')
            if cell_id is None:
                return

            my_team = data.get('myTeam', [])
            for player in my_team:
                if player.get('cellId') == cell_id:
                    champion_id = player.get('championId', 0)
                    if champion_id == 0:
                        return  # No champion selected yet

                    role = player.get('assignedPosition', '').lower()
                    if not role:
                        role = 'middle'  # Default

                    # Check if we've already processed this selection
                    if hasattr(self, '_last_champion') and self._last_champion == (champion_id, role):
                        return

                    self._last_champion = (champion_id, role)

                    # Process the selection
                    await self.process_champion_selection(champion_id, role)
                    break

        except Exception as e:
            print(f"Error in champion select handler: {e}")

    async def process_champion_selection(self, champion_id: int, role: str):
        """
        Process champion selection and apply builds

        Args:
            champion_id: Selected champion ID
            role: Assigned role
        """
        champion_name = CHAMPION_NAMES.get(champion_id, f"Champion{champion_id}")

        print(f"\n{'=' * 50}")
        print(f"Champion selected: {champion_name} ({role})")
        print(f"{'=' * 50}")

        # Fetch build data
        print("Fetching build data from U.GG...")
        build_data = await self.provider.get_build(champion_id, role, self.current_patch)

        if not build_data:
            print("✗ Failed to fetch build data")
            return

        print("✓ Build data retrieved")

        # Apply runes
        if build_data.runes:
            success = await self.rune_manager.apply_runes(
                build_data.runes,
                champion_name,
                role
            )
            if not success:
                print("✗ Failed to apply runes")

        # Create item set (optional - requires champion key)
        # This would need Data Dragon integration for proper champion keys
        # For now, we'll skip item sets in the MVP

        print()


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nReceived interrupt signal...")
    sys.exit(0)


async def main():
    """Main entry point"""
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Create and start application
    app = LeagueHelper()

    try:
        await app.start()
    except KeyboardInterrupt:
        await app.stop()
    except Exception as e:
        print(f"Fatal error: {e}")
        await app.stop()


if __name__ == "__main__":
    # Run the application
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
