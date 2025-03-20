import psutil
import time
import smtplib
import json
from datetime import datetime
import logging

class SystemMonitor:
    def __init__(self, config_path='monitor_config.json'):
        self.config = self.load_config(config_path)
        self.setup_logging()
        
    def load_config(self, path):
        """Load configuration from JSON file"""
        with open(path, 'r') as f:
            return json.load(f)
            
    def setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            filename='system_monitor.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def check_cpu_usage(self):
        """Monitor CPU usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > self.config['cpu_threshold']:
            self.send_alert(f"High CPU usage: {cpu_percent}%")
            logging.warning(f"High CPU usage detected: {cpu_percent}%")
        return cpu_percent
        
    def check_memory_usage(self):
        """Monitor memory usage"""
        memory = psutil.virtual_memory()
        if memory.percent > self.config['memory_threshold']:
            self.send_alert(f"High memory usage: {memory.percent}%")
            logging.warning(f"High memory usage detected: {memory.percent}%")
        return memory.percent
        
    def check_disk_usage(self, path="/"):
        """Monitor disk usage"""
        disk = psutil.disk_usage(path)
        if disk.percent > self.config['disk_threshold']:
            self.send_alert(f"High disk usage: {disk.percent}%")
            logging.warning(f"High disk usage detected: {disk.percent}%")
        return disk.percent
        
    def send_alert(self, message):
        """Send email alert"""
        if self.config['email_enabled']:
            try:
                server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
                server.starttls()
                server.login(self.config['smtp_user'], self.config['smtp_password'])
                server.sendmail(
                    self.config['from_email'],
                    self.config['to_email'],
                    f"Subject: System Alert\n\n{message}"
                )
                server.quit()
                logging.info(f"Alert sent: {message}")
            except Exception as e:
                logging.error(f"Failed to send alert: {str(e)}")
                
    def run_monitor(self):
        """Main monitoring loop"""
        while True:
            try:
                cpu = self.check_cpu_usage()
                memory = self.check_memory_usage()
                disk = self.check_disk_usage()
                
                logging.info(f"System status - CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%")
                
                time.sleep(self.config['check_interval'])
                
            except Exception as e:
                logging.error(f"Monitoring error: {str(e)}")
                time.sleep(self.config['error_retry_interval'])

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.run_monitor()