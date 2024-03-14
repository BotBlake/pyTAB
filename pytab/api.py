#!/usr/bin/env python3

# pytab.api.py
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

cmd = [
    "C:/Users/.../Documents/Software/pyTAB/ffmpeg/ffmpeg.exe",
    "-hide_banner",
    "-loglevel",
    "error",
    "-c:v",
    "h264",
    "-i",
    "C:/Users/.../Documents/Software/pyTAB/videos/jellyfish-40-mbps-hd-h264.mkv",
    "-progress",
    "-",
    "-f",
    "null",
    "-",
    "-benchmark",
]


def launch():
    # Logic needs to go here
    return cmd #hardcoded for now!