import os
import shutil
import time
from pathlib import Path
from datetime import datetime
import schedule

def organize_downloads(source_dir, organized_dir):
    """
    Organize files by extension into categorized folders
    """
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp']
    }
    
    source = Path(source_dir)
    dest = Path(organized_dir)
    
    for file in source.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            moved = False
            
            for category, extensions in categories.items():
                if ext in extensions:
                    category_path = dest / category
                    category_path.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), str(category_path / file.name))
                    print(f"Moved {file.name} to {category}")
                    moved = True
                    break
            
            if not moved:
                other_path = dest / 'Others'
                other_path.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file), str(other_path / file.name))
                print(f"Moved {file.name} to Others")

def backup_files(source_dir, backup_dir):
    """
    Create timestamped backups of important files
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(backup_dir) / f"backup_{timestamp}"
    
    try:
        shutil.copytree(source_dir, backup_path)
        print(f"Backup created successfully at {backup_path}")
        
        # Keep only last 5 backups
        backups = sorted(Path(backup_dir).glob('backup_*'))
        if len(backups) > 5:
            for old_backup in backups[:-5]:
                shutil.rmtree(old_backup)
                print(f"Removed old backup: {old_backup.name}")
    except Exception as e:
        print(f"Backup failed: {e}")


def send_email_report(subject, body, to_email):
    """
    Send automated email reports
    Requires: email configuration
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Configure these with your email settings
    SENDER_EMAIL = "your_email@gmail.com"
    SENDER_PASSWORD = "your_app_password"
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
def check_website_changes(url, output_file):
    """
    Monitor website for changes
    Requires: pip install requests beautifulsoup4
    """
    import requests
    from bs4 import BeautifulSoup
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text()
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                old_content = f.read()
            
            if old_content != content:
                print(f"Website {url} has changed!")
                
        
        with open(output_file, 'w') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error checking website: {e}")
def monitor_disk_space(threshold=80):
    """
    Monitor disk space and alert if usage exceeds threshold
    """
    import psutil
    
    disk = psutil.disk_usage('/')
    percent_used = disk.percent
    
    if percent_used > threshold:
        print(f"⚠️ WARNING: Disk usage at {percent_used}%")
    else:
        print(f"✓ Disk usage OK: {percent_used}%")
    
    return percent_used
def setup_scheduled_tasks():
    """
    Set up automated task scheduling
    Requires: pip install schedule
    """
    schedule.every().day.at("02:00").do(
        backup_files, 
        source_dir="/path/to/important/files",
        backup_dir="/path/to/backups"
    )
    schedule.every().hour.do(
        organize_downloads,
        source_dir=str(Path.home() / "Downloads"),
        organized_dir=str(Path.home() / "Organized")
    )
    schedule.every(30).minutes.do(monitor_disk_space)
    
    print("Scheduled tasks configured. Running...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)
def bulk_rename_files(directory, prefix="", add_date=False):
    """
    Rename multiple files with consistent naming
    """
    path = Path(directory)
    files = sorted([f for f in path.iterdir() if f.is_file()])
    
    for idx, file in enumerate(files, 1):
        ext = file.suffix
        if add_date:
            date_str = datetime.now().strftime('%Y%m%d')
            new_name = f"{prefix}_{date_str}_{idx:03d}{ext}"
        else:
            new_name = f"{prefix}_{idx:03d}{ext}"
        
        new_path = file.parent / new_name
        file.rename(new_path)
        print(f"Renamed: {file.name} -> {new_name}")


if __name__ == "__main__":
    print("Python Task Automation Script")
    print("=" * 50)
    
    print("\nDone!")