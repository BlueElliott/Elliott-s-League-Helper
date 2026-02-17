"""
Champion-Specific Build Data
Fallback builds for popular champions with valid rune IDs
"""

from providers.base import RuneData, ItemBuild, BuildData


# Champion-specific rune builds (using valid Season 2026 IDs)
CHAMPION_BUILDS = {
    # === MAGES ===
    103: {  # Ahri
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8200,      # Sorcery
            selected_perks=[
                8112,  # Electrocute
                8143,  # Sudden Impact
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                8226,  # Manaflow Band
                8237,  # Scorch
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]  # Flash + Ignite
    },

    34: {  # Anivia
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8214,  # Summon Aery
                8226,  # Manaflow Band
                8210,  # Transcendence
                8236,  # Gathering Storm
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]  # Flash + TP
    },

    99: {  # Lux
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8229,  # Arcane Comet
                8226,  # Manaflow Band
                8210,  # Transcendence
                8237,  # Scorch
                8304,  # Magical Footwear
                8345,  # Biscuit Delivery
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]  # Flash + Ignite
    },

    # === TANKS / JUNGLERS ===
    154: {  # Zac
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8300,      # Inspiration
            selected_perks=[
                8439,  # Aftershock
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                8304,  # Magical Footwear  (row 2)
                8347,  # Cosmic Insight    (row 4)
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]  # Flash + Smite
    },

    32: {  # Amumu
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8000,      # Precision
            selected_perks=[
                8439,  # Aftershock
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                8009,  # Presence of Mind
                8014,  # Coup de Grace
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]  # Flash + Smite
    },

    20: {  # Nunu
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8300,      # Inspiration
            selected_perks=[
                8439,  # Aftershock
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]  # Flash + Smite
    },

    # === FIGHTERS / TOP LANERS ===
    266: {  # Aatrox
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Overheal
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]  # Flash + Teleport
    },

    24: {  # Jax
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Overheal
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]  # Flash + Ignite
    },

    122: {  # Darius
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Overheal
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 6]  # Flash + Ghost
    },

    # === ASSASSINS ===
    238: {  # Zed
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8200,      # Sorcery
            selected_perks=[
                8112,  # Electrocute
                8143,  # Sudden Impact
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                8226,  # Manaflow Band
                8237,  # Scorch
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]  # Flash + Ignite
    },

    121: {  # Kha'Zix
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8200,      # Sorcery
            selected_perks=[
                8128,  # Dark Harvest
                8143,  # Sudden Impact
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                8226,  # Manaflow Band
                8236,  # Gathering Storm
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]  # Flash + Smite
    },

    84: {  # Akali
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8000,      # Precision
            selected_perks=[
                8112,  # Electrocute
                8143,  # Sudden Impact
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                8009,  # Presence of Mind
                8014,  # Coup de Grace
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]  # Flash + Ignite
    },

    # === MARKSMEN / ADC ===
    222: {  # Jinx
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Overheal
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]  # Flash + Heal
    },

    22: {  # Ashe
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8300,      # Inspiration
            selected_perks=[
                8005,  # Press the Attack
                9101,  # Overheal
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]  # Flash + Heal
    },

    51: {  # Caitlyn
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]  # Flash + Heal
    },

    166: {  # Akshan
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8005,  # Press the Attack
                9101,  # Overheal
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]  # Flash + Ignite
    },

    # === SUPPORTS ===
    412: {  # Thresh
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8300,      # Inspiration
            selected_perks=[
                8439,  # Aftershock
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]  # Flash + Ignite
    },

    117: {  # Lulu
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8214,  # Summon Aery
                8226,  # Manaflow Band
                8210,  # Transcendence
                8236,  # Gathering Storm
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 3]  # Flash + Exhaust
    },

    16: {  # Soraka
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8400,      # Resolve
            selected_perks=[
                8214,  # Summon Aery
                8226,  # Manaflow Band
                8210,  # Transcendence
                8236,  # Gathering Storm
                8473,  # Bone Plating
                8451,  # Overgrowth
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]  # Flash + Ignite
    },

    # === MORE MAGES / MID ===
    157: {  # Yasuo
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8008,  # Lethal Tempo
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    777: {  # Yone
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8008,  # Lethal Tempo
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    55: {  # Katarina
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8000,      # Precision
            selected_perks=[
                8112,  # Electrocute
                8139,  # Taste of Blood
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    112: {  # Viktor
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8229,  # Arcane Comet
                8226,  # Manaflow Band
                8210,  # Transcendence
                8236,  # Gathering Storm
                8304,  # Magical Footwear
                8345,  # Biscuit Delivery
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    61: {  # Orianna
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8229,  # Arcane Comet
                8226,  # Manaflow Band
                8210,  # Transcendence
                8236,  # Gathering Storm
                8304,  # Magical Footwear
                8345,  # Biscuit Delivery
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    142: {  # Zoe
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8229,  # Arcane Comet
                8226,  # Manaflow Band
                8233,  # Absolute Focus
                8237,  # Scorch
                8304,  # Magical Footwear
                8345,  # Biscuit Delivery
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    69: {  # Cassiopeia
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8000,      # Precision
            selected_perks=[
                8230,  # Phase Rush
                8226,  # Manaflow Band
                8210,  # Transcendence
                8237,  # Scorch
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    268: {  # Azir
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8229,  # Arcane Comet
                8226,  # Manaflow Band
                8210,  # Transcendence
                8236,  # Gathering Storm
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]
    },

    # === MORE TOP LANERS ===
    86: {  # Garen
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 6]  # Flash + Ghost
    },

    54: {  # Malphite
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8200,      # Sorcery
            selected_perks=[
                8439,  # Aftershock
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                8229,  # Arcane Comet
                8236,  # Gathering Storm
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]
    },

    114: {  # Fiora
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]
    },

    164: {  # Camille
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]
    },

    98: {  # Shen
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8000,      # Precision
            selected_perks=[
                8437,  # Grasp of the Undying
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]
    },

    39: {  # Irelia
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]
    },

    58: {  # Renekton
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]
    },

    17: {  # Teemo
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8100,      # Domination
            selected_perks=[
                8230,  # Phase Rush
                8226,  # Manaflow Band
                8234,  # Celerity
                8237,  # Scorch
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    # === MORE JUNGLERS ===
    64: {  # Lee Sin
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    104: {  # Graves
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    254: {  # Vi
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    245: {  # Ekko
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8000,      # Precision
            selected_perks=[
                8112,  # Electrocute
                8139,  # Taste of Blood
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    120: {  # Hecarim
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    28: {  # Evelynn
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8200,      # Sorcery
            selected_perks=[
                8128,  # Dark Harvest
                8143,  # Sudden Impact
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                8226,  # Manaflow Band
                8236,  # Gathering Storm
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    141: {  # Kayn
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    # === MORE ADCs ===
    81: {  # Ezreal
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8300,      # Inspiration
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]
    },

    21: {  # Miss Fortune
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8008,  # Lethal Tempo
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]
    },

    67: {  # Vayne
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]
    },

    202: {  # Jhin
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8200,      # Sorcery
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8017,  # Cut Down
                8233,  # Absolute Focus
                8237,  # Scorch
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]
    },

    # === MORE SUPPORTS ===
    40: {  # Janna
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8214,  # Summon Aery
                8226,  # Manaflow Band
                8210,  # Transcendence
                8236,  # Gathering Storm
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 3]  # Flash + Exhaust
    },

    89: {  # Leona
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8000,      # Precision
            selected_perks=[
                8439,  # Aftershock
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    53: {  # Blitzcrank
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8000,      # Precision
            selected_perks=[
                8439,  # Aftershock
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                9101,  # Absorb Life
                8014,  # Coup de Grace
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    25: {  # Morgana
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8229,  # Arcane Comet
                8226,  # Manaflow Band
                8210,  # Transcendence
                8237,  # Scorch
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    267: {  # Nami
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8214,  # Summon Aery
                8226,  # Manaflow Band
                8210,  # Transcendence
                8236,  # Gathering Storm
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 3]  # Flash + Exhaust
    },

    # === POPULAR MISSING CHAMPIONS ===
    234: {  # Viego
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]  # Flash + Smite
    },

    875: {  # Sett
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]  # Flash + Teleport
    },

    887: {  # Gwen
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]
    },

    517: {  # Sylas
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8200,      # Sorcery
            selected_perks=[
                8112,  # Electrocute
                8139,  # Taste of Blood
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                8226,  # Manaflow Band
                8237,  # Scorch
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    235: {  # Senna
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8446,  # Demolish
                8451,  # Overgrowth
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]  # Flash + Heal (ADC) or [4, 14] Support
    },

    236: {  # Lucian
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8005,  # Press the Attack
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]
    },

    145: {  # Kai'Sa
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]
    },

    498: {  # Xayah
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]
    },

    360: {  # Samira
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8005,  # Press the Attack
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    92: {  # Riven
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    711: {  # Vex
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8100,      # Domination
            selected_perks=[
                8229,  # Arcane Comet
                8226,  # Manaflow Band
                8210,  # Transcendence
                8237,  # Scorch
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 14]
    },

    523: {  # Aphelios
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8100,      # Domination
            selected_perks=[
                8021,  # Fleet Footwork
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8143,  # Sudden Impact
                8135,  # Treasure Hunter
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 7]
    },

    76: {  # Nidalee
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8200,      # Sorcery
            selected_perks=[
                8128,  # Dark Harvest
                8143,  # Sudden Impact
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                8226,  # Manaflow Band
                8236,  # Gathering Storm
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    107: {  # Rengar
        'runes': RuneData(
            primary_style=8100,  # Domination
            sub_style=8200,      # Sorcery
            selected_perks=[
                8128,  # Dark Harvest
                8143,  # Sudden Impact
                8140,  # Grisly Mementos
                8135,  # Treasure Hunter
                8226,  # Manaflow Band
                8236,  # Gathering Storm
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    876: {  # Lillia
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8300,      # Inspiration
            selected_perks=[
                8230,  # Phase Rush
                8226,  # Manaflow Band
                8210,  # Transcendence
                8236,  # Gathering Storm
                8304,  # Magical Footwear
                8347,  # Cosmic Insight
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]
    },

    516: {  # Ornn
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8000,      # Precision
            selected_perks=[
                8437,  # Grasp of the Undying
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                9101,  # Absorb Life
                9104,  # Legend: Alacrity
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]
    },
}


def get_champion_build(champion_id: int, role: str = 'middle') -> BuildData:
    """
    Get build data for a champion

    Args:
        champion_id: Champion ID
        role: Role (used for item recommendations)

    Returns:
        BuildData with champion-specific runes or generic fallback
    """
    if champion_id in CHAMPION_BUILDS:
        build = CHAMPION_BUILDS[champion_id]
        return BuildData(
            runes=build['runes'],
            items=_get_role_items(role),
            summoner_spells=build.get('summoner_spells', [4, 14])
        )
    else:
        # Generic fallback for unknown champions
        return _get_generic_build(role)


def _get_role_items(role: str) -> ItemBuild:
    """Get role-appropriate items"""
    role_items = {
        'top': ItemBuild(
            starting_items=[1054, 2003],  # Doran's Shield + Pot
            core_items=[3078, 3153, 3742],  # Trinity, BotRK, Hullbreaker
            situational_items=[3065, 3156, 3143]
        ),
        'jungle': ItemBuild(
            starting_items=[1039, 2003, 2003],  # Hailblade + Pots
            core_items=[6693, 3074, 3153],  # Jungle item, Hydra, BotRK
            situational_items=[3065, 3143, 6333]
        ),
        'middle': ItemBuild(
            starting_items=[1056, 2003, 2003],  # Doran's Ring + Pots
            core_items=[3020, 6653, 3135],  # Sorc Shoes, Luden's, Void
            situational_items=[3157, 3165, 3089]
        ),
        'bottom': ItemBuild(
            starting_items=[1055, 2003],  # Doran's Blade + Pot
            core_items=[3006, 6672, 3031],  # Zerker's, Kraken, IE
            situational_items=[3139, 3046, 3036]
        ),
        'support': ItemBuild(
            starting_items=[3854, 2003, 2003],  # Support item + Pots
            core_items=[3107, 3222, 3190],  # Redemption, Crucible, Locket
            situational_items=[3109, 3504, 3050]
        ),
    }

    return role_items.get(role, role_items['middle'])


def _get_generic_build(role: str) -> BuildData:
    """Generic build for unknown champions"""
    # Use Conqueror for generic build (works on most champs)
    return BuildData(
        runes=RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Overheal
                9104,  # Legend: Alacrity
                8014,  # Coup de Grace
                8473,  # Bone Plating
                8451,  # Overgrowth
                5008,  # Adaptive Force
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        items=_get_role_items(role),
        summoner_spells=[4, 14]
    )
