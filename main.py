import copy
from datetime import datetime
import json
import os
import yt_dlp
from yt_dlp.postprocessor import MetadataParserPP

# if in doubt about how a CLI option changes to embedded options, check out
# https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py


def title_contains_keyword(info, *, incomplete):
    keywords = url["title_keywords"].split("|")
    title = info.get("title", "").lower()
    if title:
        for keyword in keywords:
            if keyword.lower() not in title:
                return f"Title does not contain keyword: {keyword}"


try:
    with open("/app/data/archive_urls.json", "r") as file:
        archive_urls = json.load(file)
except FileNotFoundError:
    print("Error: archive_urls.json not found.")
    exit(1)

video_ydl_opts = {
    "check_formats": True,
    "compat_opts": ["no-keep-subs"],
    "concurrent_fragment_downloads": 5,
    "download_archive": "archive.log",
    "format": "(bestvideo[vcodec^=av01][height>=4320][fps>30]/bestvideo[vcodec^=vp9.2][height>=4320][fps>30]/bestvideo[vcodec^=vp9][height>=4320][fps>30]/bestvideo[vcodec^=avc1][height>=4320][fps>30]/bestvideo[height>=4320][fps>30]/bestvideo[vcodec^=av01][height>=4320]/bestvideo[vcodec^=vp9.2][height>=4320]/bestvideo[vcodec^=vp9][height>=4320]/bestvideo[vcodec^=avc1][height>=4320]/bestvideo[height>=4320]/bestvideo[vcodec^=av01][height>=2880][fps>30]/bestvideo[vcodec^=vp9.2][height>=2880][fps>30]/bestvideo[vcodec^=vp9][height>=2880][fps>30]/bestvideo[vcodec^=avc1][height>=2880][fps>30]/bestvideo[height>=2880][fps>30]/bestvideo[vcodec^=av01][height>=2880]/bestvideo[vcodec^=vp9.2][height>=2880]/bestvideo[vcodec^=vp9][height>=2880]/bestvideo[vcodec^=avc1][height>=2880]/bestvideo[height>=2880]/bestvideo[vcodec^=av01][height>=2160][fps>30]/bestvideo[vcodec^=vp9.2][height>=2160][fps>30]/bestvideo[vcodec^=vp9][height>=2160][fps>30]/bestvideo[vcodec^=avc1][height>=2160][fps>30]/bestvideo[height>=2160][fps>30]/bestvideo[vcodec^=av01][height>=2160]/bestvideo[vcodec^=vp9.2][height>=2160]/bestvideo[vcodec^=vp9][height>=2160]/bestvideo[vcodec^=avc1][height>=2160]/bestvideo[height>=2160]/bestvideo[vcodec^=av01][height>=1440][fps>30]/bestvideo[vcodec^=vp9.2][height>=1440][fps>30]/bestvideo[vcodec^=vp9][height>=1440][fps>30]/bestvideo[vcodec^=avc1][height>=1440][fps>30]/bestvideo[height>=1440][fps>30]/bestvideo[vcodec^=av01][height>=1440]/bestvideo[vcodec^=vp9.2][height>=1440]/bestvideo[vcodec^=vp9][height>=1440]/bestvideo[vcodec^=avc1][height>=1440]/bestvideo[height>=1440]/bestvideo[vcodec^=av01][height>=1080][fps>30]/bestvideo[vcodec^=vp9.2][height>=1080][fps>30]/bestvideo[vcodec^=vp9][height>=1080][fps>30]/bestvideo[vcodec^=avc1][height>=1080][fps>30]/bestvideo[height>=1080][fps>30]/bestvideo[vcodec^=av01][height>=1080]/bestvideo[vcodec^=vp9.2][height>=1080]/bestvideo[vcodec^=vp9][height>=1080]/bestvideo[vcodec^=avc1][height>=1080]/bestvideo[height>=1080]/bestvideo[vcodec^=av01][height>=720][fps>30]/bestvideo[vcodec^=vp9.2][height>=720][fps>30]/bestvideo[vcodec^=vp9][height>=720][fps>30]/bestvideo[vcodec^=avc1][height>=720][fps>30]/bestvideo[height>=720][fps>30]/bestvideo[vcodec^=av01][height>=720]/bestvideo[vcodec^=vp9.2][height>=720]/bestvideo[vcodec^=vp9][height>=720]/bestvideo[vcodec^=avc1][height>=720]/bestvideo[height>=720]/bestvideo[vcodec^=av01][height>=480][fps>30]/bestvideo[vcodec^=vp9.2][height>=480][fps>30]/bestvideo[vcodec^=vp9][height>=480][fps>30]/bestvideo[vcodec^=avc1][height>=480][fps>30]/bestvideo[height>=480][fps>30]/bestvideo[vcodec^=av01][height>=480]/bestvideo[vcodec^=vp9.2][height>=480]/bestvideo[vcodec^=vp9][height>=480]/bestvideo[vcodec^=avc1][height>=480]/bestvideo[height>=480]/bestvideo[vcodec^=av01][height>=360][fps>30]/bestvideo[vcodec^=vp9.2][height>=360][fps>30]/bestvideo[vcodec^=vp9][height>=360][fps>30]/bestvideo[vcodec^=avc1][height>=360][fps>30]/bestvideo[height>=360][fps>30]/bestvideo[vcodec^=av01][height>=360]/bestvideo[vcodec^=vp9.2][height>=360]/bestvideo[vcodec^=vp9][height>=360]/bestvideo[vcodec^=avc1][height>=360]/bestvideo[height>=360]/bestvideo[vcodec^=avc1][height>=240][fps>30]/bestvideo[vcodec^=av01][height>=240][fps>30]/bestvideo[vcodec^=vp9.2][height>=240][fps>30]/bestvideo[vcodec^=vp9][height>=240][fps>30]/bestvideo[height>=240][fps>30]/bestvideo[vcodec^=avc1][height>=240]/bestvideo[vcodec^=av01][height>=240]/bestvideo[vcodec^=vp9.2][height>=240]/bestvideo[vcodec^=vp9][height>=240]/bestvideo[height>=240]/bestvideo[vcodec^=avc1][height>=144][fps>30]/bestvideo[vcodec^=av01][height>=144][fps>30]/bestvideo[vcodec^=vp9.2][height>=144][fps>30]/bestvideo[vcodec^=vp9][height>=144][fps>30]/bestvideo[height>=144][fps>30]/bestvideo[vcodec^=avc1][height>=144]/bestvideo[vcodec^=av01][height>=144]/bestvideo[vcodec^=vp9.2][height>=144]/bestvideo[vcodec^=vp9][height>=144]/bestvideo[height>=144]/bestvideo)+(bestaudio[acodec^=opus]/bestaudio)/best",
    "ignoreerrors": "download_only",
    "merge_output_template": "mkv",
    "outtmpl": {
        "default": "%(uploader)s - %(upload_date)s - %(title)s [%(id)s].%(ext)s"
    },
    "overwrites": False,
    "postprocessors": [
        {"key": "FFmpegMetadata", "add_metadata": True},
        {"key": "FFmpegEmbedSubtitle"},
        {"key": "EmbedThumbnail", "already_have_thumbnail": False},
    ],
    "source_address": "0.0.0.0",
    "subtitleslangs": ["all"],
    "throttledratelimit": 100000,
    "verbose": True,
    "writesubtitles": True,
    "writethumbnail": True,
}

audio_ydl_opts = {
    "check_formats": True,
    "concurrent_fragment_downloads": 5,
    "download_archive": "archive.log",
    "format": "(bestaudio[acodec^=opus]/bestaudio)/best",
    "ignoreerrors": "download_only",
    "max_sleep_interval": 30,
    "merge_output_template": "mkv",
    "outtmpl": {
        "default": "%(uploader)s - %(upload_date)s - %(title)s [%(id)s].%(ext)s"
    },
    "overwrites": False,
    "postprocessors": [
        {"key": "FFmpegMetadata", "add_metadata": True},
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        },
    ],
    "sleep_interval": 5,
    "sleep_interval_requests": 1,
    "source_address": "0.0.0.0",
    "throttledratelimit": 100000,
    "verbose": True,
}

for url in archive_urls:
    archive_log_lines = 0
    downloaded_videos = 0

    # get the number of lines in the archive.log file
    try:
        with open("/app/data/archive.log", "r") as file:
            archive_log_lines = len(file.readlines())
    except FileNotFoundError:
        pass

    ydl_opts = None

    if url["type"] == "audio":
        ydl_opts = copy.deepcopy(audio_ydl_opts)
    elif url["type"] == "video":
        ydl_opts = copy.deepcopy(video_ydl_opts)

    outtmpl = os.path.join(url["storage_path"], ydl_opts["outtmpl"]["default"])
    if url["output_template"]:
        outtmpl = os.path.join(url["storage_path"], url["output_template"])
    ydl_opts["outtmpl"]["default"] = outtmpl

    if url["cookie_file"]:
        ydl_opts["cookiefile"] = url["cookie_file"]

    if url["title_keywords"]:
        ydl_opts["match_filter"] = title_contains_keyword

    # if sponsorblock_enabled exists and is true, add a new postprocessor to the ydl_opts
    if url.get("sponsorblock_enabled", False):
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

        # modify the FFmpegMetadata postprocessor to include the sponsorblock chapters
        for postprocessor in ydl_opts["postprocessors"]:
            if postprocessor.get("key") == "FFmpegMetadata":
                postprocessor["add_chapters"] = True
                postprocessor["add_metadata"] = False
                postprocessor["add_infojson"] = None
                break

    with yt_dlp.YoutubeDL(ydl_opts) as client:
        client.download(url["address"])

    # once we've finished downloaded files, check how many new lines are in the archive.log file
    try:
        with open("archive.log", "r") as file:
            downloaded_videos = len(file.readlines()) - archive_log_lines
    except FileNotFoundError:
        pass

    url["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url["last_run_downloaded"] = downloaded_videos

    # update the archive_urls.json file with the new last_run and last_run_downloaded values
    with open("archive_urls.json", "w") as file:
        json.dump(archive_urls, file, indent=4)
