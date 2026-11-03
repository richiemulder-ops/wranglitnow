"""Start Jarvis (if it isn't already running) and open it in the browser. The desktop shortcut runs this.

    launch.py          start if needed, then open the page
    launch.py --stop   stop the running server
"""
import os
import subprocess
import sys
import time
import urllib.request
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "http://localhost:%s/" % (os.environ.get("JARVIS_PORT") or 4700)
PID_FILE = os.path.join(HERE, "data", "server.pid")


def running():
    try:
        with urllib.request.urlopen(URL, timeout=2) as r:
            return r.status == 200
    except OSError:
        return False


def python_exe():
    """The console Python (not pythonw): the server's helper scripts talk over stdin/stdout."""
    exe = sys.executable
    if os.path.basename(exe).lower() == "pythonw.exe":
        exe = os.path.join(os.path.dirname(exe), "python.exe")
    return exe


def start():
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    log = open(os.path.join(HERE, "data", "server.log"), "a", encoding="utf-8")
    flags = 0x08000000 if os.name == "nt" else 0          # CREATE_NO_WINDOW: no black box on screen
    p = subprocess.Popen([python_exe(), os.path.join(HERE, "server.py")], cwd=HERE,
                         stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                         creationflags=flags, close_fds=True)
    with open(PID_FILE, "w") as f:
        f.write(str(p.pid))
    for _ in range(60):
        if running():
            return True
        if p.poll() is not None:
            return False
        time.sleep(0.5)
    return running()


def stop():
    try:
        pid = int(open(PID_FILE).read().strip())
    except (OSError, ValueError):
        print("Jarvis isn't running (no record of it).")
        return
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
    else:
        os.kill(pid, 15)
    os.remove(PID_FILE)
    print("Jarvis stopped.")


def main():
    if "--stop" in sys.argv:
        return stop()
    if not running() and not start():
        msg = "Jarvis didn't start. Details are in " + os.path.join(HERE, "data", "server.log")
        print(msg)
        if os.name == "nt":
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, msg, "Jarvis", 0x10)
        sys.exit(1)
    webbrowser.open(URL)


if __name__ == "__main__":
    main()
