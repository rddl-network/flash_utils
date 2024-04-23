import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import serial.tools.list_ports


class FlasherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ESP Flasher")
        self.geometry("500x500")
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        # ESP Type Selection
        self.esp_type_var = tk.StringVar(value="esp32c3")  # Preselect esp32c3
        tk.Label(main_frame, text="Select ESP Type:").grid(row=0, column=0)

        esp_types = [("esp32", "esp32"), ("esp32c3", "esp32c3")]
        for i, (esp_type, value) in enumerate(esp_types, start=1):
            tk.Radiobutton(main_frame, text=esp_type, variable=self.esp_type_var, value=value).grid(row=i, column=0, columnspan=2, sticky="w")

        # Firmware File Selection
        tk.Label(main_frame, text="Firmware File:").grid(row=3, column=0, columnspan=2, pady=(20, 0))
        self.firmware_file_entry = tk.Entry(main_frame)
        self.firmware_file_entry.grid(row=4, column=0, pady=(5, 5), sticky="ew")
        tk.Button(main_frame, text="Browse", command=self.browse_file).grid(row=4, column=1, pady=(5, 5), padx=(5, 0),
                                                                            sticky="ew")
        # Label to display the selected file
        self.selected_file_label = tk.Label(main_frame, text="No file selected")
        self.selected_file_label.grid(row=5, column=0, columnspan=2, pady=(5, 20))

        # USB Device Selection
        self.device_frame = tk.LabelFrame(main_frame, text="Select USB Device")
        self.device_frame.grid(row=6, column=0, columnspan=2, pady=(10, 10), sticky="ew")

        self.selected_device = tk.StringVar()
        self.device_radio_buttons = []

        tk.Button(main_frame, text="Refresh List", command=self.populate_devices).grid(row=7, column=0, columnspan=2,
                                                                                       pady=(0, 20), sticky="ew")

        tk.Button(main_frame, text="Flash ESP", command=self.flash_esp).grid(row=8, column=0, columnspan=2,
                                                                             pady=(0, 10), sticky="ew")

        self.output_text = tk.Text(main_frame, height=8, state='disabled')
        self.output_text.grid(row=9, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        main_frame.columnconfigure(0, weight=1)

        self.populate_devices()

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.firmware_file_entry.delete(0, tk.END)
            self.firmware_file_entry.insert(0, file_path)
            self.selected_file_label.config(text=f"Selected: {file_path.split('/')[-1]}")

    def populate_devices(self):
        for rb in self.device_radio_buttons:
            rb.destroy()
        self.device_radio_buttons.clear()

        devices = serial.tools.list_ports.comports()
        device_list = [device.device for device in devices]

        if not device_list:
            tk.Label(self.device_frame, text="No devices found").pack()
            return

        for device in device_list:
            rb = tk.Radiobutton(self.device_frame, text=device, variable=self.selected_device, value=device)
            rb.pack(anchor='w')
            self.device_radio_buttons.append(rb)

    def setup_paths(self, esp_type):
        """Setup necessary file paths based on ESP type."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if esp_type not in ["esp32", "esp32c3"]:
            messagebox.showerror("Error", f"Unsupported ESP type: {esp_type}")
            return None

        tasmota32_type = "tasmota32" if esp_type == "esp32" else "tasmota32c3"

        paths = {
            "bootloader_file": os.path.join(script_dir, esp_type, "bootloader.bin"),
            "partitions_file": os.path.join(script_dir, esp_type, "partitions.bin"),
            "safeboot_file": os.path.join(script_dir, esp_type, tasmota32_type + "-safeboot.bin"),
            "boot_app0_file": os.path.join(script_dir, "boot_app0.bin")
        }

        # Check if files exist
        missing_files = [path for path in paths.values() if not os.path.exists(path)]
        if missing_files:
            messagebox.showerror("Error", "One or more required files are missing: " + ", ".join(missing_files))
            return None

        return paths

    def flash_esp(self):
        esp_type = self.esp_type_var.get().strip()
        firmware_file = self.firmware_file_entry.get().strip()
        selected_device = self.selected_device.get()

        # Validate input
        if not esp_type or not firmware_file or not selected_device:
            messagebox.showerror("Error", "ESP type, firmware file, and USB device are required.")
            return

        # Setup paths based on ESP type
        paths = self.setup_paths(esp_type)
        if not paths:
            return

        # Attempt to flash the ESP
        self.execute_flash_command(paths, firmware_file, selected_device)

    # Updated to include selected_device in execute_flash_command
    def execute_flash_command(self, paths, firmware_file, selected_device):
        """Execute the flashing command with the selected device."""
        command = [
            "esptool.py", "-p", selected_device, "-b", "460800", "--before", "default_reset",
            "--after", "hard_reset", "--chip", "auto", "write_flash", "--flash_mode", "dio",
            "--flash_size", "detect", "--flash_freq=keep", "0x0000", paths["bootloader_file"],
            "0x8000", paths["partitions_file"], "0xe000", paths["boot_app0_file"],
            "0x10000", paths["safeboot_file"], "0xe0000", firmware_file
        ]

        try:
            subprocess.run(command, check=True)
            print("Flashing successful!")
        except subprocess.CalledProcessError as e:
            print(f"Error during flashing: {e}")


if __name__ == "__main__":
    app = FlasherApp()
    app.mainloop()
