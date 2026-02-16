"""
Champion-Specific Build Data
Fallback builds for popular champions with valid rune IDs
"""

from providers.base import RuneData, ItemBuild, BuildData


# Champion-specific rune builds (using valid Season 2026 IDs)
CHAMPION_BUILDS = {
    # Mages
    103: {  # Ahri
        'runes': RuneData(
            primary_style=8200,  # Sorcery
            sub_style=8100,      # Domination
            selected_perks=[
                8214,  # Summon Aery
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
        'summoner_spells': [4, 14]  # Flash + Ignite
    },

    # Tanks
    154: {  # Zac
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8300,      # Inspiration
            selected_perks=[
                8439,  # Aftershock
                8446,  # Demolish
                8473,  # Bone Plating
                8451,  # Overgrowth
                8347,  # Cosmic Insight
                8410,  # Approach Velocity
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 11]  # Flash + Smite
    },

    # Fighters
    266: {  # Aatrox
        'runes': RuneData(
            primary_style=8000,  # Precision
            sub_style=8400,      # Resolve
            selected_perks=[
                8010,  # Conqueror
                9101,  # Overheal
                9104,  # Legend: Alacrity
                8299,  # Last Stand
                8473,  # Bone Plating
                8451,  # Overgrowth
                5005,  # Attack Speed
                5008,  # Adaptive Force
                5002   # Armor
            ]
        ),
        'summoner_spells': [4, 12]  # Flash + Teleport
    },

    # Supports
    16: {  # Poppy
        'runes': RuneData(
            primary_style=8400,  # Resolve
            sub_style=8300,      # Inspiration
            selected_perks=[
                8437,  # Grasp of the Undying
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
