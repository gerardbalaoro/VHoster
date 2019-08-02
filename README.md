<h1 align="center">VHoster</h1>
<p align="center">
    Apache Virtual Host Manager<br><br>
    <img align="center" src="docs/preview.gif">
</p>



## Usage

```
Usage: vhoster [OPTIONS] COMMAND [ARGS]...

  Apache Virtual Host Manager

  https://github.com/GerardBalaoro/VHoster
  Copyright (c) Gerard Balaoro

Options:
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  config           Manage configuration variables
  explore          Browse current site path or site registered to DOMAIN
  forget (remove)  Unregister the current (or specified) PATH or DOMAIN
  link             Link current working directory to domain
  list             List all registered sites
  open             Open current site or site registered to DOMAIN in browser
  park (create)    Register the current (or specified) PATH to given DOMAIN
  rebuild          Rebuild all site configuration files
  refresh          Refresh configuration files of the site
  secure           Secure the site with a trusted TLS certificate
  set-root         Set document root for the site
  share            Generable public url for the site
  show             Display site information
  start            Restart all or specified services
  stop             Stop all or specified services
```


## Installation

```
pip install git+https://github.com/GerardBalaoro/VHoster#egg=VHoster
```

### Build Executable Using PyInstaller

    pip install -U pyinstaller
    py build.py


## Configuration

The application will load the settings inside the **config.json** file in the user app data directory.

```jsonc
{
    "dns": {
        // Path to HOSTS File
        "file": "C:/Windows/System32/drivers/etc/hosts"
    },
    "apache": {
        // Path to Apache Executable
        "bin": "C:/Xampp/apache/bin/httpd.exe",
        // Path to Apache Configuration File
        "conf": "C:/Xampp/apache/conf/extra/httpd-vhosts.conf"
    },
    "paths": {
        // Where to store individual *.conf files
        "conf": "C:/Xampp/apache/sites/conf",
        // Where to store generated certificates and keys
        "certs": "C:/Xampp/apache/sites/certs"
    },
    "ngrok": {
        // Path to ngrok configuration file
        "config": "%USERPROFILE%/.ngrok2/ngrok.yml"
    },
    "sites": [
        {
            "domain": "localhost.test",
            // Working directory
            "path": "C:/Xampp/htdocs/",
            // Document root (if different from path)
            "root": "",
            "secure": true,
            // Override default TLD
        }
    ]
```

> This application needs **administrative privileges** in order to access the Windows Hosts File


## Credits

- Icon made by [bqlqn](https://www.flaticon.com/authors/bqlqn) from [www.flaticon.com](https://www.flaticon.com/) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)
