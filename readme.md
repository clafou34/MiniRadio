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
```
python3 -m venv <your path>/MiniRadio/venv
source <your path>/MiniRadio/venv/bin/activate
```

* Install dependences
```
pip install bottle
pip install python-mpd2
pip install gunicorn
```


* Create launcher script `start_miniradio.sh` in `<your path>/MiniRadio`

* Insert following code in `start_miniradio.sh`
```
#!/bin/bash
source $(dirname $(readlink -f $0))/venv/bin/activate
python3 $(dirname $(readlink -f $0))/miniradio_app/application.py
```

* Save and make script executable : `chmod 755 start_miniradio.sh`

## Configuration
The configuration of MiniRadio is found in the file `radioui.conf`, which is by default located in the `configuration` directory of the application's sources.
Example :
```
[global]
run-mode = DEBUG
listening-host = 0.0.0.0
listening-port = 6809
listening-https-keyfile = 
listening-https-certfile =

[mpd.connexion]
mpd-address = localhost
mpd-port = 6600

[web.client]
use-web-client = True
```

* `run-mode` can have 2 values : `DEBUG` for maximum information in standard error output, or `NORMAL` for minimization of output. Default is `NORMAL`.
* `listening-host` : This is IP address for listening HTTP/HTTPS request (default : 0.0.0.0 ==> for listening on all IP interfaces of host).
* `listening-port` : This is port use by MiniRadio for listening HTTP requests (default : 6809)
* `listening-https-keyfile` : If you want the application to be secured by HTTPS, then enter the path to the file containing the private key in this option. By default, this option is empty, which causes the application to start without HTTPS.
* `listening-https-certfile` : If you want the application to be secured by HTTPS, then enter the path to the file containing the certificate in this option. By default, this option is empty, which causes the application to start without HTTPS.
* `mpd-address` : This is the adress (IP or domain name) where MPD listen. For connexion by socket on same host, you can put node name of abstract socket (ex : `/run/mpd/socket`). Default is 'localhost'.
* `mpd-port` : Port on which MPD listen. Default is 6600.
* `use-web-client` : Allow to activate web UI (value `True`) or inactivate it (value `False`). Default is `False`.

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

## Access to MiniRadio

The homepage is accessible at the address `http://<your-server-address>:<listening-port>/`.

API is accessible at `http://<your-server-address>:<listening-port>/api/`.

Web UI is accessible at `http://<your-server-address:listening-port>/webclient/`.

Example : [http://localhost:6809/](http://localhost:6809/)