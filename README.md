# Web-based File Transfer System

A simple and lightweight file transfer system built with Python that allows you to share files between devices through a web interface. It supports multiple platforms (Windows, macOS, Linux) and handles files with Unicode characters (including Chinese).

## Features

- Web-based interface for easy file upload and download
- Configurable storage directory
- Activity logging
- Cross-platform compatibility
- Unicode filename support
- No external dependencies (uses Python standard library only)

## Requirements

- Python 3.8 or higher

## Quick Start

1. Download all the files to a directory:
   - `web_file_server.py`
   - `template.html`
   - `config.txt`
   - `log.txt`

2. Run the server:
   ```bash
   python web_file_server.py
   ```

3. Open your web browser and go to:
   ```
   http://localhost:8000
   ```

## Configuration

### Storage Directory

You can change the storage location by editing `config.txt`:

1. Open `config.txt`
2. Modify the `STORAGE_PATH` value to your desired directory path
   ```
   STORAGE_PATH=your/preferred/path
   ```

Example configurations:
- Windows: `STORAGE_PATH=C:\Users\YourName\Documents\FileTransfer`
- macOS/Linux: `STORAGE_PATH=/home/username/FileTransfer`

### Port Number

To change the default port (8000):

1. Open `web_file_server.py`
2. Modify the port number in the last line:
   ```python
   if __name__ == '__main__':
       run_server(port=your_preferred_port)
   ```

## Accessing from Other Devices

To access the file transfer system from other devices on the same network:

1. Find the server's IP address:
   - Windows: Run `ipconfig` in Command Prompt
   - macOS/Linux: Run `ifconfig` or `ip addr` in Terminal

2. On other devices, open a web browser and go to:
   ```
   http://[server-ip]:8000
   ```
   Replace `[server-ip]` with the actual IP address of the server

## File Operations

### Uploading Files

1. Click the "Choose File" button
2. Select the file you want to upload
3. Click the "Upload" button

### Downloading Files

1. Find the file in the "Available Files" list
2. Click the "Download" button next to the file

## Activity Logging

All file transfers are logged in `log.txt` with the following information:
- Timestamp
- Activity type (UPLOAD/DOWNLOAD)
- Filename
- Client IP address

Recent activities are also displayed at the bottom of the web interface.

## Security Considerations

This is a basic file transfer system designed for use on trusted local networks. When using this system:

1. Be cautious when exposing the server to the internet
2. Consider adding authentication if needed
3. Be aware that files are transferred without encryption
4. Ensure proper file permissions on the storage directory

## Troubleshooting

1. **Port Already in Use**
   ```bash
   OSError: [Errno 98] Address already in use
   ```
   Solution: Change the port number or close the application using the current port

2. **Permission Denied**
   ```bash
   PermissionError: [Errno 13] Permission denied
   ```
   Solution: Ensure you have write permissions for the storage directory

3. **Unicode Filename Issues**
   - Ensure your system's locale supports Unicode
   - Check that the files are being saved with UTF-8 encoding

## File Structure

- `web_file_server.py`: The main server script
- `template.html`: The HTML template for the web interface
- `config.txt`: Configuration file for the storage directory and port number
- `log.txt`: Activity log file
