# pyTAB

pyTAB (Python Transcoding Acceleration Benchmark) is a benchmarking tool designed to measure the performance of hardware when handling simultaneous ffmpeg transcoding processes. This tool tests how many parallel ffmpeg transcoding processes a system can manage, providing detailed insights into hardware performance.

The benchmark results can be uploaded to the central Jellyfin Hardware Survey Server, allowing users to compare their hardware's performance with other systems. This facilitates easy visualization of the results and serves as a valuable resource for Jellyfin users looking to optimize their transcoding capabilities.

## [pyTAB](https://github.com/BotBlake/pytab) QuickStart Guide
Warnings:
> This is an Alpha Version of the Client.
It has not been properly tested, nor implemented for all Platforms yet!
Use at your own risk.

> This hardware benchmark will use all system ressources available.

> The Benchmark will take multiple hours to finish. Make sure to run it, when the system is not used.

### Software Requirements

pyTAB is build as a python module via poetry. Therefore you need to have at least python 3.11.2 and poetry installed on your system.
poetry is installed via pipx using: `pipx install poetry`
If you do not have pipx installed, follow the [official install guide](https://pipx.pypa.io/stable/installation/)

Its also required to have access to a running instance of Venson's [Jellyfin Hardware Visualizer](https://github.com/JPVenson/Jellyfin.HardwareVisualizer). More information about that is available in the GitHub repo.

### Installing pyTAB

1. Clone the GitHub Repository `git clone https://github.com/BotBlake/pyTAB`
2. Go into the pytab Folder `cd pytab`
3. Switch to the development branch `git switch develop`
4. Open the venv shell `poetry shell`
5. Install Dependencies `poetry install`  
_(To exit the Shell: `exit`)_

Since the state of the software often Changes, you might have to do some "additional steps" to ensure its running correctly. They are explained down below in the [additional Steps](https://github.com/BotBlake/pytab?tab=readme-ov-file#additional-steps) section.

### Running pyTAB

1. open the poetry shell `poetry shell`
2. run the script `pytab`
> By default this will use the official Jellyfin Hardware Survey Server https://hwa.jellyfin.org/. If you want to run from a custom Server, use the `--server {url}` option

_If you want / need specific info about all the CLI Arguments, run `pytab -h`_

### Hardware Control

_To reduce Test Runtime you can disable certain hardware reducing the number of tests you run._

- CPU based tests can be disabled using the `--nocpu` flag
- GPU based tests can be disabled using the `--gpu 0` option or by selecting 0 in the interactive GPU selector
- If the CPU and GPU are disabled the program will error out saying "ERROR: All Hardware Disabled"

### Path specification
Since the Script downloads ffmpeg AND video files, you have the option to specify a Path for both.
If the files are already existing there, they will not be redownloaded.

- Path to video directory via `--videos {path}`
- Path to ffmpeg portable directory via `--ffmpeg {path}`

### Additional Steps

_During development pyTAB may require you to set up specific things manually these will change over Time_

- Make sure you are on the latest version `git pull`
- Take a Look into the "Current Issues" section

## Current Issues
You will find a List of currently known issues below.
These will change over time, so please ensure you check this section regularly for any changes.

### NvEnc Driver Limit
NVIDIA Limits their consumer grade GPU's maximum NvEnc Streams through the driver. Currently this leads to a super long runtime on NvEnc limited devices.

If you do use a NVIDIA consumer grade Graphics Card and have not done anything to circumvent the limit, its currently recommended to not Test on that device.

