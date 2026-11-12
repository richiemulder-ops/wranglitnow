"""Start Jarvis (if it isn't already running) and open it in the browser. The desktop shortcut runs this.

    launch.py          start if needed, then open the page
    launch.py --stop   stop the running server
    launch.py --restart  wait for the old server to stop (after an update), then start it again
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


def spawn():
    """launch.py --spawn: start the server, record its process id, and exit straight away.

    The server must outlive whatever started Jarvis: the desktop shortcut, the updater, or a Claude
    Code session running the install, whose processes are cleaned up (the whole tree under its
    shell) when the session closes. Started from this short-lived helper, the server has no living
    parent within moments, so a clean-up of the caller's tree can't reach it, even while the server
    is still loading. Flags (Windows):
      CREATE_NO_WINDOW: no black box on screen, and a console of its own, apart from the caller's.
      CREATE_NEW_PROCESS_GROUP: the caller's Ctrl+C or console closing doesn't reach it.
      CREATE_BREAKAWAY_FROM_JOB: out of the caller's job object, where that job allows it."""
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    log = open(os.path.join(HERE, "data", "server.log"), "a", encoding="utf-8")
    base = (0x08000000 | 0x00000200) if os.name == "nt" else 0
    cmd = [python_exe(), os.path.join(HERE, "server.py")]
    try:
        p = subprocess.Popen(cmd, cwd=HERE, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                             creationflags=base | (0x01000000 if os.name == "nt" else 0), close_fds=True,
                             start_new_session=os.name != "nt")
    except OSError:   # the caller's job forbids breaking away: start it without that
        p = subprocess.Popen(cmd, cwd=HERE, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                             creationflags=base, close_fds=True, start_new_session=os.name != "nt")
    with open(PID_FILE, "w") as f:
        f.write(str(p.pid))


def alive(pid):
    if os.name != "nt":
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    import ctypes   # os.kill(pid, 0) would stop the process on Windows, so ask for its exit code
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, pid)   # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    code = ctypes.c_ulong()
    k.GetExitCodeProcess(h, ctypes.byref(code))
    k.CloseHandle(h)
    return code.value == 259   # STILL_ACTIVE


def start():
    flags = 0x08000000 if os.name == "nt" else 0   # the helper is gone in a moment; no window for it either
    subprocess.run([python_exe(), os.path.abspath(__file__), "--spawn"], cwd=HERE, creationflags=flags,
                   stdin=subprocess.DEVNULL, timeout=60)
    try:
        pid = int(open(PID_FILE).read().strip())
    except (OSError, ValueError):
        return False
    for _ in range(60):
        if running():
            return True
        if not alive(pid):
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
    if "--spawn" in sys.argv:   # internal: see spawn()
        return spawn()
    if "--stop" in sys.argv:
        return stop()
    if "--restart" in sys.argv:   # the page reloads itself, so no new browser tab
        for _ in range(40):
            if not running():
                break
            time.sleep(0.5)
        start()
        return
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
