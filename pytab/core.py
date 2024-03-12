#!/usr/bin/env python3
"""
This comment needs to be overwritten to describe this FILE's role in the
overall software ecosystem of this tool.
"""

import click
from pytab import worker

from typing import Any

# from pytab import api

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    max_content_width=120
)

placebo_cmd = [
    "./ffmpeg/ffmpeg.exe",
    "-hide_banner",
    "-c:v",
    "h264",
    "-i",
    "./videos/jellyfish-40-mbps-hd-h264.mkv",
    "-benchmark",
    "-f",
    "null",
    "-",
]


def benchmark(ffmpeg_cmd: str) -> tuple[list, dict[str, Any]]:
    """
    This function's purpose is X. It accepts a, b, and c types
    as arguments. it returns an x type. especially consider these
    specific aspects when using this function...
    """
    print("Benchmarking now...")
    runs = []
    total_workers = 1
    run = True
    # ensure first worker always has the required difference
    last_Speed = -0.5
    failure_reason = []

    with click.progressbar(
        length=0,
        label="Workers: 1,Speed: 0.0") as progress_bar:
        while run:
            output = worker.workMan(total_workers, ffmpeg_cmd)
            # First check if we continue Running:
            if output[0]:
                run = False
                failure_reason.append(output[1])
            elif output[1]["speed"] < 1:
                run = False
                failure_reason.append("performance")
            # elif output[1]["speed"]-last_Speed < 0.5:
            #    run = False
            #    failure_reason.append("failed_inconclusive")
            else:  # When no failure happened
                runs.append(output[1])
                total_workers += 60
                last_Speed = output[1]["speed"]
                # break up long strings like this.
                label_value = (
                    f"Workers: {total_workers}"
                    ", Speed: {last_Speed}"
                )
                progress_bar.label = 
            progress_bar.update(1)
        progress_bar.update(1)

    result = {
        "max_streams": runs[(len(runs)) - 1]["workers"],
        "failure_reasons": failure_reason,
        "single_worker_speed": runs[(len(runs)) - 1]["speed"],
        "single_worker_rss_kb": runs[(len(runs)) - 1]["rss_kb"],
    }
    return runs, result

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--ffmpeg",
    "ffmpeg_path",
    type=click.Path(
        resolve_path=True,
        dir_okay=True,
        exists=True,
        writable=True,
        executable=True
    ),
    default="./ffmpeg",
    show_default=True,
    required=False,
    help="Path for JellyfinFFMPEG Download/execution",
)
@click.option(
    "--videos",
    "video_path",
    type=click.Path(
        resolve_path=True,
        dir_okay=True,
        exists=True,
        writable=True,
        readable=True,
        executable=False,
    ),
    default="./ffmpeg",
    show_default=True,
    required=False,
    help="Path for JellyfinFFMPEG Download/execution",
)
@click.option(
    "--debug",
    "debug_flag",
    is_flag=True,
    default=False,
    help="Enable additional debug output",
)
def cli(ffmpeg_path: str, video_path: str, debug_flag: str) -> None:
    """
    This function's purpose is X. It accepts a, b, and c types
    as arguments. it returns an x type. especially consider these
    specific aspects when using this function...
    """

    global debug
    debug = debug_flag

    runs, result = benchmark(placebo_cmd)
    print()
    print(
        "------------DEV-OUT"+("-"*80)
    )
    print(runs)
    print("-"*49)
    print(result)
print(
    "------------DEV-END"+("-"*80)
)


def main():
    return cli(obj={})


if __name__ == "__main__":
    cli()
