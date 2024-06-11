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
import os
import click
from pytab import worker, api, hwi
from hashlib import sha256
from requests import get as reqGet

from shutil import rmtree
import zipfile
import tarfile

placebo_cmd = [
    "./ffmpeg/ffmpeg.exe",
    "-hide_banner",
    "-c:v",
    "h264",
    "-i",
    "./videos/nvidia_s.mp4",
    "-c:v",
    "h264_nvenc",
    "-benchmark",
    "-f",
    "null",
    "-",
]


def match_hash(hash_dict: dict) -> tuple:
    supported_hashes = [
        "sha256",
    ]  # list of currently supported hashing methods

    if not hash_dict:
        click.echo("Note: This File cannot be hash-verified!")
        return None, None

    for hash in hash_dict:
        if hash in supported_hashes:
            click.echo(f"Note: Compatible hashing method found. Using {hash}")
            return hash, hash_dict[hash]
    click.echo("Note: This Client cannot hash-verify this File!")
    return None, None


def calculate_sha256(file_path: str) -> str:
    # Calculate SHA256 checksum of a file
    sha256_hash = sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def obtainSource(
    target_path: str, source_url: str, hash_dict: dict, notify_on_download: bool
) -> tuple:
    hash_algorithm, source_hash = match_hash(hash_dict)

    target_path = os.path.realpath(target_path)  # Relative Path!
    filename = os.path.basename(source_url)  # Extract filename from the URL
    file_path = os.path.join(target_path, filename)  # path/filename

    if os.path.exists(file_path):  # if file already exists
        existing_checksum = None
        if hash_algorithm == "sha256":
            existing_checksum = calculate_sha256(file_path)  # checksum validation

        if existing_checksum == source_hash or source_hash is None:  # if valid/no sum
            return True, file_path  # Checksum valid, no need to download again
        else:
            os.remove(file_path)  # Delete file if checksum doesn't match

    # Create target path if non present
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    if notify_on_download:
        click.echo("Downloading File...", nl=False)

    try:  # Download file
        response = reqGet(source_url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            if notify_on_download:
                click.echo(" Done!")
        else:
            return False, response.status_code  # Unable to download file
    except Exception:
        return False, "Unknown Error!"  # Unable to download file
    downloaded_checksum = calculate_sha256(file_path)  # checksum validation
    if downloaded_checksum == source_hash or source_hash is None:  # if valid/no sum
        return True, file_path  # Checksum valid
    else:
        os.remove(file_path)  # Delete file if checksum doesn't match
        return False, "Invalid Checksum!"  # Checksum invalid


def unpackArchive(archive_path, target_path):
    if os.path.exists(target_path):
        rmtree(target_path)
        click.echo("--> Replacing existing Files with validated ones.")
    os.makedirs(target_path)

    click.echo("Unpacking Archive...", nl=False)

    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as zip_ref:
            zip_ref.extractall(target_path)
    elif archive_path.endswith(".tar.gz"):
        with tarfile.open(archive_path, "r:gz") as tar_ref:
            tar_ref.extractall(target_path)
    click.echo(" Done!")


def benchmark(ffmpeg_cmd: str) -> tuple:
    print("Benchmarking now...")
    runs = []
    total_workers = 9
    run = True
    last_Speed = -0.5  # to Assure first worker always has the required difference
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
            # elif output[1]["speed"]-last_Speed < 0.5:
            #    run = False
            #    failure_reason.append("failed_inconclusive")
            else:  # When no failure happened
                runs.append(output[1])
                total_workers += 1
                last_Speed = output[1]["speed"]
                progress_bar.label = f"Workers: {total_workers}, Speed: {last_Speed}"
            progress_bar.update(1)
        progress_bar.update(1)
    if len(runs) > 0:
        result = {
            "max_streams": runs[(len(runs)) - 1]["workers"],
            "failure_reasons": failure_reason,
            "single_worker_speed": runs[(len(runs)) - 1]["speed"],
            "single_worker_rss_kb": runs[(len(runs)) - 1]["rss_kb"],
        }
        return True, runs, result
    else:
        return False, runs, {}


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--ffmpeg",
    "ffmpeg_path",
    type=click.Path(
        resolve_path=True,
        dir_okay=True,
        writable=True,
        executable=True,
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
        writable=True,
        readable=True,
    ),
    default="./videos",
    show_default=True,
    required=False,
    help="Path for download of test files. (SSD required)",
)
@click.option(
    "--debug",
    "debug_flag",
    is_flag=True,
    default=False,
    help="Enable additional debug output",
)
def cli(ffmpeg_path: str, video_path: str, debug_flag: bool) -> None:
    """
    Python Transcoding Acceleration Benchmark Client made for Jellyfin Hardware Survey
    """
    global debug
    debug = debug_flag

    platforms = api.getPlatform()  # obtain list of (supported) Platforms + ID's
    platformID = hwi.MatchID(platforms, 0)  # dummy: return = platforms[x]["id"]
    valid, server_data = api.getTestData(platformID)
    if not valid:
        click.echo(f"Cancled: {server_data}")

    # Download ffmpeg
    ffmpeg_data = server_data["ffmpeg"]
    click.echo("Loading ffmpeg")

    ffmpeg_download = obtainSource(
        ffmpeg_path, ffmpeg_data["ffmpeg_source_url"], ffmpeg_data["ffmpeg_hashs"], True
    )

    if ffmpeg_download[0] is False:
        click.echo(f"An Error occured: {ffmpeg_download[1]}", err=True)
        click.pause("Press any key to exit")
        exit()

    ffmpeg_files = f"{ffmpeg_path}/ffmpeg_files"
    unpackArchive(ffmpeg_download[1], ffmpeg_files)
    ffmpeg_binary = f"{ffmpeg_files}/ffmpeg"  # noqa: F841

    click.echo()

    exit()

    valid, runs, result = benchmark(placebo_cmd)
    print()
    print(("-" * 15) + "DEV-OUT" + ("-" * 40))
    print(runs)
    print("-" * 20)
    print(result)
    print(("-" * 15) + "DEV-END" + ("-" * 40))


def main():
    return cli(obj={})


if __name__ == "__main__":
    cli()
