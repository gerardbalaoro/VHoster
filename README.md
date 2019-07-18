<h1 align="center">VHoster</h1>
<p align="center">Virtual Host Helper for XAMPP Windows</p>


## Usage


- **Create Host**

   ```
   vhoster create [-h] [-p PORT] name path
   ```

- **Create Host**

   ```
   vhoster delete [-h] name
   ```

### Arguments

- `name`
  - Virtual host name
- `path`
  - Virtual host root path, relative to XAMPP document root (htdocs)
- `port` (optional)
  - Virtual host port number


## Configuration

The application will load the settings inside the **config.json** file in the user app data directory.

```json
{
    "tld": "test",
    "dns": {
        "file": "C:/Windows/System32/drivers/etc/hosts"
    },
    "apache": {
        "bin": "C:/DevApps/Xampp/apache/bin/httpd.exe",
        "conf": "C:/DevApps/Xampp/apache/conf/extra/httpd-vhosts.conf"
    },
    "collection": [],
    "sites": []
}
```

> This application needs **administrative privileges** in order to access the Windows Hosts File


## Credits

- Icon made by [Pixelmeetup](https://www.flaticon.com/authors/pixelmeetup) from [www.flaticon.com](https://www.flaticon.com/) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)
