"""
System Tray UI
Provides a simple system tray interface for the app
"""

import asyncio
import threading
from typing import Optional, Callable
from PIL import Image, ImageDraw
import pystray


class TrayUI:
    """System tray icon and menu"""

    def __init__(self, on_start: Callable, on_stop: Callable, on_exit: Callable):
        """
        Initialize system tray

        Args:
            on_start: Callback when user clicks "Start"
            on_stop: Callback when user clicks "Stop"
            on_exit: Callback when user clicks "Exit"
        """
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_exit = on_exit
        self.icon: Optional[pystray.Icon] = None
        self.is_running = False

    def create_icon(self, color='green'):
        """Create a simple colored circle icon"""
        # Create a 64x64 image
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)

        # Draw a colored circle
        if color == 'green':
            fill_color = (34, 139, 34)  # Green - running
        elif color == 'red':
            fill_color = (220, 20, 60)  # Red - stopped
        else:
            fill_color = (128, 128, 128)  # Gray - idle

        draw.ellipse([8, 8, 56, 56], fill=fill_color, outline='black', width=2)

        return image

    def start_clicked(self, icon, item):
        """Handle Start menu click"""
        print("[UI] Start clicked")
        self.is_running = True
        icon.icon = self.create_icon('green')
        if self.on_start:
            # Run async callback in thread
            threading.Thread(target=lambda: asyncio.run(self.on_start()), daemon=True).start()

    def stop_clicked(self, icon, item):
        """Handle Stop menu click"""
        print("[UI] Stop clicked")
        self.is_running = False
        icon.icon = self.create_icon('red')
        if self.on_stop:
            threading.Thread(target=lambda: asyncio.run(self.on_stop()), daemon=True).start()

    def exit_clicked(self, icon, item):
        """Handle Exit menu click"""
        print("[UI] Exit clicked")
        if self.on_exit:
            self.on_exit()
        icon.stop()

    def create_menu(self):
        """Create the tray menu"""
        return pystray.Menu(
            pystray.MenuItem(
                "Elliott's League Helper",
                lambda: None,
                enabled=False
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Start",
                self.start_clicked,
                default=True
            ),
            pystray.MenuItem(
                "Stop",
                self.stop_clicked
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Exit",
                self.exit_clicked
            )
        )

    def run(self):
        """Run the system tray (blocks until exit)"""
        icon = pystray.Icon(
            "league_helper",
            self.create_icon('red'),  # Start as stopped
            "Elliott's League Helper",
            self.create_menu()
        )

        self.icon = icon
        print("[UI] System tray started")
        icon.run()

    def update_status(self, running: bool, message: str = ""):
        """Update the tray icon status"""
        if self.icon:
            color = 'green' if running else 'red'
            self.icon.icon = self.create_icon(color)
            if message:
                self.icon.title = f"Elliott's League Helper - {message}"
