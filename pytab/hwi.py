#!/usr/bin/env python3

# pytab.hwi.py
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
import platform

def MatchID(platforms: list, dummy_id: str) -> str:
    for element in platforms:
        if platform.system().lower() == element["type"].lower():
            return element["id"]
    return None

def get_os_info():
    required = ["pretty_name", "name", "version_id", "version", "version_codename", "id", "home_url", "support_url", "bug_report_url"]
    os_element = dict()

    # Getting system name, release and version
    os_element['name'] = platform.system()
    os_element['version'] = platform.version()
    os_element['version_id'] = platform.release()
    
    # Filling all possible values
    if os_element['name'] == 'Linux':
        try:
            with open('/etc/os-release') as f:
                for line in f:
                    key, value = line.strip().split('=', 1)
                    value = value.strip('"')
                    print(f"Key: {key} -- Value: {value}")
                    if key.lower() in required:
                        os_element[key.lower()] = value
        except FileNotFoundError:
            os_element['pretty_name'] = "Linux (Unknown Distro)"
            os_element['id'] = "linux"
    
    elif os_element['name'] == 'Windows':
        os_element['pretty_name'] = platform.system() + " " + platform.release()
        os_element['id'] = "windows"
        os_element['home_url'] = "https://www.microsoft.com/windows"
        os_element['support_url'] = "https://support.microsoft.com"
        os_element['bug_report_url'] = "https://support.microsoft.com/contactus/"

    return os_element