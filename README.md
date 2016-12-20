# pypic

*Take video with a Raspberry Pi and upload it to cloud storage*

## Installation

 1. `$ git clone https://github.com/tstringer/pypic.git`
 2. `$ cd pypic`
 3. `$ sudo pip3 install .`

:bulb: **Note**: for cloud storage (benefits? Offsite and redundant storage) you must define the environment variables `AZSTORAGE_ACCOUNT_NAME` and `AZSTORAGE_ACCOUNT_KEY`. A common approach is to put these in `~/.bashrc` as exports, or if you are going to run this on startup with cron put them in `~/.profile` as exports and the cron job would read `@reboot . $HOME/.profile && /path/to/pypic -c -d 60 &`

## Hardware

This has been tested on a `Raspberry Pi 2 Model B` and with a `Raspberry Pi Camera` (Rev 1.3)

## Usage

```
# list help
$ pypic -h

# capture a continuous loop of video for 10 seconds (default)
$ pypic -c

# capture a 60 second video
$ pypic -d 60

# continuously capture 5 minutes videos
$ pypic -c -d 300
```

## Run on startup

It might be a common request to run `pypic` on startup of a device like a Raspberry Pi (tested with RPi).

 1. Run `crontab -e`
 2. Add the following to the end `@reboot /path/to/pypic -c -d 60 &` (find the path by running `which pypic`)
 3. Save and exit the crontab editor
 4. (Optional) Reboot the device

## Future

 - Rolling storage (at least locally and configurable, as it is running continuously will fill storage)
 - Cache for uploading (in the case that there is no internet connection to upload to cloud storage, cache the cloud upload operations until connected)
 - Support other cloud storage providers (currently only supports Azure Blob Storage)
