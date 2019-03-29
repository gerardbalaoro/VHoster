<h1 align="center">VHoster</h1>
<p align="center">Virtual Host Helper for XAMPP Windows</p>


## Binaries

- **mkvhost**
  - create new virtual host
 
- **rmvhost**
  - delete virtual host


## Configuration

The application uses configuration inside the **config.json** file, which is created whenever it is initialized.

```json
{
   "XAMPP_DIR": "C:\\Xampp\\",
   "DOCUMENT_ROOT": "C:\\Xampp\\htdocs\\"
}
```


> This application needs **administrative privileges** in order to access the Windows Hosts File


## Building Binaries Using PyInstaller

- Intall PyInstaller

  ```
  pip install pyinstaller
  ```
  
- Create Binaries

  ```
  pyinstaller mkvhost.py -F -i favicon.ico
  pyinstaller rmvhost.py -F -i favicon.ico
  ```


## Credits

- Icon made by [Pixelmeetup](https://www.flaticon.com/authors/pixelmeetup) from [www.flaticon.com](https://www.flaticon.com/) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)
