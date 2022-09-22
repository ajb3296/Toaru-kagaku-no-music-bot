import os
import platform

def get_java_path():
    platform_sys = platform.system()
    if platform_sys == "Windows":
        # Windows
        jpath = f"'{os.environ.get('JAVA_HOME', None)}java'"
    else:
        jpath = "/usr/bin/java"

    return jpath