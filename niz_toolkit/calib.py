import logging
import tkinter as tk

from .const import VID
from .keyboard import Keyboard, find_device

logger = logging.getLogger(__name__)


class LockButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, text="Lock", command=self.toggle, **kwargs)
        self.locked = False

    def toggle(self):
        if self.locked:
            self.unlock()
            self.config(text="Lock")
            self.label_status.config(text="Status: Unlocked")
            self.btn_calib_init.config(state=tk.DISABLED)
            self.btn_calib_one.config(state=tk.DISABLED)
        else:
            self.lock()
            self.config(text="Unlock")
            self.label_status.config(text="Status: Locked")
            self.btn_calib_init.config(state=tk.NORMAL)
            self.btn_calib_one.config(state=tk.NORMAL)
        self.locked = not self.locked

    def lock(self):
        raise NotImplementedError

    def unlock(self):
        raise NotImplementedError


class App:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Niz calibration tool")

        self.label_model = tk.Label(self.master, text="Model: Not found")
        self.label_ver = tk.Label(self.master, text="Firmware: Unknown")
        self.label_status = tk.Label(self.master, text="Status: Unknown")
        self.btn_lock = LockButton(self.master, state=tk.DISABLED)
        self.btn_calib_init = tk.Button(
            text="Calibrate init state", command=self.calib_init, state=tk.DISABLED
        )
        self.btn_calib_one = tk.Button(
            text="Calibrate one key", command=self.calib_press, state=tk.DISABLED
        )

        self.btn_lock.label_status = self.label_status
        self.btn_lock.btn_calib_init = self.btn_calib_init
        self.btn_lock.btn_calib_one = self.btn_calib_one

        self.label_model.pack()
        self.label_ver.pack()
        self.btn_lock.label_status.pack()
        self.btn_lock.pack()
        self.btn_calib_init.pack()
        self.btn_calib_one.pack()

        PID = find_device()
        if PID:
            self.kbd = Keyboard(PID)
            self.label_model.config(text=f"Model: {self.kbd.model}")
            self.label_ver.config(text=f"Firmware: {self.kbd.version}")
            self.label_status.config(text="Status: Unlockd")
            self.btn_lock.config(state=tk.NORMAL)
            self.btn_lock.lock = self.lock
            self.btn_lock.unlock = self.unlock
        else:
            self.kbd = None
            logger.error("No device found.")

    def lock(self):
        self.kbd.lock()

    def unlock(self):
        self.kbd.unlock()

    def calib_init(self):
        self.kbd.calib_init()

    def calib_press(self):
        self.kbd.calib_press()

    def close(self):
        logger.info("App closed.")
        if self.kbd:
            if self.kbd.locked:
                self.kbd.unlock()
            self.kbd.close()


def calib(args):
    root = tk.Tk()
    root.geometry("300x200")
    # frm = tk.ttk.Frame(root, padding=10)

    app = App(root)

    def on_closing():
        app.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
