"""
Main GUI Window
Visual interface with rune and item icons
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from providers.base import BuildData
from PIL import Image, ImageTk
import io
import requests
from functools import lru_cache


# Rune tree names and colors
RUNE_TREES = {
    8000: ("Precision", "#C8AA6E"),
    8100: ("Domination", "#DC354A"),
    8200: ("Sorcery", "#5E9BE0"),
    8300: ("Inspiration", "#49AAB9"),
    8400: ("Resolve", "#00A550")
}

# Summoner spell names
SUMMONER_SPELLS = {
    1: "Cleanse", 3: "Exhaust", 4: "Flash", 6: "Ghost", 7: "Heal",
    11: "Smite", 12: "Teleport", 13: "Clarity", 14: "Ignite", 21: "Barrier"
}

# CDN URL for assets
DDRAGON_VERSION = "16.3.1"
RUNE_CDN = f"https://ddragon.leagueoflegends.com/cdn/img/"
ITEM_CDN = f"https://ddragon.leagueoflegends.com/cdn/{DDRAGON_VERSION}/img/item/"
SPELL_CDN = f"https://ddragon.leagueoflegends.com/cdn/{DDRAGON_VERSION}/img/spell/"


@lru_cache(maxsize=200)
def fetch_image(url: str, size: tuple = (48, 48)) -> Optional[ImageTk.PhotoImage]:
    """Fetch and cache an image from URL"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Failed to load image {url}: {e}")
    return None


class RuneDisplayWindow:
    """Main GUI window with visual rune and item display"""

    def __init__(self, on_apply: Optional[Callable] = None):
        """Initialize GUI window"""
        self.on_apply = on_apply
        self.current_build: Optional[BuildData] = None
        self.image_refs = []  # Keep references to prevent garbage collection

        # Create main window
        self.root = tk.Tk()
        self.root.title("Elliott's League Helper")
        self.root.geometry("700x800")
        self.root.resizable(False, False)
        self.root.configure(bg='#0a0e27')

        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass

        self._create_widgets()

    def _create_widgets(self):
        """Create all GUI widgets"""

        # Header
        header_frame = tk.Frame(self.root, bg='#1a1a2e', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="Elliott's League Helper",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg='#1a1a2e'
        )
        title_label.pack(pady=15)

        # Status bar
        status_frame = tk.Frame(self.root, bg='#16213e', height=40)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="⚪ Waiting for champion selection...",
            font=('Segoe UI', 10),
            fg='#e0e0e0',
            bg='#16213e'
        )
        self.status_label.pack(pady=10)

        # Scrollable content area
        canvas = tk.Canvas(self.root, bg='#0a0e27', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#0a0e27')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Champion info
        self.champion_label = tk.Label(
            self.scrollable_frame,
            text="Select a champion in League client",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg='#0a0e27'
        )
        self.champion_label.pack(pady=15)

        # Runes container
        self.runes_container = tk.Frame(self.scrollable_frame, bg='#0a0e27')
        self.runes_container.pack(fill='x', padx=20, pady=10)

        # Items container
        self.items_container = tk.Frame(self.scrollable_frame, bg='#0a0e27')
        self.items_container.pack(fill='x', padx=20, pady=10)

        # Apply button
        button_frame = tk.Frame(self.root, bg='#0a0e27')
        button_frame.pack(fill='x', padx=20, pady=15)

        self.apply_button = tk.Button(
            button_frame,
            text="Apply Runes & Items",
            font=('Segoe UI', 14, 'bold'),
            bg='#4ecca3',
            fg='white',
            command=self._on_apply_clicked,
            state='disabled',
            height=2,
            relief='flat',
            cursor='hand2'
        )
        self.apply_button.pack(fill='x')

    def update_status(self, message: str, color: str = 'white'):
        """Update status bar message"""
        icon = "🟢" if "connected" in message.lower() or "applied" in message.lower() else "⚪"
        if "failed" in message.lower() or "error" in message.lower():
            icon = "🔴"

        self.status_label.config(text=f"{icon} {message}", fg=color)

    def display_build(self, champion_name: str, role: str, build_data: BuildData):
        """Display runes and items with icons"""
        self.current_build = build_data
        self.image_refs.clear()

        # Update champion info
        self.champion_label.config(text=f"{champion_name} - {role.upper()}")

        # Clear previous content
        for widget in self.runes_container.winfo_children():
            widget.destroy()
        for widget in self.items_container.winfo_children():
            widget.destroy()

        # Display runes
        self._display_runes(build_data.runes)

        # Display items
        self._display_items(build_data.items)

        # Display summoner spells
        if build_data.summoner_spells:
            self._display_summoner_spells(build_data.summoner_spells)

        # Enable apply button
        self.apply_button.config(state='normal', bg='#4ecca3')

    def _display_runes(self, runes):
        """Display runes visually with icons"""
        primary_tree, primary_color = RUNE_TREES.get(runes.primary_style, ("Unknown", "#888888"))
        sub_tree, sub_color = RUNE_TREES.get(runes.sub_style, ("Unknown", "#888888"))

        # Primary tree header
        primary_header = tk.Frame(self.runes_container, bg='#0a0e27')
        primary_header.pack(fill='x', pady=(0, 10))

        tk.Label(
            primary_header,
            text=f"PRIMARY: {primary_tree}",
            font=('Segoe UI', 12, 'bold'),
            fg=primary_color,
            bg='#0a0e27'
        ).pack(anchor='w')

        # Primary runes grid
        primary_frame = tk.Frame(self.runes_container, bg='#16213e', relief='solid', bd=1)
        primary_frame.pack(fill='x', pady=5)

        # Keystone (larger)
        keystone_frame = tk.Frame(primary_frame, bg='#16213e')
        keystone_frame.pack(pady=10)

        self._create_rune_icon(keystone_frame, runes.selected_perks[0], size=(64, 64), is_keystone=True)

        # Primary perks (3 runes)
        perks_frame = tk.Frame(primary_frame, bg='#16213e')
        perks_frame.pack(pady=10)

        for i in range(1, 4):
            self._create_rune_icon(perks_frame, runes.selected_perks[i], size=(48, 48))

        # Secondary tree header
        secondary_header = tk.Frame(self.runes_container, bg='#0a0e27')
        secondary_header.pack(fill='x', pady=(15, 10))

        tk.Label(
            secondary_header,
            text=f"SECONDARY: {sub_tree}",
            font=('Segoe UI', 12, 'bold'),
            fg=sub_color,
            bg='#0a0e27'
        ).pack(anchor='w')

        # Secondary runes grid
        secondary_frame = tk.Frame(self.runes_container, bg='#16213e', relief='solid', bd=1)
        secondary_frame.pack(fill='x', pady=5)

        sec_perks_frame = tk.Frame(secondary_frame, bg='#16213e')
        sec_perks_frame.pack(pady=10)

        for i in range(4, 6):
            self._create_rune_icon(sec_perks_frame, runes.selected_perks[i], size=(48, 48))

        # Stat shards header
        shards_header = tk.Frame(self.runes_container, bg='#0a0e27')
        shards_header.pack(fill='x', pady=(15, 10))

        tk.Label(
            shards_header,
            text="STAT SHARDS",
            font=('Segoe UI', 12, 'bold'),
            fg='#C8AA6E',
            bg='#0a0e27'
        ).pack(anchor='w')

        # Stat shards
        shards_frame = tk.Frame(self.runes_container, bg='#16213e', relief='solid', bd=1)
        shards_frame.pack(fill='x', pady=5)

        shards_row = tk.Frame(shards_frame, bg='#16213e')
        shards_row.pack(pady=10)

        for i in range(6, 9):
            if i < len(runes.selected_perks):
                self._create_stat_shard(shards_row, runes.selected_perks[i])

    def _create_rune_icon(self, parent, perk_id: int, size: tuple = (48, 48), is_keystone: bool = False):
        """Create a rune icon"""
        frame = tk.Frame(parent, bg='#16213e')
        frame.pack(side='left', padx=5)

        # Try to load rune icon from CDN
        # Note: This is a simplified approach - real implementation would need proper rune ID to icon mapping
        placeholder = tk.Label(
            frame,
            text=str(perk_id),
            font=('Segoe UI', 8 if not is_keystone else 10),
            fg='white',
            bg='#2a2a4e',
            width=size[0]//8,
            height=size[1]//16,
            relief='solid',
            bd=1
        )
        placeholder.pack()

    def _create_stat_shard(self, parent, shard_id: int):
        """Create a stat shard icon"""
        shard_names = {
            5008: "AF", 5005: "AS", 5007: "AH",
            5002: "ARM", 5003: "MR", 5001: "HP"
        }

        frame = tk.Frame(parent, bg='#16213e')
        frame.pack(side='left', padx=5)

        label = tk.Label(
            frame,
            text=shard_names.get(shard_id, str(shard_id)),
            font=('Segoe UI', 10, 'bold'),
            fg='#C8AA6E',
            bg='#2a2a4e',
            width=4,
            height=2,
            relief='solid',
            bd=1
        )
        label.pack()

    def _display_items(self, items):
        """Display items visually with icons"""
        # Items header
        items_header = tk.Frame(self.items_container, bg='#0a0e27')
        items_header.pack(fill='x', pady=(15, 10))

        tk.Label(
            items_header,
            text="RECOMMENDED ITEMS",
            font=('Segoe UI', 12, 'bold'),
            fg='#4ecca3',
            bg='#0a0e27'
        ).pack(anchor='w')

        items_frame = tk.Frame(self.items_container, bg='#16213e', relief='solid', bd=1)
        items_frame.pack(fill='x', pady=5, padx=0)

        # Starting items
        self._create_item_row(items_frame, "Starting", items.starting_items)

        # Core items
        self._create_item_row(items_frame, "Core Build", items.core_items)

        # Situational items
        self._create_item_row(items_frame, "Situational", items.situational_items)

    def _create_item_row(self, parent, label: str, item_ids: list):
        """Create a row of item icons"""
        row_frame = tk.Frame(parent, bg='#16213e')
        row_frame.pack(fill='x', pady=8, padx=10)

        tk.Label(
            row_frame,
            text=label + ":",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#16213e',
            width=12,
            anchor='w'
        ).pack(side='left', padx=(0, 10))

        icons_frame = tk.Frame(row_frame, bg='#16213e')
        icons_frame.pack(side='left')

        for item_id in item_ids:
            self._create_item_icon(icons_frame, item_id)

    def _create_item_icon(self, parent, item_id: int):
        """Create an item icon"""
        # Try to fetch real item icon from CDN
        url = f"{ITEM_CDN}{item_id}.png"
        img = fetch_image(url, size=(40, 40))

        if img:
            self.image_refs.append(img)
            label = tk.Label(parent, image=img, bg='#16213e', bd=1, relief='solid')
        else:
            # Fallback to item ID
            label = tk.Label(
                parent,
                text=str(item_id),
                font=('Segoe UI', 8),
                fg='white',
                bg='#2a2a4e',
                width=5,
                height=2,
                relief='solid',
                bd=1
            )

        label.pack(side='left', padx=2)

    def _display_summoner_spells(self, spell_ids: list):
        """Display summoner spells"""
        spells_header = tk.Frame(self.items_container, bg='#0a0e27')
        spells_header.pack(fill='x', pady=(15, 10))

        tk.Label(
            spells_header,
            text="SUMMONER SPELLS",
            font=('Segoe UI', 12, 'bold'),
            fg='#5E9BE0',
            bg='#0a0e27'
        ).pack(anchor='w')

        spells_frame = tk.Frame(self.items_container, bg='#16213e', relief='solid', bd=1)
        spells_frame.pack(fill='x', pady=5)

        row = tk.Frame(spells_frame, bg='#16213e')
        row.pack(pady=10)

        for spell_id in spell_ids:
            spell_name = SUMMONER_SPELLS.get(spell_id, f"Spell{spell_id}")

            frame = tk.Frame(row, bg='#16213e')
            frame.pack(side='left', padx=10)

            label = tk.Label(
                frame,
                text=spell_name,
                font=('Segoe UI', 10, 'bold'),
                fg='white',
                bg='#2a2a4e',
                width=10,
                height=2,
                relief='solid',
                bd=1
            )
            label.pack()

    def _on_apply_clicked(self):
        """Handle apply button click"""
        if self.on_apply and self.current_build:
            self.on_apply(self.current_build)
            self.update_status("Applying runes to League client...", '#4ecca3')

    def run(self):
        """Run the GUI (blocks until window closes)"""
        self.root.mainloop()

    def destroy(self):
        """Close the window"""
        self.root.destroy()
