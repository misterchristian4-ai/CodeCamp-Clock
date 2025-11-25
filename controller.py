
# # clock_controller.py
# import os
# from tkinter import messagebox
# import winsound


# class ClockController:
    
#     def __init__(self, model):
#         self.model = model
#         self.view = None
        
#     def set_view(self, view):
#         """Sets the single main view reference."""
#         self.view = view
        
#     def update_clock(self):
#         # ... (rest of the method is the same)
#         self.model.tick_timer()

#         time_str = self.model.get_time_string()
#         date_str = self.model.get_date_string()
#         format_status = self.model.get_format_status()
        
#         if self.view:
#             self.view.update_displays({
#                 "time_str": time_str,
#                 "date_str": date_str,
#                 "format_status": format_status,
#                 "alarm_status": self.model.get_alarm_status(),
#                 "timer_str": self.model.get_timer_string(),
#                 "timer_status": self.model.get_timer_status(),
#                 "tz_key": self.model.get_selected_timezone_key()
#             })

#         if self.model.get_just_triggered_status() or self.model.get_timer_just_finished_status():
#             try:
#                 # Play a system beep: Frequency (1000 Hz), Duration (500 ms = 0.5 seconds)
#                 winsound.Beep(1000, 2000)
                
#                 # OPTIONAL: You can play a standard system sound instead if you prefer:
#                 # winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
#             except Exception as e:
#                 # Fallback in case winsound is somehow unavailable (e.g., non-Windows environment)
#                 print(f"Winsound failed: {e}. Falling back to terminal bell.")
#                 os.system('echo -e "\a"') # Keep this as an absolute last resort
#         if self.view:
#             self.view.after(1000, self.update_clock)
            
#     # --- Data Retrieval Methods (The FIX is here) ---
#     def get_timezone_keys(self):
#         """Fetches the available timezone keys from the Model."""
#         return self.model.get_timezone_keys()

#     # --- Action Methods ---
    
#     def toggle_format_action(self):
#         self.model.toggle_format()
        
#     def timezone_selected_action(self, event):
#         # Access the current_time_frame's tz_var via the main view's storage
#         # Note: The view needs to be updated if you changed the internal frame keys from "CurrentTime" to "Time"
#         selected_tz_key = self.view.frames["Time"].tz_var.get()
#         self.model.set_timezone(selected_tz_key)

#     def set_alarm_action(self):
#         alarm_frame = self.view.frames["Alarm"]
    
#         hour_raw = alarm_frame.alarm_hour_var.get().strip()
#         minute_raw = alarm_frame.alarm_minute_var.get().strip()

#     # Validate numeric first
#         if not (hour_raw.isdigit() and minute_raw.isdigit()):
#             messagebox.showerror("Invalid Input", "Alarm time must contain only digits.")
#             alarm_frame.alarm_hour_var.set("00")
#             alarm_frame.alarm_minute_var.set("00")
#             return

#         hour = int(hour_raw)
#         minute = int(minute_raw)

#     # Validate ranges
#         if not (0 <= hour <= 23):
#             messagebox.showerror("Invalid Hour", "Hour must be between 00 and 23.")
#             alarm_frame.alarm_hour_var.set("00")
#             return

#         if not (0 <= minute <= 59):
#             messagebox.showerror("Invalid Minute", "Minutes must be between 00 and 59.")
#             alarm_frame.alarm_minute_var.set("00")
#             return

#     # Passed validation → set alarm
#         self.model.set_alarm(hour, minute)


#     def clear_alarm_action(self):
#         alarm_frame = self.view.frames["Alarm"]
#         self.model.clear_alarm()

#     # Reset UI fields
#         alarm_frame.alarm_hour_var.set("00")
#         alarm_frame.alarm_minute_var.set("00")

       

#     def set_timer_action(self):
#         timer_frame = self.view.frames["Timer"]

#         h_raw = timer_frame.timer_hour_var.get().strip()
#         m_raw = timer_frame.timer_minute_var.get().strip()
#         s_raw = timer_frame.timer_second_var.get().strip()

#     # Validate numeric
#         if not (h_raw.isdigit() and m_raw.isdigit() and s_raw.isdigit()):
#             messagebox.showerror("Invalid Input", "Timer fields must contain digits only.")
#             timer_frame.timer_hour_var.set("00")
#             timer_frame.timer_minute_var.set("00")
#             timer_frame.timer_second_var.set("00")
#             return

#         hours = int(h_raw)
#         minutes = int(m_raw)
#         seconds = int(s_raw)

#     # Range validation
#         if not (0 <= hours <= 99):
#             messagebox.showerror("Invalid Hours", "Hours must be between 00 and 99.")
#             timer_frame.timer_hour_var.set("00")
#             return

#         if not (0 <= minutes <= 59):
#             messagebox.showerror("Invalid Minutes", "Minutes must be between 00 and 59.")
#             timer_frame.timer_minute_var.set("00")
#             return

#         if not (0 <= seconds <= 59):
#             messagebox.showerror("Invalid Seconds", "Seconds must be between 00 and 59.")
#             timer_frame.timer_second_var.set("00")
#             return

#     # Valid → set timer
#         self.model.set_timer(hours, minutes, seconds)


#     def start_stop_timer_action(self):
#         status = self.model.get_timer_status()
#         if status == "RUNNING":
#             self.model.stop_timer()
#         elif status in ["READY", "TIMER FINISHED!"]:
#             self.model.start_timer()

#     def reset_timer_action(self):
#         timer_frame = self.view.frames["Timer"]
#         self.model.reset_timer()

#     # Reset UI
#         timer_frame.timer_hour_var.set("00")
#         timer_frame.timer_minute_var.set("00")
#         timer_frame.timer_second_var.set("00")


# controller.py
import os
from tkinter import messagebox
import winsound # Using the built-in Windows sound module

class ClockController:
    
    def __init__(self, model):
        self.model = model
        self.view = None
        
    def set_view(self, view):
        """Sets the single main view reference."""
        self.view = view
        
    def update_clock(self):
        # 1. Tick the timer (essential for countdown)
        self.model.tick_timer()

        # 2. Fetch all updated data from the Model
        time_str = self.model.get_time_string()
        date_str = self.model.get_date_string()
        format_status = self.model.get_format_status()
        
        # 3. Update the View
        if self.view:
            self.view.update_displays({
                "time_str": time_str,
                "date_str": date_str,
                "format_status": format_status,
                "alarm_status": self.model.get_alarm_status(),
                "timer_str": self.model.get_timer_string(),
                "timer_status": self.model.get_timer_status(),
                "tz_key": self.model.get_selected_timezone_key()
            })

        # 4. Sound Trigger (Alarm or Timer) - Using winsound.PlaySound() for custom WAV/system sounds
        # if self.model.get_just_triggered_status() or self.model.get_timer_just_finished_status():
        #     try:
        #         # --- TO CHANGE SOUND ---
        #         # A. Play a system alias (e.g., SystemExclamation)
        #         # winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS) 
                
        #         # B. Play a custom WAV file (RECOMMENDED FOR CUSTOM SOUNDS)
        #         # NOTE: Ensure 'alarm.wav' is in your script's directory, or use the absolute path.
        #         WAV_FILE = "C:\\path\\to\\your\\custom_alarm.wav" # CHANGE THIS PATH
                
        #         # Check if the file exists before attempting to play it
        #         if os.path.exists(WAV_FILE):
        #             winsound.PlaySound(WAV_FILE, winsound.SND_FILENAME)
        #         else:
        #             # Fallback to beep if custom file is missing
        #             winsound.Beep(1000, 1000) 

        #     except Exception as e:
        #         print(f"Winsound error: {e}")
        #         os.system('echo -e "\a"')

        if self.model.get_just_triggered_status() or self.model.get_timer_just_finished_status():
            try:
                # Simple 1-second beep at 1000 Hz
                winsound.Beep(500, 4000) 

            except Exception as e:
                print(f"Winsound error: {e}")
                os.system('echo -e "\a"')

        # 5. Reschedule the next tick and store the ID for safe shutdown
        if self.view:
            # FIX: Capture the ID returned by after() and store it in the View.
            new_after_id = self.view.after(1000, self.update_clock)
            self.view.after_id = new_after_id # <-- Store ID in the View instance
            
    # --- Data Retrieval Methods ---
    def get_timezone_keys(self):
        return self.model.get_timezone_keys()

    # --- Action Methods ---
    
    def toggle_format_action(self):
        self.model.toggle_format()
        
    def timezone_selected_action(self, event):
        selected_tz_key = self.view.frames["Time"].tz_var.get()
        self.model.set_timezone(selected_tz_key)

    def set_alarm_action(self):
        alarm_frame = self.view.frames["Alarm"]
    
        hour_raw = alarm_frame.alarm_hour_var.get().strip()
        minute_raw = alarm_frame.alarm_minute_var.get().strip()

        if not (hour_raw.isdigit() and minute_raw.isdigit()):
            messagebox.showerror("Invalid Input", "Alarm time must contain only digits.")
            alarm_frame.alarm_hour_var.set("00")
            alarm_frame.alarm_minute_var.set("00")
            return

        hour = int(hour_raw)
        minute = int(minute_raw)

        if not (0 <= hour <= 23):
            messagebox.showerror("Invalid Hour", "Hour must be between 00 and 23.")
            alarm_frame.alarm_hour_var.set("00")
            return

        if not (0 <= minute <= 59):
            messagebox.showerror("Invalid Minute", "Minutes must be between 00 and 59.")
            alarm_frame.alarm_minute_var.set("00")
            return

        self.model.set_alarm(hour, minute)



    def clear_alarm_action(self):
        alarm_frame = self.view.frames["Alarm"]
        self.model.clear_alarm()

        alarm_frame.alarm_hour_var.set("00")
        alarm_frame.alarm_minute_var.set("00")

    def set_timer_action(self):
        timer_frame = self.view.frames["Timer"]

        h_raw = timer_frame.timer_hour_var.get().strip()
        m_raw = timer_frame.timer_minute_var.get().strip()
        s_raw = timer_frame.timer_second_var.get().strip()

        if not (h_raw.isdigit() and m_raw.isdigit() and s_raw.isdigit()):
            messagebox.showerror("Invalid Input", "Timer fields must contain digits only.")
            timer_frame.timer_hour_var.set("00")
            timer_frame.timer_minute_var.set("00")
            timer_frame.timer_second_var.set("00")
            return

        hours = int(h_raw)
        minutes = int(m_raw)
        seconds = int(s_raw)

        if not (0 <= hours <= 99):
            messagebox.showerror("Invalid Hours", "Hours must be between 00 and 99.")
            timer_frame.timer_hour_var.set("00")
            return

        if not (0 <= minutes <= 59):
            messagebox.showerror("Invalid Minutes", "Minutes must be between 00 and 59.")
            timer_frame.timer_minute_var.set("00")
            return

        if not (0 <= seconds <= 59):
            messagebox.showerror("Invalid Seconds", "Seconds must be between 00 and 59.")
            timer_frame.timer_second_var.set("00")
            return

        self.model.set_timer(hours, minutes, seconds)

    def start_stop_timer_action(self):
        status = self.model.get_timer_status()
        if status == "RUNNING":
            self.model.stop_timer()
        elif status in ["READY", "TIMER FINISHED!"]:
            self.model.start_timer()

    def reset_timer_action(self):
        timer_frame = self.view.frames["Timer"]
        self.model.reset_timer()

        timer_frame.timer_hour_var.set("00")
        timer_frame.timer_minute_var.set("00")
        timer_frame.timer_second_var.set("00")