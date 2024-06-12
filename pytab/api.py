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
import click
import requests


def getPlatform(server_url: str) -> list:
    click.echo("| Fetch Supported Platforms...", nl=False)
    platforms = None
    try:
        response = requests.get(f"{server_url}/api/v1/TestDataApi/Platforms")
        if response.status_code == 200:
            click.echo(" success!")
            platforms = response.json()
        else:
            click.echo(" Error")
            click.echo(f"ERROR: Server replied with {response.status_code}")
            click.pause("Press any key to exit")
            exit()
    except Exception:
        click.echo(" Error")
        click.echo("ERROR: No connection to Server possible")
        exit()
    platforms = platforms["platforms"]
    return platforms


def getTestData(platformID: str) -> tuple:
    # All this will be replaced by actual API code.
    # If Return Code 429, message = retry_after - header
    valid = True
    if platformID == placebo_platforms["platforms"][0]["id"]:  # if Windows 11
        message = placebo_WinTestData
    elif platformID == placebo_platforms["platforms"][1]["id"]:  # if Ubuntu / Linux
        message = placebo_LinxTestData
    else:
        print("Sorry! The dummy API is only build for Win11 and Ubuntu")
        exit(1)

    return valid, message


# Hardcoded API Responses, for Dev Info check Server Whitepaper
placebo_platforms = {
    "platforms": [
        {
            "id": "2c361be8-c0ec-4020-984b-66c620dad840",
            "name": "Windows 11",
            "type": "Windows",
            "version": "Windows 11 version 23H2",
            "version_id": "22631",
            "display_name": "Windows 11",
            "replacement_id": None,
            "supported": True,
        },
        {
            "id": "8d58b84b-73dc-4275-985d-123abe886818",
            "name": "Ubuntu",
            "type": "Linux",
            "version": "Ubuntu",
            "version_id": "22.04",
            "display_name": "Ubuntu Focal",
            "replacement_id": None,
            "supported": True,
        },
    ]
}

placebo_WinTestData = {
    "token": "XL+mWzK8HrlwxFbaAUEA86vyFtg6hv85usNrnsrmzcUDCOpjP6mSdhChZXzUXbUUQR5j7N+ecLQa6+fCjE1amvfgUj5Duvgek1vpHsyX9VO41GR8MBu+/jx/ln6eaFJ+u57u+6MRC0oNhniJGqVtcw==",
    "ffmpeg": {
        "ffmpeg_source_url": "https://repo.jellyfin.org/files/ffmpeg/windows/latest-6.x/win64/jellyfin-ffmpeg_6.0.1-7-portable_win64.zip",
        "ffmpeg_version": "6.0.1-7",
        "ffmpeg_hashs": {
            "sha256": "2fd7712a453c112c2577e4ed84c2f7b48af3dc1bd56a54095ba3c8ac854f08e3"
        },
    },
    "tests": [
        {
            "name": "jellyfish-40-mbps-hd-h264",
            "source_url": "https://repo.jellyfin.org/jellyfish/media/jellyfish-40-mbps-hd-h264.mkv",
            "source_hashs": None,
            "test_type": "transcode",
            "data": [
                {
                    "id": "097a9f8c-93fb-803d-b661-636d473a43d2",
                    "from_resolution": "720p",
                    "to_resolution": "1080p",
                    "bitrate": 9616000,
                    "arguments": [
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v hevc_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:142:format=nv12 -c:v hevc_qsv -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v hevc_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:142:yuv420p -c:v hevc_nvenc -preset p1 -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:142:format=nv12 -c:v hevc_vaapi -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,142)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx265 -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v h264_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:142:yuv420p -c:v h264_nvenc -preset p1 -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:142:format=nv12 -c:v h264_vaapi -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v h264_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:142:format=nv12 -c:v h264_qsv -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,142)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx264 -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                    ],
                },
            ],
        },
    ],
}
placebo_LinxTestData = {
    "token": "XL+mWzK8HrlwxFbaAUEA86vyFtg6hv85usNrnsrmzcUDCOpjP6mSdhChZXzUXbUUQR5j7N+ecLQa6+fCjE1amvfgUj5Duvgek1vpHsyX9VO41GR8MBu+/jx/ln6eaFJ+u57u+6MRC0oNhniJGqVtcw==",
    "ffmpeg": {
        "ffmpeg_source_url": "https://repo.jellyfin.org/files/ffmpeg/ubuntu/latest-6.x/amd64/jellyfin-ffmpeg6_6.0.1-7-focal_amd64.deb",
        "ffmpeg_version": "6.0.1-7",
        "ffmpeg_hashs": {
            "sha256": "a01b7d556f69941041e3265f916c22613b2f58fd39a062ccf8a3104b3c99350d"
        },
    },
    "tests": [
        {
            "name": "jellyfish-40-mbps-hd-h264",
            "source_url": "https://repo.jellyfin.org/jellyfish/media/jellyfish-40-mbps-hd-h264.mkv",
            "source_hashs": None,
            "test_type": "transcode",
            "data": [
                {
                    "id": "097a9f8c-93fb-803d-b661-636d473a43d2",
                    "from_resolution": "720p",
                    "to_resolution": "1080p",
                    "bitrate": 9616000,
                    "arguments": [
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v hevc_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:142:format=nv12 -c:v hevc_qsv -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v hevc_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:142:yuv420p -c:v hevc_nvenc -preset p1 -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:142:format=nv12 -c:v hevc_vaapi -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,142)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx265 -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v h264_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:142:yuv420p -c:v h264_nvenc -preset p1 -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:142:format=nv12 -c:v h264_vaapi -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v h264_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:142:format=nv12 -c:v h264_qsv -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,142)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx264 -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                    ],
                },
                {
                    "id": "aadc3d7e-8ee7-2cd0-3bfe-86df8f994a45",
                    "from_resolution": "720p",
                    "to_resolution": "2160p",
                    "bitrate": 79616000,
                    "arguments": [
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v hevc_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:142:format=nv12 -c:v hevc_qsv -preset veryfast -b:v 79616000 -maxrate 79616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v hevc_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:142:yuv420p -c:v hevc_nvenc -preset p1 -b:v 79616000 -maxrate 79616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:142:format=nv12 -c:v hevc_vaapi -b:v 79616000 -maxrate 79616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,142)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx265 -preset veryfast -b:v 79616000 -maxrate 79616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v h264_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:142:yuv420p -c:v h264_nvenc -preset p1 -b:v 79616000 -maxrate 79616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:142:format=nv12 -c:v h264_vaapi -b:v 79616000 -maxrate 79616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v h264_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:142:format=nv12 -c:v h264_qsv -preset veryfast -b:v 79616000 -maxrate 79616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,142)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx264 -preset veryfast -b:v 79616000 -maxrate 79616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                    ],
                },
            ],
        },
        {
            "name": "jellyfish-40-mbps-hd-hevc-10bit",
            "source_url": "https://repo.jellyfin.org/jellyfish/media/jellyfish-40-mbps-hd-hevc-10bit.mkv",
            "source_hashs": None,
            "test_type": "transcode",
            "data": [
                {
                    "id": "7f310440-5cde-6c14-f774-109bd052ebbf",
                    "from_resolution": "720p",
                    "to_resolution": "1080p",
                    "bitrate": 9616000,
                    "arguments": [
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v hevc_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:143:format=nv12 -c:v hevc_qsv -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v hevc_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:143:yuv420p -c:v hevc_nvenc -preset p1 -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:143:format=nv12 -c:v hevc_vaapi -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,143)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx265 -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v h264_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:143:yuv420p -c:v h264_nvenc -preset p1 -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:143:format=nv12 -c:v h264_vaapi -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v h264_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:143:format=nv12 -c:v h264_qsv -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,143)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx264 -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                    ],
                },
                {
                    "id": "50568481-5469-6623-3f4a-0b2ac2829f78",
                    "from_resolution": "1080p",
                    "to_resolution": "1080p",
                    "bitrate": 9616000,
                    "arguments": [
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v hevc_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:143:format=nv12 -c:v hevc_qsv -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v hevc_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:143:yuv420p -c:v hevc_nvenc -preset p1 -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:143:format=nv12 -c:v hevc_vaapi -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v hevc -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,143)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx265 -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h265",
                        },
                        {
                            "type": "nvidia",
                            "args": "-init_hw_device cuda=cu:{gpu} -hwaccel cuda -hwaccel_output_format cuda -c:v h264_cuvid -i {video_file} -autoscale 0 -an -sn -vf scale_cuda=-1:143:yuv420p -c:v h264_nvenc -preset p1 -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "amd",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -hwaccel vaapi -hwaccel_output_format vaapi -c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale_vaapi=-1:143:format=nv12 -c:v h264_vaapi -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "intel",
                            "args": "-init_hw_device vaapi=va:/dev/dri/by-path/{gpu}-render -init_hw_device qsv=qs@va -hwaccel qsv -hwaccel_output_format qsv -c:v h264_qsv -i {video_file} -autoscale 0 -an -sn -vf scale_qsv=-1:143:format=nv12 -c:v h264_qsv -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                        {
                            "type": "cpu",
                            "args": "-c:v h264 -i {video_file} -autoscale 0 -an -sn -vf scale=trunc(min(max(iw\\,ih*a)\\,143)/2)*2:trunc(ow/a/2)*2,format=yuv420p -c:v libx264 -preset veryfast -b:v 9616000 -maxrate 9616000 -f null - -benchmark",
                            "codec": "h264",
                        },
                    ],
                },
            ],
        },
    ],
}
