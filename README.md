# ActiveDirFavorizer

## How to start

1. `pyenv virtualenv 3.10 <env name>`
2. `pyenv local <env name>`
3. `make install`
4. follow the instructions under #configuration
5. `make start`

## Configuration
Before you can start, you need a "config.json". Currently, the ActiveDirFavorizer support macOS
desktop links and all Linux Filemanager which works with the gtk-3.0 bookmarks. Both need his own configuration. 
You don't need to write it by your own, simply duplicate one of the config_examples, rename it to "config.json", 
adjust the "watch_path" to the path you want to watch and run the "main.py".

## Troubleshooting
`OSError: inotify watch limit reached`: If you get one of these errors, you can simply increase the inotify watches with 
`sudo sysctl fs.inotify.max_user_watches=500000` 

## Install as systemd service

1. build the active dir favorizer via `make build_linux`
2. copy the dist directory `sudo cp -r dist/gtk3-linux-main /usr/bin/active-dir-favorizer`
3. copy `cp build_executable_specific/linux/active_dir_favorizer.service ~/.config/systemd/user`
4. copy `cp config.json ~/.config/active-dir-favorizer/`
5. reload the systemd daemon with `systemctl --user daemon-reload`
6. start or enable the service via `systemctl --user (start|enable) active-dir-favorizer.service`

## TODO for version 1.0

- executable without pyenv
  - [x] linux gtk3 based
  - [ ] macOS based
- [x] systemd user service configuration
- [x] add logging via stdout to ensure that loggings is possible via systemd service
- [ ] dbus interface to control externally