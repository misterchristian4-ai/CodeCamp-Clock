
# view.py
import tkinter as tk
from tkinter import ttk
import os 
from tkinter import TclError # Import TclError to handle potential icon errors

# --- Utility Functions for Styling ---
def configure_styles(root):
    style = ttk.Style(root)
    # Using a modern theme and configuring dark mode style
    style.theme_use('clam')
    
    # General Dark Background
    style.configure("TFrame", background="#2b2b2b")
    style.configure("TLabel", background="#2b2b2b", foreground="#FFFFFF")
    
    # Display elements (Digital font look)
    style.configure("Time.TLabel", background="#2b2b2b", foreground="#00ff00", font=("Consolas", 45, "bold"))
    style.configure("Info.TLabel", background="#2b2b2b", foreground="#999999", font=("Consolas", 12))
    style.configure("Header.TLabel", background="#2b2b2b", foreground="#FFFFFF", font=("Helvetica", 16, "bold"))
    
    # Buttons and Entry
    style.configure("TButton", font=("Helvetica", 10, "bold"), padding=8, background="#555555", foreground="#FFFFFF")
    style.configure("TEntry", fieldbackground="#444444", foreground="#FFFFFF", borderwidth=0)
    
    # Notebook/Tabs style
    style.configure("TNotebook", background="#2b2b2b", borderwidth=0)
    style.configure("TNotebook.Tab", background="#3c3c3c", foreground="#FFFFFF", padding=[15, 5])
    style.map("TNotebook.Tab", background=[("selected", "#555555")], foreground=[("selected", "#FFFFFF")])


# --- Individual Page Frames (Views) ---

class CurrentTimeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame", padding="20")
        self.controller = controller

        # Layout: Grid in a single column
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="🌍 CURRENT TIME", style="Header.TLabel").grid(row=0, column=0, pady=(0, 15), sticky="ew")

        # Time Label (Digital Display)
        self.time_label = ttk.Label(self, text="--:--:--", style="Time.TLabel")
        self.time_label.grid(row=1, column=0, pady=(5, 5), sticky="ew")

        # Date Label
        self.date_label = ttk.Label(self, text="---, --- --, ----", style="Info.TLabel", font=("Consolas", 18))
        self.date_label.grid(row=2, column=0, pady=(0, 15), sticky="ew")

        # Controls/Status Container
        controls_frame = ttk.Frame(self, style="TFrame")
        controls_frame.grid(row=3, column=0, pady=10, sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1) # Center the dropdown

        # Time Zone Dropdown
        ttk.Label(controls_frame, text="TIME ZONE:", style="Info.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tz_var = tk.StringVar(self)
        self.tz_combobox = ttk.Combobox(controls_frame, textvariable=self.tz_var, state="readonly", width=20)
        self.tz_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Populate combobox values (must be handled carefully during initialization)
        try:
            self.tz_combobox['values'] = self.controller.get_timezone_keys()
            self.tz_combobox.current(0)
        except IndexError:
            # Handle case where controller might not be fully initialized or returns no keys
            self.tz_combobox['values'] = ['Loading...']
            self.tz_combobox.set('Loading...')

        self.tz_combobox.bind('<<ComboboxSelected>>', self.controller.timezone_selected_action)

        # Format Button
        self.format_button = ttk.Button(controls_frame, text="CHANGE TIME_FORMAT", command=self.controller.toggle_format_action)
        self.format_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Status Label
        self.status_label = ttk.Label(self, text="", style="Info.TLabel")
        self.status_label.grid(row=4, column=0, pady=(15, 0), sticky="ew")
        
        # Keep a reference to the alarm status for flashing logic
        self.alarm_status = "ALARM OFF" 

    def update(self, data):
        self.time_label.config(text=data["time_str"])
        self.date_label.config(text=data["date_str"])
        self.status_label.config(text=f"{data['format_status']} | Time Zone: {data['tz_key']}")
        self.alarm_status = data["alarm_status"]
        
        # Flashing Alarm Check
        if "TRIGGERED" in self.alarm_status:
            current_color = self.time_label.cget("foreground")
            # Flashing between red and the normal green
            new_color = "#FF4444" if current_color == "#00ff00" else "#00ff00" 
            self.time_label.config(foreground=new_color)
        else:
            self.time_label.config(foreground="#00ff00")


class AlarmFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame", padding="20")
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="⏰ ALARM", style="Header.TLabel", foreground="#ff6666").grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Alarm Status Label
        self.alarm_status_label = ttk.Label(self, text="Alarm SET", style="Time.TLabel", foreground="#FF4444")
        self.alarm_status_label.grid(row=1, column=0, pady=(5, 30), sticky="ew")

        # Input Frame
        input_frame = ttk.Frame(self, style="TFrame")
        input_frame.grid(row=2, column=0, pady=10, sticky="ew")
        
        ttk.Label(input_frame, text="SET TIME:", font= "arial 20", style="Info.TLabel").pack(side=tk.LEFT, padx=10)
        
        # Hour Input
        self.alarm_hour_var = tk.StringVar(self, value="00")
        self.alarm_hour_entry = ttk.Entry(input_frame, textvariable=self.alarm_hour_var, width=3, justify='center')
        self.alarm_hour_entry.pack(side=tk.LEFT)
        ttk.Label(input_frame, text=":", style="Info.TLabel").pack(side=tk.LEFT)
        
        # Minute Input
        self.alarm_minute_var = tk.StringVar(self, value="00")
        self.alarm_minute_entry = ttk.Entry(input_frame, textvariable=self.alarm_minute_var, width=3, justify='center')
        self.alarm_minute_entry.pack(side=tk.LEFT)
        
        # Buttons Frame
        button_frame = ttk.Frame(self, style="TFrame")
        button_frame.grid(row=3, column=0, pady=(20, 0), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Button(button_frame, text="SET ALARM", command=self.controller.set_alarm_action).grid(row=0, column=0, padx=10, sticky="ew")
        ttk.Button(button_frame, text="CLEAR ALARM", command=self.controller.clear_alarm_action).grid(row=0, column=1, padx=10, sticky="ew")

    def update(self, data):
        self.alarm_status_label.config(text=data["alarm_status"])
        
        if "TRIGGERED" in data["alarm_status"]:
            current_color = self.alarm_status_label.cget("foreground")
            # Flashing between white and red
            new_color = "#FFFFFF" if current_color == "#FF4444" else "#FF4444" 
            self.alarm_status_label.config(foreground=new_color)
        else:
            self.alarm_status_label.config(foreground="#FF4444")


class TimerFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame", padding="20")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="⏱️ TIMER", style="Header.TLabel", foreground="#66ccff").grid(row=0, column=0, pady=(0, 20), sticky="ew")

        # Timer Display
        self.timer_label = ttk.Label(self, text="00:00:00", style="Time.TLabel", foreground="#66ccff")
        self.timer_label.grid(row=1, column=0, pady=(5, 5), sticky="ew")

        # Timer Status Label
        self.timer_status_label = ttk.Label(self, text="TIMER OFF", style="Info.TLabel")
        self.timer_status_label.grid(row=2, column=0, pady=(0, 20), sticky="ew")

        # Input Frame
        input_frame = ttk.Frame(self, style="TFrame")
        input_frame.grid(row=3, column=0, pady=10, sticky="ew")
        
        ttk.Label(input_frame, text="SET TIME:", style="Info.TLabel").pack(side=tk.LEFT, padx=10)
        
        # Hour Input
        self.timer_hour_var = tk.StringVar(self, value="00")
        self.timer_hour_entry = ttk.Entry(input_frame, textvariable=self.timer_hour_var, width=3, justify='center')
        self.timer_hour_entry.pack(side=tk.LEFT)
        ttk.Label(input_frame, text=":", style="Info.TLabel").pack(side=tk.LEFT)
        
        # Minute Input
        self.timer_minute_var = tk.StringVar(self, value="00")
        self.timer_minute_entry = ttk.Entry(input_frame, textvariable=self.timer_minute_var, width=3, justify='center')
        self.timer_minute_entry.pack(side=tk.LEFT)
        ttk.Label(input_frame, text=":", style="Info.TLabel").pack(side=tk.LEFT)
        
        # Second Input
        self.timer_second_var = tk.StringVar(self, value="00")
        self.timer_second_entry = ttk.Entry(input_frame, textvariable=self.timer_second_var, width=3, justify='center')
        self.timer_second_entry.pack(side=tk.LEFT)
        
        # Buttons Frame
        button_frame = ttk.Frame(self, style="TFrame")
        button_frame.grid(row=4, column=0, pady=(20, 0), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        ttk.Button(button_frame, text="SET DURATION", command=self.controller.set_timer_action).grid(row=0, column=0, padx=5, sticky="ew")
        self.start_stop_timer_button = ttk.Button(button_frame, text="START", command=self.controller.start_stop_timer_action)
        self.start_stop_timer_button.grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(button_frame, text="RESET", command=self.controller.reset_timer_action).grid(row=0, column=2, padx=5, sticky="ew")

    def update(self, data):
        self.timer_label.config(text=data["timer_str"])
        self.timer_status_label.config(text=data["timer_status"])
        
        if "FINISHED" in data["timer_status"]:
            current_color = self.timer_label.cget("foreground")
            # Flashing between red and blue
            new_color = "#FF4444" if current_color == "#66ccff" else "#66ccff" 
            self.timer_label.config(foreground=new_color)
            self.start_stop_timer_button.config(text="START")
        elif "RUNNING" in data["timer_status"]:
            self.timer_label.config(foreground="#66ccff")
            self.start_stop_timer_button.config(text="STOP")
        else:
            self.timer_label.config(foreground="#66ccff")
            self.start_stop_timer_button.config(text="START")


# --- Main Application Window ---

class ClockView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Professional Time Utility")
        self.geometry("600x450")
        self.resizable(False, False)

        configure_styles(self)
        self.configure(bg="#2b2b2b") # Set root background

        # FIX 1: Variable to store the ID of the scheduled 'after' call for cancellation
        self.after_id = None 

        # ICON FIX: Error handling added for icon loading
        icon_path = os.path.join(r'clock_image.ico')
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except TclError:
                print("Warning: Could not load icon. Ensure the path is correct and the file is a valid .ico.")
            
        # FIX 2: Register the clean shutdown handler (CRITICAL FIX for "invalid command name")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # --- 1. Notebook (Tabbed Interface) ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # --- 2. Dictionary to hold all page frames ---
        self.frames = {}
        frame_configs = [
            ("Time", CurrentTimeFrame), 
            ("Alarm", AlarmFrame), 
            ("Timer", TimerFrame)
        ]
        
        for name, FrameClass in frame_configs:
            frame = FrameClass(self.notebook, controller)
            self.frames[name] = frame
            # Add frame as a tab in the notebook
            self.notebook.add(frame, text=name)

    def on_closing(self):
        """
        Called when the user attempts to close the window.
        This explicitly cancels the scheduled 'after' loop before destroying the window.
        """
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            print("Clean shutdown: Cancelled pending clock update.")
            
        self.destroy() 


    def update_displays(self, data):
        """Passes the updated data to the update method of ALL frames."""
        # Use keys matching the Frame class names
        self.frames["Time"].update(data) 
        self.frames["Alarm"].update(data)
        self.frames["Timer"].update(data)