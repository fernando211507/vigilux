import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('nftables_data.db'):  # Reemplaza '.sqlite' con la extensión de tu base de datos
            # Ejecuta el script sh
            # Ejemplo:
            import subprocess
            subprocess.run(["/var/www/html/myproject/Run.sh"])  # Reemplaza con la ruta a tu script

if __name__ == "__main__":
    path_to_watch = '/var/www/html/myproject/'  # Reemplaza con la ruta a la carpeta que contiene la base de datos
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
