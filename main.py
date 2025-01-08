import logging
from os import rename, scandir, makedirs
from os.path import exists, join, splitext, expanduser
from shutil import move
from time import sleep

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Expand paths
source_dir = expanduser("~/Downloads/")
dest_dir_audio = expanduser("~/Audio")
dest_dir_music = expanduser("~/Music/")
dest_dir_video = expanduser("~/Videos/")
dest_dir_image = expanduser("~/Pictures/")
dest_dir_documents = expanduser("~/Documents/")

image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".ico"]
video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm"]
audio_extensions = [".mp3", ".wav", ".aac", ".flac", ".m4a"]
document_extensions = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]


def ensure_dir_exists(directory):
    if not exists(directory):
        makedirs(directory)

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name

def mov_file(dest, entry, name):
    ensure_dir_exists(dest)
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        old_name = join(dest, name)
        new_name = join(dest, unique_name)
        rename(old_name, new_name)
    move(entry.path, dest)

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    self.process_file(entry)

    def process_file(self, entry):
        name = entry.name
        if any(name.endswith(ext) for ext in audio_extensions):
            mov_file(dest_dir_audio, entry, name)
            logging.info(f"Moved audio file: {name}")
        elif any(name.endswith(ext) for ext in video_extensions):
            mov_file(dest_dir_video, entry, name)
            logging.info(f"Moved video file: {name}")
        elif any(name.endswith(ext) for ext in image_extensions):
            mov_file(dest_dir_image, entry, name)
            logging.info(f"Moved image file: {name}")
        elif any(name.endswith(ext) for ext in document_extensions):
            mov_file(dest_dir_documents, entry, name)
            logging.info(f"Moved document: {name}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

