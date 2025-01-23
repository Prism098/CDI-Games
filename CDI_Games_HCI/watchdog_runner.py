import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


class RestartHandler(FileSystemEventHandler):
    def __init__(self, script, script_to_watch):
        self.script = script
        self.script_to_watch = script_to_watch
        self.process = None

    def start_game(self):
        print(f"\nStarting game {self.script}...\n")
        self.process = subprocess.Popen([sys.executable, self.script])

    def restart_game(self):
        print("\nChanges detected. Restarting game...\n")
        if self.process is not None:
            print("Terminating old game instance...")
            self.process.terminate()
            self.process.wait()
        self.start_game()

    def on_modified(self, event):
        if event.src_path.endswith(".py") and os.path.basename(
            event.src_path
        ) != os.path.basename(self.script_to_watch):
            self.restart_game()


if __name__ == "__main__":
    # Automatically detect the directory where this script is located
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Set up paths for the game script and this script
    script_name = os.path.join(base_dir, "HCIMain.py")
    watchdog_script = os.path.join(base_dir, "watchdog_runner.py")
    path = base_dir  # Watch this directory

    # Initialize and run the watchdog
    event_handler = RestartHandler(script_name, watchdog_script)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    print(f"Watching {script_name} for changes...")
    observer.start()
    event_handler.start_game()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Watchdog stopped.")