# # clock_model.py
# import datetime
# import pytz

# class ClockModel:
#     COMMON_TIMEZONES = {
#         "Local Time": None, 
#         "UTC": "UTC",
#         "EST (New York)": "America/New_York",
#         "PST (Los Angeles) - 3 ": "America/Los_Angeles",
#         "CET (Paris)": "Europe/Paris",
#         "JST (Tokyo)": "Asia/Tokyo"
#     }
    
#     def __init__(self):
#         self._is_24_hour_format = True
#         self._selected_timezone_key = "Local Time"
#         self._selected_timezone = None 
        
#         self._alarm_time = None 
#         self._alarm_set = False
#         self._alarm_triggered = False
#         self._just_triggered = False 

#         self._timer_total_seconds = 0
#         self._timer_remaining_seconds = 0
#         self._timer_running = False
#         self._timer_finished = False
#         self._timer_just_finished = False

#     def toggle_format(self):
#         """Toggles between 12-hour and 24-hour format."""
#         self._is_24_hour_format = not self._is_24_hour_format

#     def get_time_string(self):
#         """Returns the current time string based on the selected format and timezone."""
#         if self._selected_timezone:
#             try:
#                 tz = pytz.timezone(self._selected_timezone)
#                 now = datetime.datetime.now(tz)
#             except pytz.exceptions.UnknownTimeZoneError:
#                 now = datetime.datetime.now()
#         else:
#             now = datetime.datetime.now()

#         if self._is_24_hour_format:
#             time_str = now.strftime("%H:%M:%S")
#         else:
#             time_str = now.strftime("%I:%M:%S %p")
            
#         self.check_alarm(now)
        
#         return time_str

#     def get_alarm_status(self):
#         """Returns the status of the alarm."""
#         if self._alarm_triggered:
#             return "ALARM TRIGGERED!"
#         elif self._alarm_set:
#             alarm_str = self._alarm_time.strftime("%H:%M")
#             return f"ALARM SET: {alarm_str}"
#         else:
#             return "ALARM OFF"

#     def check_alarm(self, current_datetime):
#         """Checks if the current time matches the set alarm time."""
#         self._just_triggered = False
#         if self._alarm_set and not self._alarm_triggered:
#             current_time = current_datetime.time()
#             if current_time.hour == self._alarm_time.hour and current_time.minute == self._alarm_time.minute:
#                 self._alarm_triggered = True
#                 self._just_triggered = True 
                
#     def set_alarm(self, hour, minute):
#         """Sets the alarm time."""
#         try:
#             self._alarm_time = datetime.time(hour, minute)
#             self._alarm_set = True
#             self._alarm_triggered = False
#         except ValueError:
#             pass

#     def clear_alarm(self):
#         """Clears the alarm."""
#         self._alarm_set = False
#         self._alarm_time = None
#         self._alarm_triggered = False
#         self._just_triggered = False
#         self.hour = 0
#         self.minute = 0
        

        

#     # --- Timer Methods ---

#     def set_timer(self, hours, minutes, seconds):
#         """Sets the timer duration in seconds."""
#         self._timer_total_seconds = hours * 3600 + minutes * 60 + seconds
#         self._timer_remaining_seconds = self._timer_total_seconds
#         self._timer_running = False
#         self._timer_finished = False
#         self._timer_just_finished = False

#     def start_timer(self):
#         """Starts the countdown timer."""
#         if self._timer_remaining_seconds > 0 and not self._timer_running:
#             self._timer_running = True
#             self._timer_finished = False
#             self._timer_just_finished = False

#     def stop_timer(self):
#         """Stops the countdown timer."""
#         self._timer_running = False

#     def reset_timer(self):
#         """Resets the timer to its initial duration."""
#         self._timer_total_seconds = 0
#         self._timer_remaining_seconds = self._timer_total_seconds
#         self._timer_running = False
#         self._timer_finished = False
#         self._timer_just_finished = False

#     def tick_timer(self):
#         """Decrements the timer by one second if running."""
#         self._timer_just_finished = False
#         if self._timer_running and self._timer_remaining_seconds > 0:
#             self._timer_remaining_seconds -= 1
#             if self._timer_remaining_seconds == 0:
#                 self._timer_running = False
#                 self._timer_finished = True
#                 self._timer_just_finished = True

#     def get_timer_string(self):
#         """Returns the remaining time as an HH:MM:SS string."""
#         seconds = self._timer_remaining_seconds
#         hours = seconds // 3600
#         minutes = (seconds % 3600) // 60
#         seconds = seconds % 60
#         return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

#     def get_timer_status(self):
#         """Returns the status of the timer."""
#         if self._timer_finished:
#             return "TIMER FINISHED!"
#         elif self._timer_running:
#             return "RUNNING"
#         elif self._timer_total_seconds > 0:
#             return "READY"
#         else:
#             return "OFF"

#     def get_timer_just_finished_status(self):
#         """Returns True if the timer just finished in this cycle."""
#         return self._timer_just_finished

#     def get_just_triggered_status(self):
#         """Returns True if the alarm was just triggered in this cycle."""
#         return self._just_triggered

#     def get_date_string(self):
#         """Returns the current date and day of the week string for the selected timezone."""
#         if self._selected_timezone:
#             try:
#                 tz = pytz.timezone(self._selected_timezone)
#                 now = datetime.datetime.now(tz)
#             except pytz.exceptions.UnknownTimeZoneError:
#                 now = datetime.datetime.now()
#         else:
#             now = datetime.datetime.now()
            
#         return now.strftime("%a, %b %d, %Y")

#     def get_format_status(self):
#         """Returns a string indicating the current format."""
#         return "24-Hour" if self._is_24_hour_format else "12-Hour"

#     def get_timezone_keys(self):
#         """Returns the display names of the available timezones."""
#         return list(self.COMMON_TIMEZONES.keys())

#     def get_selected_timezone_key(self):
#         """Returns the display name of the currently selected timezone."""
#         return self._selected_timezone_key

#     def set_timezone(self, tz_key):
#         """Sets the new timezone based on the display key."""
#         self._selected_timezone_key = tz_key
#         self._selected_timezone = self.COMMON_TIMEZONES.get(tz_key)

