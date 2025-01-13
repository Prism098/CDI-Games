import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess  # Use subprocess to handle processes


class RestartHandler(FileSystemEventHandler):
    def __init__(self, script, script_to_watch):
        self.script = script
        self.script_to_watch = script_to_watch
        self.process = None  # Initially no process

    def start_game(self):
        print(f"\nStarting game {self.script}...\n")
        # Use subprocess to start the game script without blocking the main loop
        self.process = subprocess.Popen([sys.executable, self.script])

    def restart_game(self):
        print("\nChanges detected. Restarting game...\n")
        # Kill the old process if it's running
        if self.process is not None:
            print("Terminating old game instance...")
            self.process.terminate()
            self.process.wait()  # Ensure the process has fully terminated
        # Start the new game process
        self.start_game()

    def on_modified(self, event):
        # Check if the modified file is not the watchdog script itself
        if event.src_path.endswith(".py") and os.path.basename(
            event.src_path
        ) != os.path.basename(self.script_to_watch):
            self.restart_game()


if __name__ == "__main__":
    path = "."  # Current directory (where your game script is located)
    script_name = "HCIMain.py"  # The name of your game script
    watchdog_script = "watchdog_runner.py"  # The name of your watchdog script
    event_handler = RestartHandler(script_name, watchdog_script)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    print(f"Watching {script_name} for changes...")
    observer.start()
    # Start the game initially
    event_handler.start_game()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Watchdog stopped.")
