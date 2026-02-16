"""
Main GUI Window
Visual interface for viewing and applying runes
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Optional, Callable
from providers.base import BuildData


# Rune tree names
RUNE_TREES = {
    8000: "Precision",
    8100: "Domination",
    8200: "Sorcery",
    8300: "Inspiration",
    8400: "Resolve"
}

# Rune names (partial list - will expand)
RUNE_NAMES = {
    # Precision
    8005: "Press the Attack", 8008: "Lethal Tempo", 8021: "Fleet Footwork", 8010: "Conqueror",
    8009: "Presence of Mind", 9101: "Overheal", 8014: "Coup de Grace",

    # Domination
    8112: "Electrocute", 8124: "Predator", 8128: "Dark Harvest", 9923: "Hail of Blades",
    8143: "Sudden Impact", 8136: "Zombie Ward", 8120: "Ghost Poro", 8138: "Eyeball Collection",
    8135: "Treasure Hunter", 8134: "Ingenious Hunter", 8105: "Relentless Hunter", 8106: "Ultimate Hunter",

    # Sorcery
    8214: "Summon Aery", 8229: "Arcane Comet", 8230: "Phase Rush",
    8224: "Nullifying Orb", 8226: "Manaflow Band", 8275: "Nimbus Cloak",
    8210: "Transcendence", 8234: "Celerity", 8233: "Absolute Focus",
    8237: "Scorch", 8232: "Waterwalking", 8236: "Gathering Storm",

    # Resolve
    8437: "Grasp of the Undying", 8439: "Aftershock", 8465: "Guardian",
    8446: "Demolish", 8463: "Font of Life", 8401: "Shield Bash",
    8429: "Conditioning", 8444: "Second Wind", 8473: "Bone Plating",
    8451: "Overgrowth", 8453: "Revitalize", 8242: "Unflinching",

    # Inspiration
    8351: "Glacial Augment", 8360: "Unsealed Spellbook", 8369: "First Strike",
    8306: "Hexflash", 8304: "Magical Footwear", 8313: "Perfect Timing",
    8321: "Futures Market", 8316: "Minion Dematerializer", 8345: "Biscuit Delivery",
    8347: "Cosmic Insight", 8410: "Approach Velocity", 8352: "Time Warp Tonic",

    # Stat shards
    5008: "Adaptive Force", 5005: "Attack Speed", 5007: "Ability Haste",
    5002: "Armor", 5003: "Magic Resist", 5001: "Health"
}


class RuneDisplayWindow:
    """Main GUI window for displaying runes"""

    def __init__(self, on_apply: Optional[Callable] = None):
        """
        Initialize GUI window

        Args:
            on_apply: Callback when user clicks "Apply Runes"
        """
        self.on_apply = on_apply
        self.current_build: Optional[BuildData] = None

        # Create main window
        self.root = tk.Tk()
        self.root.title("Elliott's League Helper")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        # Set icon color (would use actual icon in production)
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass  # Icon file not found, skip

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
            font=('Arial', 18, 'bold'),
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
            font=('Arial', 10),
            fg='#e0e0e0',
            bg='#16213e'
        )
        self.status_label.pack(pady=10)

        # Main content area
        content_frame = tk.Frame(self.root, bg='#0f3460')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Champion info
        self.champion_frame = tk.LabelFrame(
            content_frame,
            text="Champion Build",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#0f3460'
        )
        self.champion_frame.pack(fill='x', pady=(0, 10))

        self.champion_label = tk.Label(
            self.champion_frame,
            text="No champion selected",
            font=('Arial', 14),
            fg='white',
            bg='#0f3460'
        )
        self.champion_label.pack(pady=10)

        # Runes display
        runes_frame = tk.LabelFrame(
            content_frame,
            text="Runes",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#0f3460'
        )
        runes_frame.pack(fill='both', expand=True)

        # Runes text area
        self.runes_text = scrolledtext.ScrolledText(
            runes_frame,
            font=('Courier', 10),
            bg='#1a1a2e',
            fg='white',
            height=20,
            wrap='word'
        )
        self.runes_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#0f3460')
        button_frame.pack(fill='x', padx=10, pady=10)

        self.apply_button = tk.Button(
            button_frame,
            text="Apply Runes",
            font=('Arial', 12, 'bold'),
            bg='#4ecca3',
            fg='white',
            command=self._on_apply_clicked,
            state='disabled',
            height=2
        )
        self.apply_button.pack(fill='x')

    def update_status(self, message: str, color: str = 'white'):
        """Update status bar message"""
        icon = "🟢" if "connected" in message.lower() or "applied" in message.lower() else "⚪"
        if "failed" in message.lower() or "error" in message.lower():
            icon = "🔴"

        self.status_label.config(text=f"{icon} {message}", fg=color)

    def display_build(self, champion_name: str, role: str, build_data: BuildData):
        """Display runes and items for a champion"""
        self.current_build = build_data

        # Update champion info
        self.champion_label.config(text=f"{champion_name} - {role.upper()}")

        # Build rune display text
        runes = build_data.runes
        primary_tree = RUNE_TREES.get(runes.primary_style, f"Tree {runes.primary_style}")
        sub_tree = RUNE_TREES.get(runes.sub_style, f"Tree {runes.sub_style}")

        text = f"PRIMARY: {primary_tree}\n"
        text += "=" * 50 + "\n\n"

        # Display perks
        for i, perk_id in enumerate(runes.selected_perks[:6]):  # First 6 are tree perks
            perk_name = RUNE_NAMES.get(perk_id, f"Rune {perk_id}")
            if i == 0:
                text += f"🔶 KEYSTONE: {perk_name}\n\n"
            elif i == 4:
                text += f"\nSECONDARY: {sub_tree}\n"
                text += "=" * 50 + "\n\n"
                text += f"  • {perk_name}\n"
            else:
                text += f"  • {perk_name}\n"

        text += "\nSTAT SHARDS\n"
        text += "=" * 50 + "\n\n"

        # Stat shards (last 3 perks)
        for perk_id in runes.selected_perks[6:]:
            perk_name = RUNE_NAMES.get(perk_id, f"Shard {perk_id}")
            text += f"  ⬥ {perk_name}\n"

        # Display items
        text += "\n\nITEMS\n"
        text += "=" * 50 + "\n\n"
        text += f"Starting: {build_data.items.starting_items}\n"
        text += f"Core: {build_data.items.core_items}\n"
        text += f"Situational: {build_data.items.situational_items}\n"

        # Summoner spells
        if build_data.summoner_spells:
            text += "\n\nSUMMONER SPELLS\n"
            text += "=" * 50 + "\n\n"
            text += f"Spells: {build_data.summoner_spells}\n"

        # Update text area
        self.runes_text.delete('1.0', 'end')
        self.runes_text.insert('1.0', text)

        # Enable apply button
        self.apply_button.config(state='normal', bg='#4ecca3')

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
