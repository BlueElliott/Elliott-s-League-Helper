"""
Test script to verify the provider works without League client
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from providers.ugg_scraper import UGGScraperProvider


async def test_provider():
    """Test the U.GG scraper provider"""
    provider = UGGScraperProvider()

    # Test with Sejuani (ID 113)
    print("Testing with Sejuani (ID 113) - Jungle")
    print("=" * 50)

    build_data = await provider.get_build(
        champion_id=113,
        role="jungle",
        patch="14_1"
    )

    if build_data:
        print("\n[SUCCESS] Build data retrieved!")
        print("\nRunes:")
        print(f"  Primary Tree: {build_data.runes.primary_style}")
        print(f"  Sub Tree: {build_data.runes.sub_style}")
        print(f"  Perks: {build_data.runes.selected_perks}")

        print("\nItems:")
        print(f"  Starting: {build_data.items.starting_items}")
        print(f"  Core: {build_data.items.core_items}")
        print(f"  Situational: {build_data.items.situational_items}")

        if build_data.summoner_spells:
            print(f"\nSummoner Spells: {build_data.summoner_spells}")

        return True
    else:
        print("\n[FAILED] Could not retrieve build data")
        return False


if __name__ == "__main__":
    print("Elliott's League Helper - Provider Test")
    print()

    success = asyncio.run(test_provider())

    if success:
        print("\n" + "=" * 50)
        print("Provider test PASSED!")
        print("The app should work when connected to League client.")
    else:
        print("\n" + "=" * 50)
        print("Provider test FAILED!")
        print("Check the error messages above.")
