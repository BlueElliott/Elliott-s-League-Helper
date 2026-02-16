"""
Elliott's League Helper with Visual GUI
Main application with proper window interface
"""

import asyncio
import sys
import threading
from typing import Optional

from lcu.connector import LCUConnector
from lcu.websocket import LCUWebSocket
from lcu.api import LCUAPI
from providers.ugg_scraper import UGGScraperProvider, CHAMPION_NAMES as CHAMPION_ID_MAP
from runes.manager import RuneManager
from items.writer import ItemSetWriter
from ui.main_window import RuneDisplayWindow


# Convert champion names to title case
CHAMPION_NAMES = {k: v.title().replace("Khazix", "Kha'Zix").replace("Kogmaw", "Kog'Maw")
                 .replace("Reksai", "Rek'Sai").replace("Velkoz", "Vel'Koz")
                 .replace("Chogath", "Cho'Gath").replace("Kaisa", "Kai'Sa")
                 for k, v in CHAMPION_ID_MAP.items()}


class VisualLeagueHelper:
    """Main application with visual GUI"""

    def __init__(self, gui: RuneDisplayWindow):
        self.gui = gui
        self.connector = LCUConnector()
        self.api: Optional[LCUAPI] = None
        self.websocket: Optional[LCUWebSocket] = None
        self.provider = UGGScraperProvider()
        self.rune_manager: Optional[RuneManager] = None
        self.item_writer = ItemSetWriter()
        self.running = False
        self.current_patch = "14_1"
        self.event_loop: Optional[asyncio.AbstractEventLoop] = None

    async def start(self):
        """Start the application"""
        print("=" * 50)
        print("Elliott's League Helper (Visual Mode)")
        print("=" * 50)
        print()

        self.gui.update_status("Connecting to League client...")

        # Connect to League client
        print("Waiting for League of Legends client...")
        while not await self.connector.connect():
            await asyncio.sleep(5)

        print("[OK] Connected to League client")
        self.gui.update_status("Connected to League client", '#4ecca3')

        # Initialize components
        self.api = LCUAPI(self.connector)
        self.rune_manager = RuneManager(self.api, provider_name="U.GG")

        # Get summoner info
        summoner = await self.api.get_current_summoner()
        if summoner:
            name = summoner.get('displayName', 'Summoner')
            print(f"Welcome, {name}!")
            self.gui.update_status(f"Ready - {name}", '#4ecca3')

        # Get current patch
        try:
            patch = await self.provider.get_current_patch()
            if patch:
                self.current_patch = patch
                print(f"Current patch: {patch}")
        except Exception as e:
            print(f"Could not get patch: {e}")

        # Setup WebSocket
        self.websocket = LCUWebSocket(self.connector.port, self.connector.token)
        if await self.websocket.connect():
            print("[OK] WebSocket connected")

            # Register event handler
            self.websocket.on('/lol-champ-select/v1/session', self.on_champion_select)

            # Start listening
            self.running = True
            print("Listening for champion selections...")
            self.gui.update_status("Waiting for champion selection...", 'white')

            await self.websocket.listen()

    async def stop(self):
        """Stop the application"""
        print("\n[APP] Stopping...")
        self.running = False

        if self.websocket:
            await self.websocket.disconnect()

        if self.connector:
            await self.connector.disconnect()

        self.gui.update_status("Stopped", '#ff6b6b')
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
                    # Check both championId (locked) and championPickIntent (hovering)
                    champion_id = player.get('championId', 0)

                    # If not locked, check hover/pick intent
                    if champion_id == 0:
                        champion_id = player.get('championPickIntent', 0)

                    if champion_id == 0:
                        return  # No champion selected or hovered

                    role = player.get('assignedPosition', '').lower()

                    # Prevent duplicate processing of same champion
                    if hasattr(self, '_last_champion') and self._last_champion == (champion_id, role):
                        return

                    self._last_champion = (champion_id, role)
                    await self.process_champion_selection(champion_id, role)
                    break

        except Exception as e:
            print(f"Error in champion select handler: {e}")
            import traceback
            traceback.print_exc()

    async def process_champion_selection(self, champion_id: int, role: str):
        """Process champion selection and display builds"""
        champion_name = CHAMPION_NAMES.get(champion_id, f"Champion{champion_id}")

        # Handle practice tool / no-role modes
        if not role or role == '':
            role = 'top'  # Default for practice tool
            print(f"[INFO] No role detected (Practice Tool?), using default: {role}")

        # Store for apply function
        self._current_champion_name = champion_name
        self._current_role = role

        print(f"\n{'=' * 50}")
        print(f"Champion selected: {champion_name} ({role})")
        print(f"{'=' * 50}")

        self.gui.update_status(f"Fetching {champion_name} build...", '#ffd93d')

        # Fetch build data
        print("Fetching build data from U.GG...")
        build_data = await self.provider.get_build(champion_id, role, self.current_patch)

        if not build_data:
            print("[FAILED] Failed to fetch build data")
            self.gui.update_status(f"Failed to fetch {champion_name} build", '#ff6b6b')
            return

        print("[OK] Build data retrieved")

        # Display in GUI
        self.gui.display_build(champion_name, role, build_data)
        self.gui.update_status(f"{champion_name} build ready - Click 'Apply Runes'", '#4ecca3')

        print()

    async def apply_build(self, build_data):
        """Apply the build to League client"""
        print("Applying runes...")

        if build_data.runes:
            # Get champion name and role from last selection
            champion_name = getattr(self, '_current_champion_name', 'Champion')
            role = getattr(self, '_current_role', 'mid')

            success = await self.rune_manager.apply_runes(
                build_data.runes,
                champion_name,
                role
            )

            if success:
                self.gui.update_status(f"Runes applied for {champion_name}!", '#4ecca3')
            else:
                self.gui.update_status("Failed to apply runes", '#ff6b6b')

    def run_async_loop(self):
        """Run the async event loop in a separate thread"""
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        try:
            self.event_loop.run_until_complete(self.start())
        except Exception as e:
            print(f"Error in async loop: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point with visual GUI"""

    # Create GUI window
    def on_apply_runes(build_data):
        """Handle apply runes button click"""
        if hasattr(main, 'app') and main.app.event_loop:
            asyncio.run_coroutine_threadsafe(
                main.app.apply_build(build_data),
                main.app.event_loop
            )

    gui = RuneDisplayWindow(on_apply=on_apply_runes)

    # Create app instance
    app = VisualLeagueHelper(gui)
    main.app = app  # Store for callback access

    # Start async loop in background thread
    thread = threading.Thread(target=app.run_async_loop, daemon=True)
    thread.start()

    # Run GUI (blocks until window closes)
    print("Starting visual GUI...")
    print("Window should appear...")
    gui.run()

    # Cleanup on exit
    if app.event_loop:
        app.event_loop.call_soon_threadsafe(app.event_loop.stop)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
