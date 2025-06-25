# Guide to Upload Multi-Format Downloader to a Shared Web Host

This guide will help you upload and set up the Multi-Format Downloader on your shared web hosting account.

## Method 1: Using FTP/SFTP

### Prerequisites
- FTP/SFTP credentials from your hosting provider
- An FTP client (FileZilla, Cyberduck, WinSCP, etc.)

### Steps

1. **Gather your FTP credentials**
   - Hostname/Server: (e.g., ftp.yourdomain.com)
   - Username: (provided by your host)
   - Password: (provided by your host)
   - Port: 21 for FTP, 22 for SFTP (may vary)

2. **Connect to your server**
   - Open your FTP client
   - Enter your credentials and connect
   - Navigate to the appropriate directory (often public_html, www, or htdocs)

3. **Upload the files**
   - Upload all files and folders from the Ytytyt directory
   - Ensure you maintain the directory structure
   - Make sure to set the correct permissions:
     - Files: 644 (rw-r--r--)
     - Directories: 755 (rwxr-xr-x)
     - Executable scripts: 755 (rwxr-xr-x)

## Method 2: Using cPanel File Manager

If your host provides cPanel:

1. **Log in to cPanel**
   - Go to yourdomain.com/cpanel
   - Enter your username and password

2. **Open File Manager**
   - Navigate to the public_html directory

3. **Upload files**
   - Click "Upload" and select all files from your local Ytytyt directory
   - Or create a ZIP archive of your files, upload it, and extract on the server

4. **Set permissions**
   - Right-click on files/folders and select "Change Permissions"
   - Set as recommended above

## Method 3: Using Git

If your host supports Git:

1. **SSH into your server**
   ```
   ssh username@yourdomain.com
   ```

2. **Navigate to your web directory**
   ```
   cd public_html
   ```

3. **Clone the repository**
   ```
   git clone https://github.com/djb3232/Ytytyt.git
   ```

4. **Set up the application**
   ```
   cd Ytytyt
   chmod +x install.sh
   ./install.sh
   ```

## Setting Up the Web Application

After uploading the files:

1. **Install Python and dependencies**
   - Many shared hosts have Python pre-installed
   - If you have SSH access, run:
     ```
     python3 -m pip install -r requirements.txt
     ```
   - If not, contact your hosting provider for assistance

2. **Configure for your host**
   - Most shared hosts require specific configurations for web applications
   - Common options include:
     - CGI/FastCGI
     - WSGI with Apache or Nginx
     - Passenger

3. **Create a WSGI configuration file**
   Create a file named `wsgi.py` in your Ytytyt directory:

   ```python
   import sys
   import os

   # Add the directory containing your app to the Python path
   sys.path.insert(0, os.path.dirname(__file__))

   # Import your app
   from web_downloader import app as application
   ```

4. **Set up a virtual environment** (if supported)
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Shared Hosting-Specific Configurations

### For cPanel with Python Selector
If your host uses cPanel with Python Selector:

1. Create a `.htaccess` file in your application directory:
   ```
   AddHandler fcgid-script .fcgi
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$ app.fcgi/$1 [QSA,L]
   ```

2. Create an `app.fcgi` file:
   ```python
   #!/usr/bin/python3
   import sys
   import os
   from flup.server.fcgi import WSGIServer

   # Add the directory containing your app to the Python path
   sys.path.insert(0, os.path.dirname(__file__))

   # Import your app
   from web_downloader import app

   if __name__ == '__main__':
       WSGIServer(app).run()
   ```

3. Make it executable:
   ```
   chmod +x app.fcgi
   ```

### For Passenger
If your host uses Passenger:

1. Create a `passenger_wsgi.py` file:
   ```python
   import sys
   import os

   INTERP = os.path.join(os.getcwd(), 'venv', 'bin', 'python')
   if sys.executable != INTERP:
       os.execl(INTERP, INTERP, *sys.argv)

   sys.path.insert(0, os.path.dirname(__file__))
   from web_downloader import app as application
   ```

## Troubleshooting

- **500 Internal Server Error**: Check your server logs for details
- **Permission Issues**: Ensure scripts are executable (chmod +x)
- **Module Not Found**: Make sure all dependencies are installed
- **Port Binding Issues**: Most shared hosts don't allow binding to ports directly; use their provided methods instead

## Contact Your Host

If you encounter issues, contact your hosting provider's support. They can provide specific instructions for running Python web applications on their platform.