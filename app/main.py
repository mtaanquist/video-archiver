import copy
import json
from pathlib import Path
import toml
import yt_dlp

CONFIG_FILENAME = "config.toml"


def read_config(config_file):
    script_dir = Path(__file__).resolve().parent

    config_file_path = script_dir / config_file
    if not config_file_path.exists():
        raise FileNotFoundError(
            f"The configuration file '{config_file}' does not exist."
        )

    config = toml.load(config_file_path)

    archive_urls = read_json_file(script_dir / config["paths"]["archive_urls"])
    audio_options = read_json_file(script_dir / config["paths"]["audio_options"])
    video_options = read_json_file(script_dir / config["paths"]["video_options"])

    return config, archive_urls, audio_options, video_options


def read_json_file(json_file):
    if not json_file.exists():
        raise FileNotFoundError(f"The JSON file '{json_file}' does not exist.")

    with json_file.open("r") as file:
        return json.load(file)


def initialize_ydl_opts(archive_url, audio_options, video_options):
    if archive_url["type"] == "audio":
        return copy.deepcopy(audio_options)
    elif archive_url["type"] == "video":
        return copy.deepcopy(video_options)
    return {}


def set_output_template(archive_url, ydl_opts):
    outtmpl = Path(archive_url["storage_path"]) / ydl_opts["outtmpl"]["default"]
    if archive_url["output_template"]:
        outtmpl = Path(archive_url["storage_path"]) / archive_url["output_template"]

    ydl_opts["outtmpl"]["default"] = str(outtmpl)


def add_sponsorblock_postprocessors(archive_url, ydl_opts):
    if archive_url.get("sponsorblock_enabled", False):
        ydl_opts["postprocessors"].append(
            {
                "api": "https://sponsor.ajay.app",
                "categories": {"sponsor"},
                "key": "SponsorBlock",
                "when": "after_filter",
            }
        )

        ydl_opts["postprocessors"].append(
            {
                "force_keyframes": False,
                "key": "ModifyChapters",
                "remove_chapters_patterns": [],
                "remove_ranges": [],
                "remove_sponsor_segments": {"sponsor"},
                "sponsorblock_chapter_title": "[SponsorBlock]: %(category_names)l",
            }
        )

        modify_ffmpegmetadata_postprocessor(ydl_opts)


def modify_ffmpegmetadata_postprocessor(ydl_opts):
    for postprocessor in ydl_opts["postprocessors"]:
        if postprocessor.get("key") == "FFmpegMetadata":
            postprocessor["add_chapters"] = True
            postprocessor["add_metadata"] = False
            postprocessor["add_infojson"] = None
            break


def download_archive_url(archive_url, ydl_opts):
    set_output_template(archive_url, ydl_opts)

    if archive_url["cookie_file"]:
        ydl_opts["cookiefile"] = archive_url["cookie_file"]

    if archive_url["title_keywords"]:
        ydl_opts["match_filter"] = lambda info, *, incomplete: title_contains_keyword(
            info, archive_url
        )

    if "postprocessors" not in ydl_opts:
        ydl_opts["postprocessors"] = []

    add_sponsorblock_postprocessors(archive_url, ydl_opts)

    with yt_dlp.YoutubeDL(ydl_opts) as client:
        client.download([archive_url["address"]])


def title_contains_keyword(info, archive_url):
    keywords = archive_url["title_keywords"].split("|")
    title = info.get("title", "").lower()
    if title:
        for keyword in keywords:
            if keyword.lower() not in title:
                return f"Title does not contain keyword: {keyword}"


config, archive_urls, audio_options, video_options = read_config(CONFIG_FILENAME)
for archive_url in archive_urls:
    download_archive_url(
        archive_url, initialize_ydl_opts(archive_url, audio_options, video_options)
    )
