# AIPI Bridge Assistant (Windows 11)

A lightweight desktop setup helper for sharing a Windows laptop's current internet connection with an AIPI Lite device.

## Run it

1. Install Python 3 from https://www.python.org/downloads/windows/ and enable **Add Python to PATH**.
2. Download or clone this repository.
3. Double-click `run_app.bat`.

## Included features

- Lists active Windows network adapters.
- Opens Windows 11 Mobile Hotspot settings.
- Provides AIPI Lite setup guidance and 2.4 GHz compatibility tips.

## Important limitations

This first version is a **setup assistant**, not an independently implemented Wi-Fi router or driver. Windows controls hotspot creation and connection sharing.

- It cannot make an unsupported Wi-Fi adapter support simultaneous client and hotspot operation.
- It cannot guarantee that Windows offers a 2.4 GHz hotspot band; that depends on the adapter and driver.
- It does not bypass campus network restrictions or captive-portal authentication.

In Windows Mobile Hotspot settings, select the internet connection to share, edit the hotspot name and password, choose 2.4 GHz if available, and turn the hotspot on. Then connect AIPI Lite to that network from its setup page at `http://192.168.4.1`.
