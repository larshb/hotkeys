import tkinter as tk

from utilities import Actions


class Popup(tk.Toplevel):
    def __init__(self, master, actions: Actions):
        super().__init__(master)

        self.actions = actions

        self.overrideredirect(True)
        self.configure(bg="black")
        self.wm_attributes("-alpha", 0.75)

        self.width = 10
        self.height = 10

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (self.width / 2))
        y = int((screen_height / 2) - (self.height / 2))
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

        frame = tk.Frame(self, bg="black")
        frame.pack(pady=5, padx=15, fill="x")

        for key, (desc, _, _) in self.actions.actions.items():
            row = tk.Frame(frame, bg="black")
            row.pack(fill="x", pady=4)

            key_label = tk.Label(
                row,
                text=key.upper(),
                font=("Consolas", 14, "bold"),
                relief="raised",
                borderwidth=4,
                width=3,
                height=1,
                bg="#ddd",
                fg="#000",
            )
            key_label.pack(side="left")

            desc_label = tk.Label(
                row, text=desc, font=("Arial", 14), anchor="w", bg="black", fg="white"
            )
            desc_label.pack(side="left", padx=15)

        self.update_idletasks()  # process geometry changes
        self.geometry("")  # reset Toplevel size to fit content


class AutomateGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clipboard Automation Root")
        self.root.configure(bg="black")
        self.root.geometry(
            "400x400+50+50"
        )  # keep visible, can be resized or repositioned

        # Create dimming overlay as frameless Toplevel
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.overlay = tk.Toplevel(self.root)
        self.overlay.overrideredirect(True)
        self.overlay.geometry(f"{screen_width}x{screen_height}+0+0")
        self.overlay.configure(bg="black")
        self.overlay.lift()
        self.overlay.wm_attributes("-alpha", 0.5)

        # Create popup Toplevel for cheat sheet UI, parented to overlay to keep on top
        self.popup = Popup(self.overlay, Actions(self))
        self.popup.lift()

        # Bind keys on root window to capture globally within app
        self.root.bind_all("<Key>", self.key_pressed)

        # Hide the root window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width, height = 1, 1
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Default to closing after any keypress
        self.close_on_keypress = True

    def key_pressed(self, event):
        key = event.char.lower()
        callback = self.popup.actions.get_callback(key)
        if callback:
            callback()
        if self.close_on_keypress:
            self.close_app()

    def close_app(self):
        self.overlay.destroy()
        self.root.destroy()

    def run(self):
        # Do not withdraw root window so it can capture keys
        self.root.mainloop()


if __name__ == "__main__":
    app = AutomateGUI()
    app.run()
