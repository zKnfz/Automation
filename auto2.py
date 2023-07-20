import os
import logging
from os.path import splitext, exists, join
from shutil import move
from time import sleep

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


source_dir = "/Users/caydenknight/Downloads"
dest_dir_sfx = "/Users/caydenknight/Desktop/sound"
dest_dir_music = "/Users/caydenknight/Desktop/music"
dest_dir_video = "/Users/caydenknight/Desktop/downloaded vid"
dest_dir_image = "/Users/caydenknight/Desktop/downloaded img"
dest_dir_documents = "/Users/caydenknight/Desktop/docs"

image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp"]
video_extensions = [".mp4", ".avi", ".mov", ".wmv", ".flv"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        move(entry.path, join(dest, unique_name))
    else:
        move(entry.path, join(dest, name))

class MoverHandler(FileSystemEventHandler):
    
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def on_any_event(self, event):
        logging.info(f"Event type: {event.event_type}; Path: {event.src_path}")

    def check_audio_files(self, entry, name):  
        for audio_extension in audio_extensions:
            if name.lower().endswith(audio_extension):
                logging.info(f"Audio file detected with extension: {audio_extension}")
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  
        for video_extension in video_extensions:
            if name.lower().endswith(video_extension):
                logging.info(f"Video file detected with extension: {video_extension}")
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  
        for image_extension in image_extensions:
            if name.lower().endswith(image_extension):
                logging.info(f"Image file detected with extension: {image_extension}")
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  
        for documents_extension in document_extensions:
            if name.lower().endswith(documents_extension):
                logging.info(f"Document file detected with extension: {documents_extension}")
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
