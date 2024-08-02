import pyautogui, time, threading, ctypes, sqlite3
import customtkinter as ctk

stop_flooding = threading.Event()

def focus_and_type(phrase):
    hwnd = ctypes.windll.user32.FindWindowW(None, "Habbo Hotel: Origins")
    if not hwnd:
        print("Habbo window not found.")
        return
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)

    words = phrase.split()
    current_message = ""

    for word in words:
        if stop_flooding.is_set():
            break
        if len(current_message) + len(word) + 1 <= 60:
            current_message += " " + word if current_message else word
        else:
            pyautogui.typewrite(current_message)
            pyautogui.press("enter")
            time.sleep(0.5)
            current_message = word

    if not stop_flooding.is_set() and current_message:
        pyautogui.typewrite(current_message)
        pyautogui.press("enter")

def on_keybind(key):
    global stop_flooding
    stop_flooding.clear()
    phrase = text_inputs[key].get("1.0", "end-1c")
    thread = threading.Thread(target=focus_and_type, args=(phrase,))
    thread.start()

def stop_flood():
    stop_flooding.set()

def save_texts():
    conn = sqlite3.connect('habbo_flooder_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS texts (key TEXT PRIMARY KEY, text TEXT)''')
    for key, text_input in text_inputs.items():
        text = text_input.get("1.0", "end-1c")
        cursor.execute('''INSERT OR REPLACE INTO texts (key, text) VALUES (?, ?)''', (key, text))
    conn.commit()
    conn.close()

def load_texts():
    conn = sqlite3.connect('habbo_flooder_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS texts (key TEXT PRIMARY KEY, text TEXT)''')
    cursor.execute('''SELECT key, text FROM texts''')
    for row in cursor.fetchall():
        key, text = row
        if key in text_inputs:
            text_inputs[key].insert("1.0", text)
    conn.close()

# Create the GUI
app = ctk.CTk()
app.title("Habbo Flooder")

# Adjusting window size and padding
app.geometry("600x500")
app.grid_columnconfigure(0, weight=1)

title_label = ctk.CTkLabel(app, text="Habbo Flooder", font=("Arial", 20))
title_label.pack(pady=20)

tab_control = ctk.CTkTabview(app)
tab_control.pack(expand=1, fill="both", padx=20, pady=10)

text_inputs = {}
keybinds = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11"]
stop_key = "F12"

for key in keybinds:
    tab = tab_control.add(key)
    frame = ctk.CTkFrame(tab)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    label = ctk.CTkLabel(frame, text=f"Enter the phrase to flood for {key}:")
    label.pack(pady=10)

    text_input = ctk.CTkTextbox(frame, width=400, height=150)
    text_input.pack(pady=10)

    button = ctk.CTkButton(frame, text=f"Start Flooding ({key})", command=lambda k=key: on_keybind(k))
    button.pack(pady=10)
    
    text_inputs[key] = text_input

    app.bind(f"<{key}>", lambda event, k=key: on_keybind(k))

# Bind the stop function to a key
app.bind(f"<{stop_key}>", lambda event: stop_flood())
stop_label = ctk.CTkLabel(app, text=f"Press {stop_key} to stop flooding.")
stop_label.pack(pady=20)

load_texts()

app.protocol("WM_DELETE_WINDOW", lambda: (save_texts(), app.destroy()))
app.mainloop()
