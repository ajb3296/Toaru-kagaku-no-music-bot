import subprocess
import multiprocessing

def child_process():
    print(f"Child process PID : {multiprocessing.current_process().pid}")
    subprocess.call(["java", "-jar", "Lavalink.jar"], shell=False)
