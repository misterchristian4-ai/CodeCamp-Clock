
# ⏰ Professional Time Utility (Tkinter Clock Application)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-lightgrey)
![MVC](https://img.shields.io/badge/Architecture-MVC-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-purple)
![Status](https://img.shields.io/badge/Status-Active-success)

A feature-packed desktop time utility built using **Python + Tkinter**,
structured with **MVC architecture** for clean, scalable, and
maintainable code.

------------------------------------------------------------------------

## 🌟 Features

### 🕒 Live Time & Date

-   Accurate real-time clock\
-   Multiple timezone support\
-   Local system time option\
-   Smooth UI updates (1000ms interval)

### 🌓 12/24 Hour Format

-   Toggle between **AM/PM** and **24-hour** mode

### ⏰ Alarm System

-   Set alarm using **HH:MM**\
-   Sound alert (Windows: `winsound`)\
-   Reliable trigger logic even when seconds don't align

### ⏳ Countdown Timer

-   Supports **HH:MM:SS** format\
-   Start / Stop / Reset\
-   Plays sound at finish\
-   Status labels for clarity

### 🎬 Splash Screen

-   Loads a GIF animation before the main UI\
-   Smooth transition

### 🛑 Clean Shutdown

Prevents this common Tkinter crash:

    TclError: invalid command name

using a safe `after_cancel()` strategy.

------------------------------------------------------------------------

## 📦 Installation

### 1️⃣ Install Dependencies

``` bash
pip install pytz Pillow
```

### 2️⃣ Run the App

``` bash
python main.py
```

------------------------------------------------------------------------

## 📁 Project Structure

    Clock_App/
    ├── main.py             # Application entry point
    ├── controller.py       # Controller logic
    ├── models.py           # Model logic: time, alarm, timer
    ├── view.py             # Tkinter UI
    ├── splash.py           # Splash screen class
    ├── DGIF.gif            # Loading animation
    └── clock_image.ico     # (Optional) Application icon

------------------------------------------------------------------------

## 🧭 Usage Overview

### 🧩 Tabs

#### 1. **Time Tab**

-   Shows real-time clock + date\
-   Dropdown to select timezone\
-   Toggle 12/24-hour format

#### 2. **Alarm Tab**

-   Enter alarm time (HH:MM)\
-   Set, Trigger, Clear\
-   Sound plays when time is reached

#### 3. **Timer Tab**

-   Enter countdown time\
-   Set → Start/Stop → Reset\
-   Sound plays when done

------------------------------------------------------------------------

## 🧱 MVC Architecture

  --------------------------------------------------------------------------
  Component                File              Description
  ------------------------ ----------------- -------------------------------
  **Model**                `models.py`       Manages time, timezone, alarm,
                                             timer

  **View**                 `view.py`         UI with Tkinter

  **Controller**           `controller.py`   Connects user actions \<→ model
                                             \<→ view
  --------------------------------------------------------------------------

The MVC pattern keeps the project modular and easy to maintain.

------------------------------------------------------------------------

## 🛠️ Troubleshooting

### 🔇 No Sound?

-   **Windows only:** `winsound`\
-   For macOS/Linux, replace with:
    -   `playsound`
    -   `pygame`

### ❗ TclError on Close

Already fixed using proper loop cancellation.\
Avoid deleting `on_closing()` or `WM_DELETE_WINDOW`.

### ❗ Icon Not Displaying

Ensure:

``` python
icon_path = os.path.join(os.getcwd(), "clock_image.ico")
```

------------------------------------------------------------------------

## 🖼️ Screenshots (Optional Section)

You can add images like this:

    ![Main UI](screenshots/main_ui.png)
    ![Splash Screen](screenshots/splash.gif)

------------------------------------------------------------------------

## ⭐ Future Enhancements (Ideas)

-   Pomodoro mode\
-   Data persistence (save alarms/timers)\
-   Dark/Light theme toggle\
-   Modern custom Tkinter widgets (CTk)\
-   Multiple alarms

------------------------------------------------------------------------
