import time
import os
from threading import Thread
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from .site.builderCss import compile_css

# 1. The Action (What happens when a file changes)
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            # This is where you call your CSS compiler
            print(f"🔔 Change detected: {event.src_path}")
            try:
                compile_css()
            except:
                print("Failed")

# 2. The Worker (The function that runs inside the thread)
def run_watcher_loop(path):
    target_path = os.path.abspath(path)
    
    if not os.path.exists(target_path):
        print(f"❌ Watcher Error: Folder not found at {target_path}")
        return

    event_handler = MyHandler()
    observer = PollingObserver() # Force polling for reliability
    observer.schedule(event_handler, target_path, recursive=True)
    
    observer.start()
    print(f"✅ Watcher Thread is active on: {target_path}")
    
    try:
        while True:
            time.sleep(1) # Keep the thread alive
    except Exception as e:
        observer.stop()
        print(f"Watcher Thread crashed: {e}")
    observer.join()

# 3. The Starter (Call this in your main Flask block)
def start_background_watcher():
    # Define your path here
    folder_to_watch = "./app/site/src/"
    
    # Create the thread
    # daemon=True means the thread dies automatically when you close the app
    watcher_thread = Thread(target=run_watcher_loop, args=(folder_to_watch,), daemon=True)
    watcher_thread.start()

# --- Integration with Flask ---
def run():
    start_background_watcher()
    
    # Start your Flask app
    # app.run(debug=True)