# pyTAB

Python Transcoding Acceleration Benchmark

## Testing guide for [pyTAB](https://github.com/BotBlake/pytab)

_pyTAB is in heavy development a.t.m. so expect it to be laggy and crash._
_Since it is a Hardware Benchmark, it will try to use as many System Ressources as possible!_

### Software requirements

Also pyTAB is build as a python module via poetry. Therefore you need to have at least python 3.11.2 and poetry installed on your system.
poetry is installed via pipx using: `pipx install poetry`
If you do not have pipx installed, follow the [official install guide](https://pipx.pypa.io/stable/installation/)

Its also required to have access to a running instance of Venson's [Jellyfin Hardware Visualizer](https://github.com/JPVenson/Jellyfin.HardwareVisualizer). More information about that is available in the GitHub repo.

### installing pyTAB

1. Clone the GitHub Repository `git clone https://github.com/BotBlake/pyTAB`
2. Go into the pytab Folder `cd pytab`
3. Switch to the development branch `git switch develop`
4. Open the venv shell `poetry shell`
5. Install Dependencies `poetry install`  
_(To exit the Shell: `exit`)_

Since the state of the software often Changes, you might have to do some "additional steps" to ensure its running correctly. They are explained down below.

### running pyTAB

1. open the poetry shell `poetry shell`
2. run the script `pytab --server "https://Your/Test/Server/"`
_If you want / need specific info about all the CLI Arguments, do `pytab -h`_

(If you do not care about the actual test results, you can use the developer mode through `--debug` and specify a local file Path instead of a Server URL.)

### additional Steps

_During development pyTAB may require you to set up specific things manually these will change over Time_

- Make sure you are on the latest version `git pull`
- Take a Look into the "Current Issues" section

## Current Issues

### OS Support

_Since a lot of Hardware recognition is not yet implemented for Linux based Systems, these are currently not supported. Try running the Script on Windows instead._

- Use Windows 🗿

### Software Limits

_To reduce Test Runtime (and because proper support isnt yet implemented, there are a few limitations on what devices pyTAB uses at the moment)_

- Only NVIDIA GPUs supported
- CPU Tests _(can be disabled manually)_
- No full Support for AMD / Intel GPU's yet _(may work when enabled manually)_
- Script will always use the first GPU that it can find
