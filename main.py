from pathlib import Path
import re
import csv

# CONFIGURATIONS
# TODO: Update Target Path to location of your files.
# TODO: When Ready, Adjust DRY_RUN to false
TARGET_PATH = r"X:\Media Server\Movies"
DRY_RUN = False 
CSV_OUTPUT = "rename_results.csv"

# JUNK TERMS
JUNK_TERMS = {
    # RESOLUTIONS
    "1080p", "720p", "480p", "360p", "2160p", "4k", "sd", "uhd",

    # SOURCES
    "hdrip", "webrip", "web", "bluray", "brrip", "hdtv", "hevc",
    "dvdrip", "dvdscr", "cam", "telesync", "ts", "web-dl", "webdl",
    "hdts", "hddvdrip",

    # CODECS
    "xvid", "x264", "h264", "x265", "h265", "avc", "vp9", "divx", "vp8",

    # AUDIO
    "ac3", "aac", "dts", "eac3", "dd5", "dd51", "51", "5.1", "2.0", "stereo", "mono",

    # SITES
    "evo", "rarbg", "tgx", "yts", "galaxyrg", "hd4u", "gcjm", "oft", "mircrew",
    "publichd", "uindex", "torrenting", "ozlem", "ettv", "ettvhd", "ettv-team", "fov", "yify",

    # FILE SIZES
    "1600mb", "1400mb", "1200mb", "700mb", "500mb", "350mb", "250mb", "200mb",
    "mp4", "mkv", "avi", "mov", "wmv", "flv", "m4v",

    # EXTRAS
    "remastered", "bonus", "edition", "ed", "extended", "uncut", "director", "cut", "unrated",
    "limited", "theatrical", "version", "special", "collection", "complete", "hd", "hq",

    # RANDOMS
    "subs", "sub", "eng", "ita", "french", "spanish", "german", "dual", "audio", "dub",
    "internal", "proper", "repack", "readnfo", "nfo", "sample", "preview", "3500Mb", "Ddp5", "Galaxyrgtgx",
    "Lamatgx", "800Mb"
}

YEAR_PATTERN = re.compile(r"(19\d{2}|20\d{2})")

def sanitize_name(name: str) -> str:
    # Remove website prefixes
    name = re.sub(r"^www\.[^\s]+[\s\-]+", "", name, flags=re.IGNORECASE)

    # Replace separators with spaces
    name = re.sub(r"[._\-]", " ", name)

    # Remove brackets
    name = re.sub(r"[\[\]\(\)]", "", name)

    # Remove non-alphanumeric characters
    name = re.sub(r"[^a-zA-Z0-9\s]", "", name)

    words = name.split()

    cleaned_words = []
    year = None

    for word in words:
        lower = word.lower()
        if lower in JUNK_TERMS:
            continue
        if YEAR_PATTERN.fullmatch(word):
            year = word
            continue
        cleaned_words.append(word)

    title = " ".join(cleaned_words).strip()
    title = title.title()

    if year:
        return f"{title} ({year})"

    return title

def rename_items(path_str: str, csv_path: str):
    path = Path(path_str)
    results = []

    if not path.exists():
        print("ERROR: PATH DOES NOT EXIST")
        return

    for item in path.iterdir():
        new_name = sanitize_name(item.stem if item.is_file() else item.name)

        if item.is_file():
            new_name_with_ext = new_name + item.suffix
        else:
            new_name_with_ext = new_name

        results.append([item.name, new_name_with_ext, "file" if item.is_file() else "folder"])

        if new_name_with_ext != item.name:
            print(f"{item.name} → {new_name_with_ext}")

            if not DRY_RUN:
                item.rename(item.with_name(new_name_with_ext))

    # Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["original_name", "new_name", "type"])
        writer.writerows(results)

    print(f"\nCSV SAVED TO: {csv_path}")

# Run the script
rename_items(TARGET_PATH, CSV_OUTPUT)
