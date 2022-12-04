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
 

## TODO for version 1.0

- executable without pyenv
  - [x] linux gtk3 based
  - [ ] ~~macOS based~~
- [ ] user service configuration
- [ ] dbus interface to control externally 