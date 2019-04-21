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


## Installation

Copy the executable inside the root of the XAMPP installation folder.


## Configuration

The application will load the settings inside the **vhoster.json** file (if it exists) at the same directory as the executable.

```json
{
   "XAMPP_DIR": "C:\\Xampp\\",
   "DOCUMENT_ROOT": "C:\\Xampp\\htdocs\\"
}
```


> This application needs **administrative privileges** in order to access the Windows Hosts File


## Building Binaries Using PyInstaller

```
pyinstaller vhoster.py -F -i favicon.ico
```


## Credits

- Icon made by [Pixelmeetup](https://www.flaticon.com/authors/pixelmeetup) from [www.flaticon.com](https://www.flaticon.com/) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)
