# Architecture
![Architecture schema](architecture.svg "MiniRadio Architecture")

MiniRadio requires a functional and properly configured MPD server with access to your MP3 file library and your playlists.

It uses 2 pythons modules :
* API framework Bottle : https://bottlepy.org/docs/dev/
* Python client library for MPD : https://pypi.org/project/python-mpd2/

# Using Miniradio

## Installation
* Create your MiniRadio folder
`mkdir <your path>/MiniRadio`

* Copy MiniRadio application sources folder `miniradio_app` in created folder `<your path>/MiniRadio`


* Create virtual environnement
`python3 -m venv <your path>/MiniRadio/venv`
`source <your path>/MiniRadio/venv/bin/activate`

* Install dependences
`pip install bottle`
`pip install python-mpd2`

* Create launcher script `start_miniradio.sh` in `<your path>/MiniRadio`

* Insert following code in `start_miniradio.sh`
```
#!/bin/bash
source $(dirname $(readlink -f $0))/venv/bin/activate
python3 $(dirname $(readlink -f $0))/miniradio_app/application.py
```

* Save and make script executable : `chmod 755 start_miniradio.sh`

## Configuration


## Manual execution
Launch your script `start_miniradio.sh`.
Ctrl+C for stop execution.

## Execution at boot
* Create service file `miniradio-webserver.service` in `/etc/systemd/system`
* Insert flowing code in service file
```
[Unit]
Description=MiniRadio webserver

[Service]
Type=simple
ExecStart=<your path>/MiniRadio/start_miniradio.sh
Restart=on-failure
User=<your user>

[Install]
WantedBy=multi-user.target
```
Replace `<your path>` and `<your user>` with your installation path and your execution user (never use root).

* Validate the unit file before loading it.
`sudo systemd-analyze verify /etc/systemd/system/miniradio-webserver.service`

* Reload the service manager so it reads the new unit file.
`sudo systemctl daemon-reload`

* Enable the service for future boots and start it in the current boot.
`sudo systemctl enable --now miniradio-webserver.service`

* To check service
`sudo systemctl status miniradio-webserver.service`
