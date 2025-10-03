#!/usr/bin/env python3
import rumps
import random
import datetime
import json
import os
from pathlib import Path
from AppKit import NSSound, NSImage
import threading
import time

class MindBellApp(rumps.App):
    def __init__(self):
        # Load icon
        icon_path = os.path.join(os.path.dirname(__file__), 'media', 'icon.png')
        super(MindBellApp, self).__init__("", quit_button=None)
        
        # Set up the icon
        if os.path.exists(icon_path):
            self.icon = icon_path
        else:
            self.icon = "🔔"
        
        # Configuration
        self.config_file = Path.home() / '.mindbell_config.json'
        self.load_config()
        
        # State
        self.enabled = False
        self.next_bell_time = None
        self.timer_thread = None
        self.running = True
        
        # Menu items
        self.toggle_item = rumps.MenuItem("Start Bell", callback=self.toggle_bell)
        self.interval_menu = rumps.MenuItem("Interval Range")
        self.active_hours_menu = rumps.MenuItem("Active Hours")
        self.sound_menu = rumps.MenuItem("Bell Sound")
        self.next_bell_item = rumps.MenuItem("Next Bell: Not scheduled")
        
        # Build interval submenu
        self.build_interval_menu()
        
        # Build active hours submenu
        self.build_active_hours_menu()
        
        # Build sound selection submenu
        self.build_sound_menu()
        
        # Build main menu
        self.menu = [
            self.toggle_item,
            rumps.separator,
            self.next_bell_item,
            rumps.separator,
            self.interval_menu,
            self.active_hours_menu,
            self.sound_menu,
            rumps.separator,
            rumps.MenuItem("Test Bell", callback=self.test_bell),
            rumps.separator,
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
        
        # Start timer thread
        self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        self.timer_thread.start()
    
    def load_config(self):
        """Load configuration from file or use defaults"""
        defaults = {
            'min_interval': 15,  # minutes
            'max_interval': 45,  # minutes
            'start_hour': 9,
            'end_hour': 22,
            'sound': 'Glass'
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.config = {**defaults, **config}
            except:
                self.config = defaults
        else:
            self.config = defaults
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def build_interval_menu(self):
        """Build the interval range submenu"""
        intervals = [
            ("5-15 minutes", 5, 15),
            ("10-20 minutes", 10, 20),
            ("15-30 minutes", 15, 30),
            ("15-45 minutes", 15, 45),
            ("30-60 minutes", 30, 60),
            ("45-90 minutes", 45, 90),
            ("60-120 minutes", 60, 120),
        ]
        
        for label, min_val, max_val in intervals:
            item = rumps.MenuItem(
                label,
                callback=lambda sender, min_v=min_val, max_v=max_val: self.set_interval(min_v, max_v)
            )
            if self.config['min_interval'] == min_val and self.config['max_interval'] == max_val:
                item.state = 1
            self.interval_menu.add(item)
    
    def build_active_hours_menu(self):
        """Build the active hours submenu"""
        hour_ranges = [
            ("6 AM - 10 PM", 6, 22),
            ("7 AM - 9 PM", 7, 21),
            ("8 AM - 8 PM", 8, 20),
            ("9 AM - 5 PM", 9, 17),
            ("9 AM - 10 PM", 9, 22),
            ("10 AM - 6 PM", 10, 18),
            ("24 Hours", 0, 24),
        ]
        
        for label, start, end in hour_ranges:
            item = rumps.MenuItem(
                label,
                callback=lambda sender, s=start, e=end: self.set_active_hours(s, e)
            )
            if self.config['start_hour'] == start and self.config['end_hour'] == end:
                item.state = 1
            self.active_hours_menu.add(item)
    
    def set_interval(self, min_interval, max_interval):
        """Set the interval range"""
        # Clear all checkmarks
        for item in self.interval_menu.values():
            item.state = 0
        
        # Set new config
        self.config['min_interval'] = min_interval
        self.config['max_interval'] = max_interval
        self.save_config()
        
        # Set checkmark on selected item
        for item in self.interval_menu.values():
            if f"{min_interval}-{max_interval}" in item.title or \
               (min_interval == 5 and max_interval == 15 and "5-15" in item.title) or \
               (min_interval == 10 and max_interval == 20 and "10-20" in item.title) or \
               (min_interval == 15 and max_interval == 30 and "15-30" in item.title) or \
               (min_interval == 15 and max_interval == 45 and "15-45" in item.title) or \
               (min_interval == 30 and max_interval == 60 and "30-60" in item.title) or \
               (min_interval == 45 and max_interval == 90 and "45-90" in item.title) or \
               (min_interval == 60 and max_interval == 120 and "60-120" in item.title):
                item.state = 1
                break
        
        # Reschedule if enabled
        if self.enabled:
            self.schedule_next_bell()
    
    def set_active_hours(self, start_hour, end_hour):
        """Set the active hours"""
        # Clear all checkmarks
        for item in self.active_hours_menu.values():
            item.state = 0
        
        # Set new config
        self.config['start_hour'] = start_hour
        self.config['end_hour'] = end_hour
        self.save_config()
        
        # Set checkmark on selected item
        for item in self.active_hours_menu.values():
            if (start_hour == 6 and end_hour == 22 and "6 AM - 10 PM" in item.title) or \
               (start_hour == 7 and end_hour == 21 and "7 AM - 9 PM" in item.title) or \
               (start_hour == 8 and end_hour == 20 and "8 AM - 8 PM" in item.title) or \
               (start_hour == 9 and end_hour == 17 and "9 AM - 5 PM" in item.title) or \
               (start_hour == 9 and end_hour == 22 and "9 AM - 10 PM" in item.title) or \
               (start_hour == 10 and end_hour == 18 and "10 AM - 6 PM" in item.title) or \
               (start_hour == 0 and end_hour == 24 and "24 Hours" in item.title):
                item.state = 1
                break
        
        # Reschedule if enabled
        if self.enabled:
            self.schedule_next_bell()
    
    def build_sound_menu(self):
        """Build the sound selection submenu"""
        sounds = [
            ("Japanese Bell", "Japanese Bell"),
            ("Glass (System)", "Glass"),
            ("Ping (System)", "Ping"),
            ("Tink (System)", "Tink"),
            ("Pop (System)", "Pop"),
        ]
        
        for label, sound_name in sounds:
            item = rumps.MenuItem(
                label,
                callback=lambda sender, sn=sound_name: self.set_sound(sn)
            )
            if self.config.get('sound', 'Glass') == sound_name:
                item.state = 1
            self.sound_menu.add(item)
    
    def set_sound(self, sound_name):
        """Set the bell sound"""
        # Clear all checkmarks
        for item in self.sound_menu.values():
            item.state = 0
        
        # Set new config
        self.config['sound'] = sound_name
        self.save_config()
        
        # Set checkmark on selected item
        for item in self.sound_menu.values():
            if (sound_name == "Japanese Bell" and "Japanese Bell" in item.title) or \
               (sound_name == "Glass" and "Glass" in item.title) or \
               (sound_name == "Ping" and "Ping" in item.title) or \
               (sound_name == "Tink" and "Tink" in item.title) or \
               (sound_name == "Pop" and "Pop" in item.title):
                item.state = 1
                break
    
    def toggle_bell(self, sender):
        """Toggle the bell on/off"""
        self.enabled = not self.enabled
        
        if self.enabled:
            self.toggle_item.title = "Stop Bell"
            # Keep the same icon, just change alpha/template mode if needed
            self.schedule_next_bell()
        else:
            self.toggle_item.title = "Start Bell"
            # Keep the same icon
            self.next_bell_time = None
            self.next_bell_item.title = "Next Bell: Not scheduled"
    
    def schedule_next_bell(self):
        """Schedule the next bell within active hours"""
        now = datetime.datetime.now()
        
        # Generate random interval in minutes
        interval_minutes = random.randint(
            self.config['min_interval'],
            self.config['max_interval']
        )
        
        # Calculate next bell time
        next_time = now + datetime.timedelta(minutes=interval_minutes)
        
        # Check if within active hours
        if self.config['end_hour'] == 24:  # 24 hours mode
            self.next_bell_time = next_time
        elif next_time.hour >= self.config['end_hour'] or next_time.hour < self.config['start_hour']:
            # Schedule for next day's start hour
            tomorrow = now + datetime.timedelta(days=1)
            self.next_bell_time = tomorrow.replace(
                hour=self.config['start_hour'],
                minute=random.randint(0, 59),
                second=0,
                microsecond=0
            )
        else:
            self.next_bell_time = next_time
        
        # Update menu
        self.update_next_bell_display()
    
    def update_next_bell_display(self):
        """Update the next bell time display"""
        if self.next_bell_time:
            time_str = self.next_bell_time.strftime("%I:%M %p")
            now = datetime.datetime.now()
            
            # Add relative time
            delta = self.next_bell_time - now
            minutes = int(delta.total_seconds() / 60)
            
            if minutes < 60:
                relative = f"in {minutes} min"
            elif minutes < 1440:
                hours = minutes // 60
                relative = f"in {hours} hr"
            else:
                relative = "tomorrow"
            
            self.next_bell_item.title = f"Next Bell: {time_str} ({relative})"
        else:
            self.next_bell_item.title = "Next Bell: Not scheduled"
    
    def is_within_active_hours(self):
        """Check if current time is within active hours"""
        now = datetime.datetime.now()
        current_hour = now.hour
        
        if self.config['end_hour'] == 24:  # 24 hours mode
            return True
        
        return self.config['start_hour'] <= current_hour < self.config['end_hour']
    
    def play_bell(self):
        """Play the bell sound"""
        sound_name = self.config.get('sound', 'Glass')
        
        # Define sound paths
        sound_map = {
            'Japanese Bell': os.path.join(os.path.dirname(__file__), 'media', 'jap-rin-1.aiff'),
            'Glass': '/System/Library/Sounds/Glass.aiff',
            'Ping': '/System/Library/Sounds/Ping.aiff',
            'Tink': '/System/Library/Sounds/Tink.aiff',
            'Pop': '/System/Library/Sounds/Pop.aiff',
        }
        
        sound_path = sound_map.get(sound_name, '/System/Library/Sounds/Glass.aiff')
        
        if os.path.exists(sound_path):
            sound = NSSound.alloc().initWithContentsOfFile_byReference_(sound_path, True)
            if sound:
                sound.play()
    
    def test_bell(self, sender):
        """Test the bell sound"""
        self.play_bell()
        rumps.notification(
            title="MindBell",
            subtitle="Test Bell",
            message="This is how your meditation bell will sound",
            sound=False
        )
    
    def timer_loop(self):
        """Background thread to check for bell times"""
        while self.running:
            if self.enabled and self.next_bell_time:
                now = datetime.datetime.now()
                
                # Update display every minute
                self.update_next_bell_display()
                
                # Check if it's time to ring
                if now >= self.next_bell_time:
                    if self.is_within_active_hours():
                        # Play bell
                        rumps.Timer(lambda _: self.play_bell(), 0.1).start()
                        
                        # Show notification
                        rumps.notification(
                            title="MindBell",
                            subtitle="Mindfulness Reminder",
                            message="Take a moment to be present",
                            sound=False
                        )
                    
                    # Schedule next bell
                    self.schedule_next_bell()
            
            # Sleep for 30 seconds
            time.sleep(30)
    
    def quit_app(self, sender):
        """Quit the application"""
        self.running = False
        rumps.quit_application()

if __name__ == "__main__":
    MindBellApp().run()