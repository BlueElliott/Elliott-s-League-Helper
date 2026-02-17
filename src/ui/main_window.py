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


# Rune tree names, colors, and icons
RUNE_TREES = {
    8000: ("Precision",   "#C8AA6E", "perk-images/Styles/7201_Precision.png"),
    8100: ("Domination",  "#DC354A", "perk-images/Styles/7200_Domination.png"),
    8200: ("Sorcery",     "#5E9BE0", "perk-images/Styles/7202_Sorcery.png"),
    8300: ("Inspiration", "#49AAB9", "perk-images/Styles/7203_Whimsy.png"),
    8400: ("Resolve",     "#00A550", "perk-images/Styles/7204_Resolve.png"),
}

# Complete rune ID -> (name, icon_path) mapping from Data Dragon 16.3.1
RUNE_DATA = {
    # Domination
    8112: ("Electrocute",       "perk-images/Styles/Domination/Electrocute/Electrocute.png"),
    8128: ("Dark Harvest",      "perk-images/Styles/Domination/DarkHarvest/DarkHarvest.png"),
    9923: ("Hail of Blades",    "perk-images/Styles/Domination/HailOfBlades/HailOfBlades.png"),
    8126: ("Cheap Shot",        "perk-images/Styles/Domination/CheapShot/CheapShot.png"),
    8139: ("Taste of Blood",    "perk-images/Styles/Domination/TasteOfBlood/GreenTerror_TasteOfBlood.png"),
    8143: ("Sudden Impact",     "perk-images/Styles/Domination/SuddenImpact/SuddenImpact.png"),
    8137: ("Sixth Sense",       "perk-images/Styles/Domination/SixthSense/SixthSense.png"),
    8140: ("Grisly Mementos",   "perk-images/Styles/Domination/GrislyMementos/GrislyMementos.png"),
    8141: ("Deep Ward",         "perk-images/Styles/Domination/DeepWard/DeepWard.png"),
    8135: ("Treasure Hunter",   "perk-images/Styles/Domination/TreasureHunter/TreasureHunter.png"),
    8105: ("Relentless Hunter", "perk-images/Styles/Domination/RelentlessHunter/RelentlessHunter.png"),
    8106: ("Ultimate Hunter",   "perk-images/Styles/Domination/UltimateHunter/UltimateHunter.png"),
    # Inspiration
    8351: ("Glacial Augment",   "perk-images/Styles/Inspiration/GlacialAugment/GlacialAugment.png"),
    8360: ("Unsealed Spellbook","perk-images/Styles/Inspiration/UnsealedSpellbook/UnsealedSpellbook.png"),
    8369: ("First Strike",      "perk-images/Styles/Inspiration/FirstStrike/FirstStrike.png"),
    8306: ("Hextech Flash",     "perk-images/Styles/Inspiration/HextechFlashtraption/HextechFlashtraption.png"),
    8304: ("Magical Footwear",  "perk-images/Styles/Inspiration/MagicalFootwear/MagicalFootwear.png"),
    8321: ("Cash Back",         "perk-images/Styles/Inspiration/CashBack/CashBack2.png"),
    8313: ("Triple Tonic",      "perk-images/Styles/Inspiration/PerfectTiming/AlchemistCabinet.png"),
    8352: ("Time Warp Tonic",   "perk-images/Styles/Inspiration/TimeWarpTonic/TimeWarpTonic.png"),
    8345: ("Biscuit Delivery",  "perk-images/Styles/Inspiration/BiscuitDelivery/BiscuitDelivery.png"),
    8347: ("Cosmic Insight",    "perk-images/Styles/Inspiration/CosmicInsight/CosmicInsight.png"),
    8410: ("Approach Velocity", "perk-images/Styles/Resolve/ApproachVelocity/ApproachVelocity.png"),
    8316: ("Jack of All Trades","perk-images/Styles/Inspiration/JackOfAllTrades/JackofAllTrades2.png"),
    # Precision
    8005: ("Press the Attack",  "perk-images/Styles/Precision/PressTheAttack/PressTheAttack.png"),
    8008: ("Lethal Tempo",      "perk-images/Styles/Precision/LethalTempo/LethalTempoTemp.png"),
    8021: ("Fleet Footwork",    "perk-images/Styles/Precision/FleetFootwork/FleetFootwork.png"),
    8010: ("Conqueror",         "perk-images/Styles/Precision/Conqueror/Conqueror.png"),
    9101: ("Absorb Life",       "perk-images/Styles/Precision/AbsorbLife/AbsorbLife.png"),
    9111: ("Triumph",           "perk-images/Styles/Precision/Triumph.png"),
    8009: ("Presence of Mind",  "perk-images/Styles/Precision/PresenceOfMind/PresenceOfMind.png"),
    9104: ("Legend: Alacrity",  "perk-images/Styles/Precision/LegendAlacrity/LegendAlacrity.png"),
    9105: ("Legend: Haste",     "perk-images/Styles/Precision/LegendHaste/LegendHaste.png"),
    9103: ("Legend: Bloodline", "perk-images/Styles/Precision/LegendBloodline/LegendBloodline.png"),
    8014: ("Coup de Grace",     "perk-images/Styles/Precision/CoupDeGrace/CoupDeGrace.png"),
    8017: ("Cut Down",          "perk-images/Styles/Precision/CutDown/CutDown.png"),
    8299: ("Last Stand",        "perk-images/Styles/Sorcery/LastStand/LastStand.png"),
    # Resolve
    8437: ("Grasp of the Undying","perk-images/Styles/Resolve/GraspOfTheUndying/GraspOfTheUndying.png"),
    8439: ("Aftershock",        "perk-images/Styles/Resolve/VeteranAftershock/VeteranAftershock.png"),
    8465: ("Guardian",          "perk-images/Styles/Resolve/Guardian/Guardian.png"),
    8446: ("Demolish",          "perk-images/Styles/Resolve/Demolish/Demolish.png"),
    8463: ("Font of Life",      "perk-images/Styles/Resolve/FontOfLife/FontOfLife.png"),
    8401: ("Shield Bash",       "perk-images/Styles/Resolve/MirrorShell/MirrorShell.png"),
    8429: ("Conditioning",      "perk-images/Styles/Resolve/Conditioning/Conditioning.png"),
    8444: ("Second Wind",       "perk-images/Styles/Resolve/SecondWind/SecondWind.png"),
    8473: ("Bone Plating",      "perk-images/Styles/Resolve/BonePlating/BonePlating.png"),
    8451: ("Overgrowth",        "perk-images/Styles/Resolve/Overgrowth/Overgrowth.png"),
    8453: ("Revitalize",        "perk-images/Styles/Resolve/Revitalize/Revitalize.png"),
    8242: ("Unflinching",       "perk-images/Styles/Sorcery/Unflinching/Unflinching.png"),
    # Sorcery
    8214: ("Summon Aery",       "perk-images/Styles/Sorcery/SummonAery/SummonAery.png"),
    8229: ("Arcane Comet",      "perk-images/Styles/Sorcery/ArcaneComet/ArcaneComet.png"),
    8230: ("Phase Rush",        "perk-images/Styles/Sorcery/PhaseRush/PhaseRush.png"),
    8224: ("Axiom Arcanist",    "perk-images/Styles/Sorcery/NullifyingOrb/Axiom_Arcanist.png"),
    8226: ("Manaflow Band",     "perk-images/Styles/Sorcery/ManaflowBand/ManaflowBand.png"),
    8275: ("Nimbus Cloak",      "perk-images/Styles/Sorcery/NimbusCloak/6361.png"),
    8210: ("Transcendence",     "perk-images/Styles/Sorcery/Transcendence/Transcendence.png"),
    8234: ("Celerity",          "perk-images/Styles/Sorcery/Celerity/CelerityTemp.png"),
    8233: ("Absolute Focus",    "perk-images/Styles/Sorcery/AbsoluteFocus/AbsoluteFocus.png"),
    8237: ("Scorch",            "perk-images/Styles/Sorcery/Scorch/Scorch.png"),
    8232: ("Waterwalking",      "perk-images/Styles/Sorcery/Waterwalking/Waterwalking.png"),
    8236: ("Gathering Storm",   "perk-images/Styles/Sorcery/GatheringStorm/GatheringStorm.png"),
    # Stat shards
    5008: ("Adaptive Force",    "perk-images/StatMods/StatModsAdaptiveForceIcon.png"),
    5005: ("Attack Speed",      "perk-images/StatMods/StatModsAttackSpeedIcon.png"),
    5007: ("Ability Haste",     "perk-images/StatMods/StatModsCDRScalingIcon.png"),
    5002: ("Armor",             "perk-images/StatMods/StatModsArmorIcon.png"),
    5003: ("Magic Resist",      "perk-images/StatMods/StatModsMagicResIcon.MagicResist.png"),
    5001: ("Health",            "perk-images/StatMods/StatModsHealthScalingIcon.png"),
}

# Summoner spell names and icons
SUMMONER_SPELLS = {
    1:  ("Cleanse",   "SummonerBoost.png"),
    3:  ("Exhaust",   "SummonerExhaust.png"),
    4:  ("Flash",     "SummonerFlash.png"),
    6:  ("Ghost",     "SummonerHaste.png"),
    7:  ("Heal",      "SummonerHeal.png"),
    11: ("Smite",     "SummonerSmite.png"),
    12: ("Teleport",  "SummonerTeleport.png"),
    13: ("Clarity",   "SummonerMana.png"),
    14: ("Ignite",    "SummonerDot.png"),
    21: ("Barrier",   "SummonerBarrier.png"),
}

# CDN base URLs
DDRAGON_VERSION = "16.3.1"
DDRAGON_IMG = "https://ddragon.leagueoflegends.com/cdn/img/"
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
        primary_info = RUNE_TREES.get(runes.primary_style, ("Unknown", "#888888", ""))
        sub_info = RUNE_TREES.get(runes.sub_style, ("Unknown", "#888888", ""))
        primary_tree, primary_color, primary_icon = primary_info
        sub_tree, sub_color, sub_icon = sub_info

        # Primary tree header with icon
        self._make_section_header(self.runes_container, f"PRIMARY  {primary_tree}", primary_color, primary_icon)

        primary_frame = tk.Frame(self.runes_container, bg='#16213e', relief='solid', bd=1)
        primary_frame.pack(fill='x', pady=5)

        # Keystone row
        keystone_row = tk.Frame(primary_frame, bg='#16213e')
        keystone_row.pack(pady=12)
        self._create_rune_icon(keystone_row, runes.selected_perks[0], size=(64, 64), is_keystone=True)

        # Primary rows 2-4
        perks_row = tk.Frame(primary_frame, bg='#16213e')
        perks_row.pack(pady=10)
        for i in range(1, 4):
            self._create_rune_icon(perks_row, runes.selected_perks[i], size=(44, 44))

        # Secondary tree header with icon
        self._make_section_header(self.runes_container, f"SECONDARY  {sub_tree}", sub_color, sub_icon, top_pad=15)

        secondary_frame = tk.Frame(self.runes_container, bg='#16213e', relief='solid', bd=1)
        secondary_frame.pack(fill='x', pady=5)

        sec_row = tk.Frame(secondary_frame, bg='#16213e')
        sec_row.pack(pady=10)
        for i in range(4, 6):
            self._create_rune_icon(sec_row, runes.selected_perks[i], size=(44, 44))

        # Stat shards header
        self._make_section_header(self.runes_container, "STAT SHARDS", "#C8AA6E", top_pad=15)

        shards_frame = tk.Frame(self.runes_container, bg='#16213e', relief='solid', bd=1)
        shards_frame.pack(fill='x', pady=5)

        shards_row = tk.Frame(shards_frame, bg='#16213e')
        shards_row.pack(pady=10)
        for i in range(6, 9):
            if i < len(runes.selected_perks):
                self._create_rune_icon(shards_row, runes.selected_perks[i], size=(36, 36), is_shard=True)

    def _make_section_header(self, parent, text: str, color: str, icon_path: str = "", top_pad: int = 0):
        """Create a section header with optional icon"""
        header = tk.Frame(parent, bg='#0a0e27')
        header.pack(fill='x', pady=(top_pad, 6))

        if icon_path:
            url = DDRAGON_IMG + icon_path
            img = fetch_image(url, size=(24, 24))
            if img:
                self.image_refs.append(img)
                tk.Label(header, image=img, bg='#0a0e27').pack(side='left', padx=(0, 6))

        tk.Label(
            header,
            text=text,
            font=('Segoe UI', 11, 'bold'),
            fg=color,
            bg='#0a0e27'
        ).pack(side='left', anchor='w')

    def _create_rune_icon(self, parent, perk_id: int, size: tuple = (44, 44),
                          is_keystone: bool = False, is_shard: bool = False):
        """Create a rune icon fetched from Data Dragon"""
        bg = '#16213e'
        frame = tk.Frame(parent, bg=bg)
        frame.pack(side='left', padx=8 if is_keystone else 5)

        rune_name, icon_path = RUNE_DATA.get(perk_id, (str(perk_id), ""))

        if icon_path:
            url = DDRAGON_IMG + icon_path
            img = fetch_image(url, size=size)
            if img:
                self.image_refs.append(img)
                border_color = '#FFD700' if is_keystone else ('#C8AA6E' if is_shard else '#555577')
                lbl = tk.Label(frame, image=img, bg=bg, bd=2, relief='solid',
                               highlightbackground=border_color, highlightthickness=1)
                lbl.pack()
                tk.Label(frame, text=rune_name, font=('Segoe UI', 7),
                         fg='#aaaacc', bg=bg, wraplength=size[0]+10).pack()
                return

        # Fallback text label
        tk.Label(
            frame,
            text=rune_name,
            font=('Segoe UI', 8, 'bold' if is_keystone else 'normal'),
            fg='#FFD700' if is_keystone else '#aaaacc',
            bg='#2a2a4e',
            width=size[0] // 8,
            height=size[1] // 16,
            relief='solid', bd=1, wraplength=60
        ).pack()

    def _display_items(self, items):
        """Display items visually with icons"""
        self._make_section_header(self.items_container, "RECOMMENDED ITEMS", "#4ecca3", top_pad=15)

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
        """Display summoner spells with icons"""
        self._make_section_header(self.items_container, "SUMMONER SPELLS", "#5E9BE0", top_pad=15)

        spells_frame = tk.Frame(self.items_container, bg='#16213e', relief='solid', bd=1)
        spells_frame.pack(fill='x', pady=5)

        row = tk.Frame(spells_frame, bg='#16213e')
        row.pack(pady=10)

        for spell_id in spell_ids:
            spell_name, spell_file = SUMMONER_SPELLS.get(spell_id, (f"Spell{spell_id}", ""))
            frame = tk.Frame(row, bg='#16213e')
            frame.pack(side='left', padx=12)

            if spell_file:
                url = SPELL_CDN + spell_file
                img = fetch_image(url, size=(44, 44))
                if img:
                    self.image_refs.append(img)
                    tk.Label(frame, image=img, bg='#16213e', bd=2, relief='solid').pack()
                    tk.Label(frame, text=spell_name, font=('Segoe UI', 8),
                             fg='#aaaacc', bg='#16213e').pack()
                    continue

            tk.Label(
                frame, text=spell_name,
                font=('Segoe UI', 10, 'bold'), fg='white',
                bg='#2a2a4e', width=10, height=2, relief='solid', bd=1
            ).pack()

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
