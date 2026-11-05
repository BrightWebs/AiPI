import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "AIPI Bridge Assistant"

def run_powershell(command):
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            capture_output=True, text=True, timeout=12
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as exc:
        return "", str(exc), 1

def get_active_adapters():
    command = (
        "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | "
        "Select-Object -ExpandProperty Name"
    )
    out, err, code = run_powershell(command)
    if code != 0:
        return [], err or "Could not read network adapters."
    return [line.strip() for line in out.splitlines() if line.strip()], None

def open_hotspot_settings():
    try:
        subprocess.Popen(["cmd", "/c", "start", "", "ms-settings:network-mobilehotspot"], shell=False)
    except Exception:
        messagebox.showerror(APP_TITLE, "Could not open Windows Mobile Hotspot settings.")

def open_network_settings():
    try:
        subprocess.Popen(["cmd", "/c", "start", "", "ms-settings:network-status"], shell=False)
    except Exception:
        messagebox.showerror(APP_TITLE, "Could not open Windows network settings.")

def refresh_adapters():
    adapters, error = get_active_adapters()
    adapter_box.configure(state="normal")
    adapter_box.delete("1.0", "end")
    if error:
        adapter_box.insert("end", error)
    elif adapters:
        adapter_box.insert("end", "\n".join("• " + name for name in adapters))
    else:
        adapter_box.insert("end", "No active network adapters were detected.")
    adapter_box.configure(state="disabled")

root = tk.Tk()
root.title(APP_TITLE)
root.geometry("650x610")
root.minsize(600, 560)

style = ttk.Style()
try:
    style.theme_use("vista")
except tk.TclError:
    pass

main = ttk.Frame(root, padding=22)
main.pack(fill="both", expand=True)

ttk.Label(main, text="AIPI Bridge Assistant", font=("Segoe UI", 21, "bold")).pack(anchor="w")
ttk.Label(
    main,
    text="Share your Windows laptop's current internet connection with AIPI Lite.",
    font=("Segoe UI", 10)
).pack(anchor="w", pady=(4, 16))

status = ttk.Label(main, text="Windows 11 helper • Uses Windows Mobile Hotspot", foreground="#286a43")
status.pack(anchor="w", pady=(0, 14))

ttk.Label(main, text="1. Check your laptop's active connections", font=("Segoe UI", 12, "bold")).pack(anchor="w")
adapter_box = tk.Text(main, height=4, wrap="word", font=("Segoe UI", 10), relief="solid", borderwidth=1)
adapter_box.pack(fill="x", pady=(7, 8))
adapter_box.configure(state="disabled")
ttk.Button(main, text="Refresh connection list", command=refresh_adapters).pack(anchor="w", pady=(0, 18))

ttk.Label(main, text="2. Configure Windows Mobile Hotspot", font=("Segoe UI", 12, "bold")).pack(anchor="w")
ttk.Label(
    main,
    text=("Open Windows' built-in hotspot settings. Turn on Mobile hotspot, choose the "
          "connection to share, then edit the network name and password."),
    wraplength=590, justify="left"
).pack(anchor="w", pady=(6, 9))
ttk.Button(main, text="Open Mobile Hotspot settings", command=open_hotspot_settings).pack(anchor="w", pady=(0, 18))

ttk.Label(main, text="3. AIPI Lite compatibility settings", font=("Segoe UI", 12, "bold")).pack(anchor="w")
tips = (
    "• Set the hotspot band to 2.4 GHz if Windows offers that option.\n"
    "• Use WPA2-compatible security and a password-protected network.\n"
    "• On AIPI Lite, join the hotspot shown in its setup page at http://192.168.4.1.\n"
    "• If Windows cannot share the current Wi-Fi connection, the Wi-Fi adapter may not "
    "support simultaneous Wi-Fi client and hotspot operation."
)
ttk.Label(main, text=tips, wraplength=590, justify="left").pack(anchor="w", pady=(6, 18))

ttk.Label(main, text="Important", font=("Segoe UI", 10, "bold")).pack(anchor="w")
ttk.Label(
    main,
    text=("This first version is a setup assistant, not a custom Wi-Fi driver. Windows controls "
          "the hotspot and whether your adapter can share the connection. It does not bypass "
          "campus network rules or captive-portal sign-ins."),
    wraplength=590, justify="left"
).pack(anchor="w", pady=(4, 12))

bottom = ttk.Frame(main)
bottom.pack(fill="x", side="bottom")
ttk.Button(bottom, text="Open Network settings", command=open_network_settings).pack(side="left")
ttk.Button(bottom, text="Quit", command=root.destroy).pack(side="right")

refresh_adapters()
root.mainloop()
