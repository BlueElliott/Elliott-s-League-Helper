"""
Elliott's League Helper with System Tray UI
Main application entry point with GUI
"""

import asyncio
import signal
import sys
import threading
from typing import Optional

from lcu.connector import LCUConnector
from lcu.websocket import LCUWebSocket
from lcu.api import LCUAPI
from providers.ugg_scraper import UGGScraperProvider, CHAMPION_NAMES as CHAMPION_ID_MAP
from runes.manager import RuneManager
from items.writer import ItemSetWriter
from ui.tray import TrayUI


# Convert champion names to title case for display
CHAMPION_NAMES = {k: v.title().replace("Khazix", "Kha'Zix").replace("Kogmaw", "Kog'Maw")
                 .replace("Reksai", "Rek'Sai").replace("Velkoz", "Vel'Koz")
                 .replace("Chogath", "Cho'Gath").replace("Kaisa", "Kai'Sa")
                 for k, v in CHAMPION_ID_MAP.items()}


class LeagueHelperWithUI:
    """Main application class with UI"""

    def __init__(self):
        self.connector = LCUConnector()
        self.api: Optional[LCUAPI] = None
        self.websocket: Optional[LCUWebSocket] = None
        self.provider = UGGScraperProvider()
        self.rune_manager: Optional[RuneManager] = None
        self.item_writer = ItemSetWriter()
        self.running = False
        self.current_patch = "14_1"
        self.tray_ui: Optional[TrayUI] = None
        self.event_loop: Optional[asyncio.AbstractEventLoop] = None

    async def start(self):
        """Start the application"""
        print("=" * 50)
        print("Elliott's League Helper (UI Mode)")
        print("=" * 50)
        print()

        # Connect to League client
        print("Waiting for League of Legends client...")
        if self.tray_ui:
            self.tray_ui.update_status(False, "Waiting for League client...")

        while not await self.connector.connect():
            await asyncio.sleep(5)

        print("[OK] Connected to League client")
        if self.tray_ui:
            self.tray_ui.update_status(True, "Connected")

        # Initialize components
        self.api = LCUAPI(self.connector)
        self.rune_manager = RuneManager(self.api, provider_name="U.GG")

        # Get summoner info
        summoner = await self.api.get_current_summoner()
        if summoner:
            name = summoner.get('displayName', 'Summoner')
            print(f"Welcome, {name}!")
            if self.tray_ui:
                self.tray_ui.update_status(True, f"Ready - {name}")

        # Get current patch
        patch = await self.provider.get_current_patch()
        if patch:
            self.current_patch = patch
            print(f"Current patch: {patch}")

        # Setup WebSocket
        self.websocket = LCUWebSocket(self.connector.port, self.connector.token)
        if await self.websocket.connect():
            print("[OK] WebSocket connected")
            print()

            # Register event handler
            self.websocket.on('/lol-champ-select/v1/session', self.on_champion_select)

            # Start listening
            self.running = True
            print("Listening for champion selections...")
            print("Use the system tray to control the app.")
            print()

            await self.websocket.listen()

    async def stop(self):
        """Stop the application"""
        print("\n[UI] Stopping application...")
        self.running = False

        if self.websocket:
            await self.websocket.disconnect()

        if self.connector:
            await self.connector.disconnect()

        if self.tray_ui:
            self.tray_ui.update_status(False, "Stopped")

        print("[OK] Stopped")

    async def on_champion_select(self, data: dict):
        """Handle champion selection event"""
        if not data or not self.running:
            return

        try:
            cell_id = data.get('localPlayerCellId')
            if cell_id is None:
                return

            my_team = data.get('myTeam', [])
            for player in my_team:
                if player.get('cellId') == cell_id:
                    champion_id = player.get('championId', 0)
                    if champion_id == 0:
                        return

                    role = player.get('assignedPosition', '').lower()
                    if not role:
                        role = 'middle'

                    # Prevent duplicate processing
                    if hasattr(self, '_last_champion') and self._last_champion == (champion_id, role):
                        return

                    self._last_champion = (champion_id, role)
                    await self.process_champion_selection(champion_id, role)
                    break

        except Exception as e:
            print(f"Error in champion select handler: {e}")

    async def process_champion_selection(self, champion_id: int, role: str):
        """Process champion selection and apply builds"""
        champion_name = CHAMPION_NAMES.get(champion_id, f"Champion{champion_id}")

        print(f"\n{'=' * 50}")
        print(f"Champion selected: {champion_name} ({role})")
        print(f"{'=' * 50}")

        if self.tray_ui:
            self.tray_ui.update_status(True, f"{champion_name} - Fetching...")

        # Fetch build data
        print("Fetching build data from U.GG...")
        build_data = await self.provider.get_build(champion_id, role, self.current_patch)

        if not build_data:
            print("[FAILED] Failed to fetch build data")
            if self.tray_ui:
                self.tray_ui.update_status(True, f"{champion_name} - Failed")
            return

        print("[OK] Build data retrieved")

        # Apply runes
        if build_data.runes:
            success = await self.rune_manager.apply_runes(
                build_data.runes,
                champion_name,
                role
            )

            if success:
                if self.tray_ui:
                    self.tray_ui.update_status(True, f"{champion_name} - Applied!")
            else:
                print("[FAILED] Failed to apply runes")
                if self.tray_ui:
                    self.tray_ui.update_status(True, f"{champion_name} - Error")

        print()

    def run_async_loop(self):
        """Run the async event loop in a separate thread"""
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        try:
            self.event_loop.run_until_complete(self.start())
        except Exception as e:
            print(f"Error in async loop: {e}")

    async def handle_start(self):
        """Handle UI start command"""
        if not self.running:
            # Start the async loop in a thread
            thread = threading.Thread(target=self.run_async_loop, daemon=True)
            thread.start()

    async def handle_stop(self):
        """Handle UI stop command"""
        if self.running and self.event_loop:
            asyncio.run_coroutine_threadsafe(self.stop(), self.event_loop)

    def handle_exit(self):
        """Handle UI exit command"""
        print("\n[UI] Exiting application...")
        if self.running and self.event_loop:
            self.event_loop.call_soon_threadsafe(self.event_loop.stop)
        sys.exit(0)


def main():
    """Main entry point with UI"""
    app = LeagueHelperWithUI()

    # Create tray UI
    tray = TrayUI(
        on_start=app.handle_start,
        on_stop=app.handle_stop,
        on_exit=app.handle_exit
    )

    app.tray_ui = tray

    print("Starting system tray UI...")
    print("Look for the icon in your system tray!")
    print()

    # Auto-start the application
    threading.Thread(target=app.run_async_loop, daemon=True).start()

    # Run tray (blocks until exit)
    tray.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
