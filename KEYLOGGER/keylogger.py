# consented_key_recorder.py
# Run with: python3 consented_key_recorder.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime

LOGFILE = "keystrokes_consent_log.txt"

def ask_consent():
    msg = (
        "This application records keystrokes while this window is focused.\n\n"
        f"Data will be stored locally in:\n  {LOGFILE}\n\n"
        "Do you consent to recording your keystrokes?"
    )
    return messagebox.askyesno("Consent required", msg)

def log_key(event):
    # Identify printable vs non-printable keys
    char = event.char if event.char and event.char.isprintable() else f"<{event.keysym}>"
    timestamp = datetime.utcnow().isoformat() + "Z"
    line = f"{timestamp}\t{char}\n"

    # Append to log file
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(line)

    # Only manually insert *non-printable* keys (printables already appear automatically)
    if not (event.char and event.char.isprintable()):
        txt.insert(tk.END, f"{char}")
        txt.see(tk.END)

def on_close():
    if messagebox.askokcancel("Quit", "Stop recording and close?"):
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Consented Keystroke Recorder")
    root.geometry("700x400")

    consent = ask_consent()
    if not consent:
        messagebox.showinfo("No consent", "Consent not given. Exiting.")
        root.destroy()
    else:
        tk.Label(
            root,
            text="Recording keystrokes while this window is focused.\nClose window to stop.",
            pady=8
        ).pack()

        txt = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=18)
        txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        txt.focus_set()

        # Bind key press events only to the text box
        txt.bind("<Key>", log_key)

        root.protocol("WM_DELETE_WINDOW", on_close)
        root.mainloop()
