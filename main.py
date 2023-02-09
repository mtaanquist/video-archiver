import copy
import json
import os
import yt_dlp
from yt_dlp.postprocessor import MetadataParserPP


with open("archive_urls.json", "r") as file:
    archive_urls = json.load(file)

video_ydl_opts = {
    "check_formats": True,
    "compat_opts": ["no-keep-subs"],
    "concurrent_fragment_downloads": 5,
    "download_archive": "archive.log",
    "format": "(bestvideo[vcodec^=av01][height>=4320][fps>30]/bestvideo[vcodec^=vp9.2][height>=4320][fps>30]/bestvideo[vcodec^=vp9][height>=4320][fps>30]/bestvideo[vcodec^=avc1][height>=4320][fps>30]/bestvideo[height>=4320][fps>30]/bestvideo[vcodec^=av01][height>=4320]/bestvideo[vcodec^=vp9.2][height>=4320]/bestvideo[vcodec^=vp9][height>=4320]/bestvideo[vcodec^=avc1][height>=4320]/bestvideo[height>=4320]/bestvideo[vcodec^=av01][height>=2880][fps>30]/bestvideo[vcodec^=vp9.2][height>=2880][fps>30]/bestvideo[vcodec^=vp9][height>=2880][fps>30]/bestvideo[vcodec^=avc1][height>=2880][fps>30]/bestvideo[height>=2880][fps>30]/bestvideo[vcodec^=av01][height>=2880]/bestvideo[vcodec^=vp9.2][height>=2880]/bestvideo[vcodec^=vp9][height>=2880]/bestvideo[vcodec^=avc1][height>=2880]/bestvideo[height>=2880]/bestvideo[vcodec^=av01][height>=2160][fps>30]/bestvideo[vcodec^=vp9.2][height>=2160][fps>30]/bestvideo[vcodec^=vp9][height>=2160][fps>30]/bestvideo[vcodec^=avc1][height>=2160][fps>30]/bestvideo[height>=2160][fps>30]/bestvideo[vcodec^=av01][height>=2160]/bestvideo[vcodec^=vp9.2][height>=2160]/bestvideo[vcodec^=vp9][height>=2160]/bestvideo[vcodec^=avc1][height>=2160]/bestvideo[height>=2160]/bestvideo[vcodec^=av01][height>=1440][fps>30]/bestvideo[vcodec^=vp9.2][height>=1440][fps>30]/bestvideo[vcodec^=vp9][height>=1440][fps>30]/bestvideo[vcodec^=avc1][height>=1440][fps>30]/bestvideo[height>=1440][fps>30]/bestvideo[vcodec^=av01][height>=1440]/bestvideo[vcodec^=vp9.2][height>=1440]/bestvideo[vcodec^=vp9][height>=1440]/bestvideo[vcodec^=avc1][height>=1440]/bestvideo[height>=1440]/bestvideo[vcodec^=av01][height>=1080][fps>30]/bestvideo[vcodec^=vp9.2][height>=1080][fps>30]/bestvideo[vcodec^=vp9][height>=1080][fps>30]/bestvideo[vcodec^=avc1][height>=1080][fps>30]/bestvideo[height>=1080][fps>30]/bestvideo[vcodec^=av01][height>=1080]/bestvideo[vcodec^=vp9.2][height>=1080]/bestvideo[vcodec^=vp9][height>=1080]/bestvideo[vcodec^=avc1][height>=1080]/bestvideo[height>=1080]/bestvideo[vcodec^=av01][height>=720][fps>30]/bestvideo[vcodec^=vp9.2][height>=720][fps>30]/bestvideo[vcodec^=vp9][height>=720][fps>30]/bestvideo[vcodec^=avc1][height>=720][fps>30]/bestvideo[height>=720][fps>30]/bestvideo[vcodec^=av01][height>=720]/bestvideo[vcodec^=vp9.2][height>=720]/bestvideo[vcodec^=vp9][height>=720]/bestvideo[vcodec^=avc1][height>=720]/bestvideo[height>=720]/bestvideo[vcodec^=av01][height>=480][fps>30]/bestvideo[vcodec^=vp9.2][height>=480][fps>30]/bestvideo[vcodec^=vp9][height>=480][fps>30]/bestvideo[vcodec^=avc1][height>=480][fps>30]/bestvideo[height>=480][fps>30]/bestvideo[vcodec^=av01][height>=480]/bestvideo[vcodec^=vp9.2][height>=480]/bestvideo[vcodec^=vp9][height>=480]/bestvideo[vcodec^=avc1][height>=480]/bestvideo[height>=480]/bestvideo[vcodec^=av01][height>=360][fps>30]/bestvideo[vcodec^=vp9.2][height>=360][fps>30]/bestvideo[vcodec^=vp9][height>=360][fps>30]/bestvideo[vcodec^=avc1][height>=360][fps>30]/bestvideo[height>=360][fps>30]/bestvideo[vcodec^=av01][height>=360]/bestvideo[vcodec^=vp9.2][height>=360]/bestvideo[vcodec^=vp9][height>=360]/bestvideo[vcodec^=avc1][height>=360]/bestvideo[height>=360]/bestvideo[vcodec^=avc1][height>=240][fps>30]/bestvideo[vcodec^=av01][height>=240][fps>30]/bestvideo[vcodec^=vp9.2][height>=240][fps>30]/bestvideo[vcodec^=vp9][height>=240][fps>30]/bestvideo[height>=240][fps>30]/bestvideo[vcodec^=avc1][height>=240]/bestvideo[vcodec^=av01][height>=240]/bestvideo[vcodec^=vp9.2][height>=240]/bestvideo[vcodec^=vp9][height>=240]/bestvideo[height>=240]/bestvideo[vcodec^=avc1][height>=144][fps>30]/bestvideo[vcodec^=av01][height>=144][fps>30]/bestvideo[vcodec^=vp9.2][height>=144][fps>30]/bestvideo[vcodec^=vp9][height>=144][fps>30]/bestvideo[height>=144][fps>30]/bestvideo[vcodec^=avc1][height>=144]/bestvideo[vcodec^=av01][height>=144]/bestvideo[vcodec^=vp9.2][height>=144]/bestvideo[vcodec^=vp9][height>=144]/bestvideo[height>=144]/bestvideo)+(bestaudio[acodec^=opus]/bestaudio)/best",
    "ignoreerrors": "download_only",
    "merge_output_template": "mkv",
    "outtmpl": {"default": "%(uploader)s - %(upload_date)s - %(title)s [%(id)s].%(ext)s"},
    "overwrites": False,
    "postprocessors": [{
        "key": "FFmpegMetadata",
        "add_metadata": True
    }, {
        "key": "FFmpegEmbedSubtitle"
    }, {
        "key": "EmbedThumbnail",
        "already_have_thumbnail": False
    }, {
        'key': 'MetadataParser',
        'when': 'pre_process',
        'actions': [
            (MetadataParserPP.Actions.INTERPRET, 'title', "%(meta_title)s"), 
            (MetadataParserPP.Actions.INTERPRET, 'uploader', "%(meta_artist)s")
        ]
    }],
    "source_address": "0.0.0.0",
    "subtitleslangs": ["all"],
    "throttledratelimit": 100000,
    "verbose": True,
    "writesubtitles": True,
    "writethumbnail": True
}

audio_ydl_opts = {
    "check_formats": True,
    "concurrent_fragment_downloads": 5,
    "download_archive": "archive.log",
    "format": "(bestaudio[acodec^=opus]/bestaudio)/best",
    "ignoreerrors": "download_only",
    "max_sleep_interval": 30,
    "merge_output_template": "mkv",
    "outtmpl": {"default": "%(uploader)s - %(upload_date)s - %(title)s [%(id)s].%(ext)s"},
    "overwrites": False,
    "postprocessors": [{
        "key": "FFmpegMetadata",
        "add_metadata": True
    }, {
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }, {
        'key': 'MetadataParser',
        'when': 'pre_process',
        'actions': [
            (MetadataParserPP.Actions.INTERPRET, 'title', "%(meta_title)s"), 
            (MetadataParserPP.Actions.INTERPRET, 'uploader', "%(meta_artist)s")
        ]
    }],
    "sleep_interval": 5,
    "sleep_interval_requests": 1,
    "source_address": "0.0.0.0",
    "throttledratelimit": 100000,
    "verbose": True
}

for url in archive_urls:
    ydl_opts = None
    outtmpl = None

    match url["type"]:
        case "audio":
            ydl_opts = copy.deepcopy(audio_ydl_opts)
        case "video":
            ydl_opts = copy.deepcopy(video_ydl_opts)

    outtmpl = ydl_opts["outtmpl"]["default"]
    if url["output_template"]:
        outtmpl = os.path.join(url["storage_path"], url["output_template"])
    else:
        outtmpl = os.path.join(url["storage_path"], outtmpl)
    ydl_opts["outtmpl"]["default"] = outtmpl

    with yt_dlp.YoutubeDL(ydl_opts) as client:
        client.download(url["address"])
