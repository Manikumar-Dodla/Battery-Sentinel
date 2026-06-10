import time
import os
import psutil
import winsound
import tkinter as tk
from plyer import notification

# ==========================
# Configuration
# ==========================

LOW_BATTERY_WARNING = 30
HIBERNATE_BATTERY = 20

HIGH_BATTERY_WARNING = 85
RED_SCREEN_WARNING = 90

NORMAL_CHECK_INTERVAL = 300  # 5 minutes
LOW_BATTERY_INTERVAL = 60    # 1 minute

current_year = time.strftime("%Y")
LOG_FILE = rf"C:\Projects\Battery\Logs_{current_year}.txt"

# ==========================
# Alert Flags
# ==========================

low_alert_sent = False
high_alert_sent = False
red_alert_sent = False
hibernate_alert_sent = False

# ==========================
# Logging
# ==========================

def write_log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {message}\n")

# ==========================
# Notifications
# ==========================

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

# ==========================
# Red Warning Screen
# ==========================

def red_warning_screen():
    write_log("Red warning screen opened.")

    root = tk.Tk()

    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="red")

    root.bind("<Escape>", lambda e: root.destroy())

    label = tk.Label(
        root,
        text="UNPLUG CHARGER\nBATTERY ABOVE 90%\n\nPress ESC to dismiss",
        font=("Arial", 40, "bold"),
        bg="red",
        fg="white"
    )

    label.pack(expand=True)

    root.mainloop()

    write_log("Red warning screen closed.")

# ==========================
# Hibernate
# ==========================

def hibernate_system():
    write_log("Critical battery reached. Hibernation sequence started.")

    show_notification(
        "Critical Battery",
        "Battery critically low. Hibernating in 10 seconds."
    )

    winsound.Beep(600, 1000)

    time.sleep(10)

    write_log("Executing shutdown /h")

    os.system("shutdown /h")

# ==========================
# Startup Logging
# ==========================

write_log("=" * 60)
write_log(f"Battery Monitor Started - {current_year}")
write_log("=" * 60)

# ==========================
# Initial Battery State
# ==========================

battery = psutil.sensors_battery()

if battery is None:
    write_log("Battery information unavailable.")
    raise SystemExit

previous_plugged_state = battery.power_plugged

write_log(
    f"Initial State | Battery={battery.percent}% | Charging={battery.power_plugged}"
)

# ==========================
# Main Loop
# ==========================

try:
    while True:

        battery = psutil.sensors_battery()

        if battery is None:
            write_log("Battery information unavailable.")
            break

        percent = battery.percent
        plugged = battery.power_plugged

        # ----------------------
        # Charger State Changes
        # ----------------------

        if plugged != previous_plugged_state:

            if plugged:
                write_log(
                    f"Charger Connected | Battery={percent}%"
                )
            else:
                write_log(
                    f"Charger Disconnected | Battery={percent}%"
                )

            previous_plugged_state = plugged

        # ----------------------
        # LOW BATTERY WARNING
        # ----------------------

        if (
            percent <= LOW_BATTERY_WARNING
            and not plugged
            and not low_alert_sent
        ):
            winsound.Beep(800, 500)

            show_notification(
                "Battery Low",
                f"Battery at {percent}%. Plug in charger."
            )

            write_log(
                f"Low Battery Warning Triggered | Battery={percent}%"
            )

            low_alert_sent = True

        if percent > LOW_BATTERY_WARNING or plugged:
            low_alert_sent = False

        # ----------------------
        # HIGH BATTERY WARNING
        # ----------------------

        if (
            percent >= HIGH_BATTERY_WARNING
            and plugged
            and not high_alert_sent
        ):
            winsound.Beep(1000, 500)

            show_notification(
                "Battery Charged",
                f"Battery at {percent}%. Consider unplugging charger."
            )

            write_log(
                f"High Battery Warning Triggered | Battery={percent}%"
            )

            high_alert_sent = True

        if percent < HIGH_BATTERY_WARNING or not plugged:
            high_alert_sent = False

        # ----------------------
        # RED SCREEN WARNING
        # ----------------------

        if (
            percent >= RED_SCREEN_WARNING
            and plugged
            and not red_alert_sent
        ):
            winsound.Beep(1200, 1000)

            write_log(
                f"Red Screen Warning Triggered | Battery={percent}%"
            )

            red_warning_screen()

            red_alert_sent = True

        if percent < RED_SCREEN_WARNING or not plugged:
            red_alert_sent = False

        # ----------------------
        # CRITICAL BATTERY
        # ----------------------

        if (
            percent <= HIBERNATE_BATTERY
            and not plugged
            and not hibernate_alert_sent
        ):
            write_log(
                f"Critical Battery Threshold Reached | Battery={percent}%"
            )

            hibernate_alert_sent = True

            hibernate_system()

        if percent > HIBERNATE_BATTERY or plugged:
            hibernate_alert_sent = False

        # ----------------------
        # Dynamic Sleep
        # ----------------------

        if percent <= 30 and not plugged:
            sleep_time = LOW_BATTERY_INTERVAL
        else:
            sleep_time = NORMAL_CHECK_INTERVAL

        time.sleep(sleep_time)

except KeyboardInterrupt:
    write_log("Battery Monitor Stopped Manually.")

except Exception as e:
    write_log(f"Unhandled Exception | {str(e)}")

finally:
    write_log(f"Battery Monitor Exited - {current_year}")
    write_log("=" * 60)