<h1 align="center">VHoster</h1>
<p align="center">Virtual Host Helper for XAMPP Windows</p>


## Usage

```
Usage: vhoster [OPTIONS] COMMAND [ARGS]...

  Apache Virtual Host Manager

Options:
  --path PATH  Path to registered site
  --version    Show application version
  --help       Show this message and exit.

Commands:
  forget (remove)  Unregister the current (or specified) PATH or DOMAIN
  link             Link the current working directory to given DOMAIN
  list (all)       List all registered sites
  park (create)    Register the current (or specified) PATH to given DOMAIN
  restart          Restart Apache server
  secure           Secure the current (or specified) PATH or DOMAIN with a...
  set-root         Set specified PATH as document root for current site or...
  setup            Configure Vhoster
  show (info)      Find site by DOMAIN or PATH and display its information
  unsecure         Remove trusted TLS certificate from the current (or...
```


## Installation

### As Python Module

- Clone this repository, or download as ZIP

    ```
    git clone https://github.com/GerardBalaoro/VHoster.git
    ```

- Install using PIP

    ```
    pip install -U -r requirements.txt
    pip install -U .
    ```

### Build Executable Using PyInstaller

    ```
    pip install -U pyinstaller
    py build.py
    ```


## Configuration

The application will load the settings inside the **config.json** file in the user app data directory.

```json
{
    // Default TLD
    "tld": "test",
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
    "sites": [
        {
            "domain": "localhost",
            // Working directory
            "path": "C:/Xampp/htdocs",
            // Document root (if different from path)
            "root": "",
            "secure": true,
            // Override default TLD
            "tld": ""
        }
    ]
```

> This application needs **administrative privileges** in order to access the Windows Hosts File


## Credits

- Icon made by [bqlqn](https://www.flaticon.com/authors/bqlqn) from [www.flaticon.com](https://www.flaticon.com/) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)