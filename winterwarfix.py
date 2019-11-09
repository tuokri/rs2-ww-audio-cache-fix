import ctypes.wintypes
import os
import shutil
import sys
from pathlib import Path

CACHE_DIR_PATTERN = r"{userpath}\My Games\Rising Storm 2\ROGame\Cache"
PUBLISHED_DIR_PATTERN = r"{userpath}\My Games\Rising Storm 2\ROGame\Published"
AUDIO_DIR = r"WwiseAudio"
WW_PACKAGE = "WinterWar.u"
YES = "yes"
NO = "no"
FIX_CACHE = 1
FIX_AUDIO = 2

CSIDL_PERSONAL = 5  # My Documents
SHGFP_TYPE_CURRENT = 0  # Get current, not default value.


def exit_prog():
    input("press any key to exit")
    sys.exit(0)


def main():
    print("****************************************************************************")
    print("PLEASE FULLY EXIT STEAM (RIGHT CLICK IN TASK BAR -> EXIT) BEFORE CONTINUING")
    print("PLEASE NOTE: AFTER FIXING CACHE YOU MIGHT BE REQUIRED TO RE-DOWNLOAD THE MOD")
    print("****************************************************************************")
    input("Press any key to continue once you have stopped Steam...")

    choice = None
    while True:
        print()
        print(f"IF YOU ARE EXPERIENCING DISCONNECTS AND WISH TO FIX CACHE, PRESS {FIX_CACHE} AND PRESS ENTER")
        print(f"IF YOU WISH TO FIX AUDIO FILES, PRESS {FIX_AUDIO} AND PRESS ENTER")
        try:
            choice = int(input("> ").strip())
        except Exception:
            continue
        if (choice == FIX_CACHE) or (choice == FIX_AUDIO):
            break

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    userpath = buf.value

    cache_dir = Path(CACHE_DIR_PATTERN.format(userpath=userpath))
    print(f"looking for Rising Storm 2 / Winter War cache in: {cache_dir}...")

    caches = [Path(c) for c in os.listdir(cache_dir)]
    if not caches:
        print("could not find Rising Storm 2 cache...")
        exit_prog()

    ww_package_paths = sorted(cache_dir.rglob(f"*/{WW_PACKAGE}"))
    if not ww_package_paths:
        print(f"could not find Winter War package ({WW_PACKAGE})")
        exit_prog()

    ww_caches = []
    for wwpp in ww_package_paths:
        print(f"found Winter War package in: {wwpp}")
        wwc = str(wwpp).rstrip(r"\Published\CookedPC\winterwar.u").split("\\")[:-1]
        ww_caches.append("\\".join(wwc))

    ww_cache = ww_caches[-1]
    print(f"full path to Winter War cache: {ww_cache}")

    published = Path(PUBLISHED_DIR_PATTERN.format(userpath=userpath))

    if choice == FIX_CACHE:
        for wwc in ww_caches:
            print(f"deleting {wwc}")
            shutil.rmtree(wwc, ignore_errors=True)
        if published.exists():
            print("****************************************************************************")
            print(f"WARNING! PUBLISHED DIRECTORY EXISTS: {published}")
            print("IF YOU ARE A MAPPER OR A MODDER, PLEASE BACKUP THIS DIRECTORY NOW!")
            print("IF YOU WISH TO CONTINUE, THE PUBLISHED DIRECTORY WILL BE DELETED!")
            print("****************************************************************************")
            while True:
                print("TYPE YES AND PRESS ENTER TO CONTINUE "
                      "OR TYPE NO AND PRESS ENTER TO EXIT PROGRAM")
                i = input("> ").lower().strip()
                if i == YES:
                    break
                if i == NO:
                    print("quiting...")
                    exit_prog()
            print(f"deleting {published}")
            shutil.rmtree(published, ignore_errors=True)
        print("Cache has been cleared!")
        print("Start Steam again and make sure you have downloaded the mod from Steam Workshop.")
        print("Once the download has finished, launch Rising Storm 2 to re-create the cache.")
    elif choice == FIX_AUDIO:
        print("Fixing audio...")
        audio_dir_src = Path(ww_cache) / Path(f"{len(ww_package_paths) - 1}/Published/CookedPC/{AUDIO_DIR}")
        audio_dir_dst = Path(published) / Path(f"CookedPC/{AUDIO_DIR}")
        if audio_dir_dst.exists():
            print(f"removing existing Winter War audio files: {audio_dir_dst}")
            shutil.rmtree(audio_dir_dst, ignore_errors=True)
        print(f"copying {audio_dir_src} -> {audio_dir_dst}")
        shutil.copytree(audio_dir_src, audio_dir_dst)
        print(f"audio fixed")
    else:
        print(f"unknown choice: {choice}")

    exit_prog()


if __name__ == '__main__':
    main()
