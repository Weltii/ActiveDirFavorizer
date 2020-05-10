# ActiveDirFavorizer
## Configuration
Before you can start, you need a "config.json". Currently the ActiveDirFavorizer support MacOs
desktop links and all Linux Filemanager which works with the gtk-3.0 bookmarks. Both need his own configuration. 
You don't need to write it by your own, simply duplicate one of the config_examples, rename it to "config.json", 
adjust the "watch_path" to the path you want to watch and run the "main.py".

## Troubleshooting
`OSError: inotify watch limit reached`: If you get one of these errors, you can simply increase the inotify watches with 
`sudo sysctl fs.inotify.max_user_watches=500000` 
 