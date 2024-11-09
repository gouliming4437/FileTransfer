import http.server
import socketserver
import os
from pathlib import Path
import cgi
import html
import urllib.parse
from datetime import datetime

def log_activity(activity_type, filename, ip_address):
    """Log file transfer activities with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} | {activity_type} | {filename} | {ip_address}\n"
    
    try:
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log: {e}")

def load_config():
    config = {'STORAGE_PATH': 'downloads'}  # default value
    try:
        with open('config.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        # Create default config file if it doesn't exist
        with open('config.txt', 'w') as f:
            f.write("# Directory path for storing files\n")
            f.write("# Examples:\n")
            f.write("# Windows: C:\\Users\\YourName\\Documents\\FileTransfer\n")
            f.write("# Mac/Linux: /home/username/FileTransfer\n")
            f.write("STORAGE_PATH=downloads\n")
    
    # Create storage directory if it doesn't exist
    storage_path = Path(config['STORAGE_PATH'])
    storage_path.mkdir(parents=True, exist_ok=True)
    return config

def get_recent_logs(max_entries=10):
    try:
        with open('log.txt', 'r', encoding='utf-8') as f:
            # Skip header lines
            next(f)  # Skip column headers
            next(f)  # Skip separator line
            
            # Get last max_entries lines
            lines = list(f)[-max_entries:]
            
            logs_html = ''
            for line in lines:
                timestamp, activity, filename, ip = [html.escape(x.strip()) for x in line.split('|')]
                logs_html += f'<tr><td>{timestamp}</td><td>{activity}</td>'
                logs_html += f'<td>{filename}</td><td>{ip}</td></tr>'
            
            return logs_html
    except FileNotFoundError:
        return ''

class FileTransferHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.config = load_config()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Get list of files in storage directory
            storage_path = Path(self.config['STORAGE_PATH'])
            files = os.listdir(storage_path)
            
            # Create file list HTML
            files_html = ''
            for file in files:
                file_path = os.path.join(storage_path, file)
                file_size = os.path.getsize(file_path)
                safe_filename = urllib.parse.quote(file)
                files_html += f'<tr><td>{html.escape(file)}</td>'
                files_html += f'<td>{file_size:,} bytes</td>'
                files_html += f'<td><a href="/download/{safe_filename}" class="button">Download</a></td></tr>'
            
            # Add storage path information to the template
            storage_info = f'<p>Storage Directory: {html.escape(str(storage_path.absolute()))}</p>'
            
            # Add recent logs to the template
            recent_logs = get_recent_logs()
            
            # Send HTML response
            with open('template.html', 'r', encoding='utf-8') as f:
                template = f.read()
                template = template.replace('{{FILES}}', files_html)
                template = template.replace('{{STORAGE_INFO}}', storage_info)
                template = template.replace('{{RECENT_LOGS}}', recent_logs)
                self.wfile.write(template.encode('utf-8'))
                
        elif self.path.startswith('/download/'):
            file_name = urllib.parse.unquote(self.path[10:])
            file_path = os.path.join(self.config['STORAGE_PATH'], file_name)
            
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Log download activity
                client_address = self.client_address[0]
                log_activity("DOWNLOAD", file_name, client_address)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                encoded_filename = urllib.parse.quote(file_name.encode('utf-8'))
                self.send_header('Content-Disposition', 
                               f"attachment; filename*=UTF-8''{encoded_filename}")
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        if self.path == '/upload':
            content_type = self.headers['Content-Type']
            
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type,
                    'CONTENT_LENGTH': self.headers['Content-Length'],
                }
            )
            
            if 'file' in form:
                fileitem = form['file']
                if fileitem.filename:
                    filename = os.path.basename(fileitem.filename)
                    if isinstance(filename, bytes):
                        filename = filename.decode('utf-8')
                    
                    filepath = os.path.join(self.config['STORAGE_PATH'], filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(fileitem.file.read())
                    
                    # Log upload activity
                    client_address = self.client_address[0]
                    log_activity("UPLOAD", filename, client_address)
                    
                    self.send_response(303)
                    self.send_header('Location', '/')
                    self.end_headers()
                    return
            
            self.send_error(400, "No file was uploaded")

def run_server(port=8000):
    # Create log file if it doesn't exist
    if not os.path.exists('log.txt'):
        with open('log.txt', 'w', encoding='utf-8') as f:
            f.write("Timestamp | Activity | Filename | IP Address\n")
            f.write("-" * 50 + "\n")

    with socketserver.TCPServer(("", port), FileTransferHandler) as httpd:
        config = load_config()
        print(f"Serving at http://localhost:{port}")
        print(f"Storage directory: {Path(config['STORAGE_PATH']).absolute()}")
        print(f"Log file: {Path('log.txt').absolute()}")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server() 