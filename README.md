<h1 align="center">VHoster</h1>
<p align="center">
   Virtual Host Helper for XAMPP Windows<br><br>
   <img align="center" src="preview.gif">
</p>



## Usage


- **Add Host**

   ```
   vhoster add [-h] [--port PORT] name path
   ```

- **Remove Host**

   ```
   vhoster remove [-h] [--port PORT] name
   ```

- **List Hosts**

   ```
   vhoster hosts
   ```

- **Configure Application**

   ```
   vhoster config
   ```

### Arguments

- `name`
  - Virtual host name
- `path`
  - Virtual host root path, relative to XAMPP document root (htdocs)
- `--port`
  - Virtual host port number
- `-h`
  - Help


## Installation

Download the executable and run `vhoster config`


## Configuration

The application will load the settings inside the **vhoster.ini** file (if it exists) at the same directory as the executable.

```ini
[paths]
document_root = C:/Xampp/htdocs
vhosts_conf_path = C:/Xampp/apache/conf/extra/httpd-vhosts.conf
apache_bin = C:/Xampp/apache/bin
hosts_file = C:/Windows/System32/drivers/etc/hosts

[commands]
apache_restart = $APACHE_BIN/httpd -k restart
```


> This application needs **administrative privileges** in order to access the Windows Hosts File


## Building Binaries Using PyInstaller

```
pyinstaller vhoster.py -F -i favicon.ico
```


## Credits

- Icon made by [Pixelmeetup](https://www.flaticon.com/authors/pixelmeetup) from [www.flaticon.com](https://www.flaticon.com/) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)
