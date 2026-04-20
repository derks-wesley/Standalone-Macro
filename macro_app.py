import json
import platform
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pynput import keyboard, mouse


class MacroStudio:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Macro Studio (G Hub-achtig)")
        self.root.geometry("760x500")

        self.events = []
        self.recording = False
        self.playing = False
        self.record_start = 0.0
        self.k_listener = None
        self.m_listener = None

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Naam macro:").pack(side="left")
        self.name_var = tk.StringVar(value="Nieuwe Macro")
        ttk.Entry(top, textvariable=self.name_var, width=30).pack(side="left", padx=8)

        self.btn_record = ttk.Button(top, text="Opnemen starten", command=self.toggle_record)
        self.btn_record.pack(side="left", padx=4)

        self.btn_play = ttk.Button(top, text="Afspelen", command=self.play_macro)
        self.btn_play.pack(side="left", padx=4)

        ttk.Button(top, text="Opslaan", command=self.save_macro).pack(side="left", padx=4)
        ttk.Button(top, text="Laden", command=self.load_macro).pack(side="left", padx=4)
        ttk.Button(top, text="Lijst legen", command=self.clear_events).pack(side="left", padx=4)

        settings = ttk.LabelFrame(self.root, text="Instellingen", padding=10)
        settings.pack(fill="x", padx=10, pady=(0, 10))

        self.loop_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings, text="Herhalen (loop)", variable=self.loop_var).grid(row=0, column=0, sticky="w")

        ttk.Label(settings, text="Herhalingen:").grid(row=0, column=1, sticky="e")
        self.repeat_var = tk.IntVar(value=1)
        ttk.Spinbox(settings, from_=1, to=999, textvariable=self.repeat_var, width=8).grid(row=0, column=2, padx=5)

        ttk.Label(settings, text="Speed multiplier:").grid(row=0, column=3, sticky="e")
        self.speed_var = tk.DoubleVar(value=1.0)
        ttk.Spinbox(settings, from_=0.1, to=5.0, increment=0.1, textvariable=self.speed_var, width=8).grid(row=0, column=4, padx=5)

        self.status_var = tk.StringVar(value="Gereed")
        ttk.Label(self.root, textvariable=self.status_var, padding=(10, 0)).pack(anchor="w")

        columns = ("tijd", "type", "actie")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("tijd", text="Tijd (s)")
        self.tree.heading("type", text="Type")
        self.tree.heading("actie", text="Actie")
        self.tree.column("tijd", width=90, anchor="center")
        self.tree.column("type", width=120, anchor="center")
        self.tree.column("actie", width=500, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def _now(self):
        return time.perf_counter() - self.record_start

    def toggle_record(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        if self.playing:
            return
        self.events.clear()
        self.refresh_tree()
        self.record_start = time.perf_counter()
        self.recording = True

        self.k_listener = keyboard.Listener(on_press=self._on_key_press, on_release=self._on_key_release)
        self.m_listener = mouse.Listener(on_click=self._on_click, on_scroll=self._on_scroll)
        self.k_listener.start()
        self.m_listener.start()

        self.status_var.set("Opname bezig... (let op: globale input wordt vastgelegd)")
        self.btn_record.configure(text="Opnemen stoppen")

    def stop_recording(self):
        self.recording = False
        if self.k_listener:
            self.k_listener.stop()
        if self.m_listener:
            self.m_listener.stop()
        self.status_var.set(f"Opname gestopt. {len(self.events)} events vastgelegd.")
        self.btn_record.configure(text="Opnemen starten")

    def _add_event(self, event):
        if not self.recording:
            return
        self.events.append(event)
        self.tree.insert("", "end", values=(f"{event['time']:.3f}", event["kind"], event["detail"]))

    def _key_str(self, key):
        if hasattr(key, "char") and key.char is not None:
            return key.char
        return str(key)

    def _on_key_press(self, key):
        self._add_event({"time": self._now(), "kind": "keyboard", "action": "press", "key": self._key_str(key), "detail": f"druk {self._key_str(key)}"})

    def _on_key_release(self, key):
        self._add_event({"time": self._now(), "kind": "keyboard", "action": "release", "key": self._key_str(key), "detail": f"los {self._key_str(key)}"})

    def _on_click(self, x, y, button, pressed):
        act = "press" if pressed else "release"
        self._add_event({
            "time": self._now(),
            "kind": "mouse_click",
            "action": act,
            "x": x,
            "y": y,
            "button": str(button),
            "detail": f"{act} {button} @ ({x},{y})",
        })

    def _on_scroll(self, x, y, dx, dy):
        self._add_event({"time": self._now(), "kind": "mouse_scroll", "action": "scroll", "x": x, "y": y, "dx": dx, "dy": dy, "detail": f"scroll dx={dx}, dy={dy} @ ({x},{y})"})

    def clear_events(self):
        if self.recording:
            messagebox.showwarning("Actie geblokkeerd", "Stop eerst de opname.")
            return
        self.events.clear()
        self.refresh_tree()
        self.status_var.set("Eventlijst geleegd")

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for e in self.events:
            self.tree.insert("", "end", values=(f"{e['time']:.3f}", e["kind"], e["detail"]))

    def save_macro(self):
        if not self.events:
            messagebox.showinfo("Geen data", "Er zijn nog geen events om op te slaan.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Macro JSON", "*.json")])
        if not path:
            return
        data = {"name": self.name_var.get().strip() or "Macro", "events": self.events}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.status_var.set(f"Macro opgeslagen: {path}")

    def load_macro(self):
        if self.recording or self.playing:
            messagebox.showwarning("Actie geblokkeerd", "Stop opnemen/afspelen voordat je laadt.")
            return
        path = filedialog.askopenfilename(filetypes=[("Macro JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.name_var.set(data.get("name", "Macro"))
            self.events = data.get("events", [])
            self.refresh_tree()
            self.status_var.set(f"Macro geladen: {path} ({len(self.events)} events)")
        except Exception as e:
            messagebox.showerror("Fout", f"Kon macro niet laden:\n{e}")

    def play_macro(self):
        if self.recording:
            messagebox.showwarning("Actie geblokkeerd", "Stop eerst de opname.")
            return
        if self.playing:
            return
        if not self.events:
            messagebox.showinfo("Geen data", "Er zijn geen events om af te spelen.")
            return

        t = threading.Thread(target=self._play_worker, daemon=True)
        t.start()

    def _play_worker(self):
        self.playing = True
        self.status_var.set("Macro wordt afgespeeld...")

        k_ctrl = keyboard.Controller()
        m_ctrl = mouse.Controller()
        repeat = self.repeat_var.get() if not self.loop_var.get() else float("inf")
        speed = max(0.1, self.speed_var.get())

        try:
            cycle = 0
            while cycle < repeat:
                prev_t = 0.0
                for event in self.events:
                    wait = max(0.0, (event["time"] - prev_t) / speed)
                    time.sleep(wait)
                    prev_t = event["time"]

                    if event["kind"] == "keyboard":
                        key_obj = self._decode_key(event["key"])
                        if event["action"] == "press":
                            k_ctrl.press(key_obj)
                        else:
                            k_ctrl.release(key_obj)

                    elif event["kind"] == "mouse_click":
                        m_ctrl.position = (event["x"], event["y"])
                        btn = self._decode_button(event["button"])
                        if event["action"] == "press":
                            m_ctrl.press(btn)
                        else:
                            m_ctrl.release(btn)

                    elif event["kind"] == "mouse_scroll":
                        m_ctrl.position = (event["x"], event["y"])
                        m_ctrl.scroll(event.get("dx", 0), event.get("dy", 0))

                cycle += 1
                if self.loop_var.get():
                    cycle = 0
        except Exception as e:
            self.status_var.set(f"Afspelen mislukt: {e}")
        finally:
            self.playing = False
            if "mislukt" not in self.status_var.get():
                self.status_var.set("Afspelen klaar")

    def _decode_key(self, s):
        if s.startswith("Key."):
            name = s.split(".", 1)[1]
            return getattr(keyboard.Key, name, s)
        return s

    def _decode_button(self, s):
        if s.startswith("Button."):
            name = s.split(".", 1)[1]
            return getattr(mouse.Button, name, mouse.Button.left)
        return mouse.Button.left


if __name__ == "__main__":
    if platform.system() == "Windows":
        try:
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("standalone.macro.studio")
        except Exception:
            pass

    root = tk.Tk()
    app = MacroStudio(root)
    root.mainloop()
