from musicbot.utils.get_java_path import get_java_path
import subprocess
import multiprocessing

def child_process():
    print(f"Child process PID : {multiprocessing.current_process().pid}")
    args = [get_java_path(), '-jar', 'Lavalink.jar']
    subprocess.call(args, shell=False)