#!/usr/bin/env python3

# pytab.core.py
# A transcoding hardware benchmarking client (for Jellyfin)
#    Copyright (C) 2024 BotBlake <B0TBlake@protonmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##########################################################################################

import click
from pytab import worker
#from pytab import api

placebo_cmd = [
    "./ffmpeg/ffmpeg.exe",
    "-hide_banner",
    "-c:v",
    "h264",
    "-i",
    "./videos/jellyfish-40-mbps-hd-h264.mkv",
    "-c:v",
    "h264",
    "-benchmark",
    "-f",
    "null",
    "-",
]


def benchmark(ffmpeg_cmd):
    print("Benchmarking now...")
    runs = []
    total_workers = 1
    run = True
    last_Speed = -0.5 #to Assure first worker always has the required difference 
    failure_reason = []

    with click.progressbar(length=0, label="Workers: 1, Speed: 0.0") as progress_bar:
        while run:
            output = worker.workMan(total_workers, ffmpeg_cmd)
            # First check if we continue Running:
            if output[0]:
                run = False
                failure_reason.append(output[1])
            elif output[1]["speed"] < 1:
                run = False
                failure_reason.append("performance")
            #elif output[1]["speed"]-last_Speed < 0.5:
            #    run = False
            #    failure_reason.append("failed_inconclusive")
            else: # When no failure happened 
                runs.append(output[1])
                total_workers += 60
                last_Speed = output[1]["speed"]
                progress_bar.label = f"Workers: {total_workers}, Speed: {last_Speed}"
            progress_bar.update(1)
        progress_bar.update(1)
    if len(runs) > 0:
        result = {
            "max_streams" : runs[(len(runs))-1]["workers"],
            "failure_reasons" : failure_reason,
            "single_worker_speed" : runs[(len(runs))-1]["speed"],
            "single_worker_rss_kb" : runs[(len(runs))-1]["rss_kb"],
        }
        return True, runs, result
    else:
        return False, runs, {}
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
        "--ffmpeg",
        "ffmpeg_path",
        type=click.Path(resolve_path=True ,dir_okay=True, exists=True, writable=True, executable=True),
        default="./ffmpeg",
        show_default=True,
        required=False,
        help="Path for JellyfinFFMPEG Download/execution"
)
@click.option(
        "--videos",
        "video_path",
        type=click.Path(resolve_path=True ,dir_okay=True, exists=True, writable=True, readable=True, executable=False),
        default="./ffmpeg",
        show_default=True,
        required=False,
        help="Path for JellyfinFFMPEG Download/execution"
)

@click.option(
        "--debug",
        "debug_flag",
        is_flag=True,
        default=False,
        help="Enable additional debug output"
)

def cli(ffmpeg_path,video_path, debug_flag):
    """
    Python Transcoding Acceleration Benchmark Client made for Jellyfin Hardware Survey
    """

    global debug
    debug = debug_flag

    valid, runs, result = benchmark(placebo_cmd)
    print()
    print("------------DEV-OUT--------------------------------------------------------------------------------")
    print(runs)
    print("-------------------------------------------------")
    print(result)
    print("------------DEV-END--------------------------------------------------------------------------------")

def main():
    return cli(obj={})

if __name__ == "__main__":
    cli()