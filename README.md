# Battery Monitor

A lightweight Windows battery monitoring utility written in Python.

Battery Monitor runs in the background and helps maintain battery health by notifying you when your battery reaches configured charge thresholds.

## Features

* 🔋 Low battery warning at **30%**
* ⚡ High battery warning at **85%**
* 🚨 Full-screen red warning screen at **90%**
* 💤 Automatic hibernation at **20%**
* 🔔 Desktop notifications
* 🔊 Audible alerts
* 📝 Automatic yearly log files
* 🔌 Charger connect/disconnect tracking
* 🖥️ Can run silently in the background

---

## Default Thresholds

| Event                 | Threshold |
| --------------------- | --------- |
| Low Battery Warning   | 30%       |
| High Battery Warning  | 85%       |
| Red Screen Warning    | 90%       |
| Automatic Hibernation | 20%       |

All values can be modified in the configuration section of the script.

---

## Requirements

* Windows
* Python 3.10+
* Battery-equipped device

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/BatteryMonitor.git
cd BatteryMonitor
```

Install dependencies:

```bash
pip install psutil plyer
```

---

## Running

Run directly with Python:

```bash
python "Battery Status.py"
```

---

## Running Silently (No Command Prompt Window)

### Option 1: Rename to `.pyw`

Rename:

```text
Battery Status.py
```

to:

```text
Battery Status.pyw
```

Windows will launch the script using `pythonw.exe`, preventing a Command Prompt window from opening.

### Option 2: Build an Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the executable:

```bash
pyinstaller --onefile --noconsole "Battery Status.py"
```

Generated executable:

```text
dist/
└── Battery Status.exe
```

The executable runs silently in the background without opening a terminal window.

---

## Start Automatically with Windows

1. Build the executable (recommended).
2. Press:

```text
Win + R
```

3. Enter:

```text
shell:startup
```

4. Create a shortcut to:

```text
Battery Status.exe
```

inside the Startup folder.

The monitor will automatically launch whenever you sign in.

---

## Logging

The application automatically creates yearly log files in the same directory as the script.

Example:

```text
Logs_2026.txt
Logs_2027.txt
Logs_2028.txt
```

Example log entries:

```text
[2026-06-11 09:15:42] Battery Monitor Started
[2026-06-11 10:03:21] Charger Connected | Battery=62%
[2026-06-11 13:48:10] High Battery Warning Triggered | Battery=85%
[2026-06-11 15:07:55] Charger Disconnected | Battery=91%
```

---

## Configuration

Modify the following values to customize behavior:

```python
LOW_BATTERY_WARNING = 30
HIBERNATE_BATTERY = 20

HIGH_BATTERY_WARNING = 85
RED_SCREEN_WARNING = 90

NORMAL_CHECK_INTERVAL = 300
LOW_BATTERY_INTERVAL = 60
```

Intervals are specified in seconds.

---

## Warning

This application can automatically hibernate your computer when the battery reaches the configured threshold.

Default:

```python
HIBERNATE_BATTERY = 20
```

If you do not want automatic hibernation, either:

```python
HIBERNATE_BATTERY = 0
```

or remove:

```python
os.system("shutdown /h")
```

from the script.

---

## Project Structure

```text
BatteryMonitor/
│
├── Battery Status.py
├── README.md
├── .gitignore
└── Logs_2026.txt
```

---

## License

MIT License
