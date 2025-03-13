import sys
import subprocess
import time
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox

class VirtualMonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.monitor_enabled = self.is_virtual_monitor_active()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Virtual Monitor Control")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.enable_button = QPushButton("Enable Virtual Monitor", self)
        self.enable_button.clicked.connect(self.enable_virtual_monitor)
        layout.addWidget(self.enable_button)

        self.disable_button = QPushButton("Disable Virtual Monitor", self)
        self.disable_button.clicked.connect(self.disable_virtual_monitor)
        layout.addWidget(self.disable_button)

        self.setLayout(layout)
        self.update_buttons()

    def update_buttons(self):
        """Show only the correct button based on the monitor state"""
        self.enable_button.setVisible(not self.monitor_enabled)
        self.disable_button.setVisible(self.monitor_enabled)

    def is_virtual_monitor_active(self):
        """Check if the virtual monitor is currently enabled"""
        try:
            result = subprocess.run(["xrandr"], capture_output=True, text=True)
            return "VIRTUAL1 connected" in result.stdout
        except Exception:
            return False

    def enable_virtual_monitor(self):
        if self.monitor_enabled:
            QMessageBox.information(self, "Info", "Virtual monitor is already enabled!")
            return

        try:
            subprocess.run(["xrandr"], check=True)  # Ensure xrandr is up to date
            subprocess.run(["xrandr", "--newmode", "1440x900_60.00", "106.50", "1440", "1528", "1672", "1904", "900", "903", "909", "934", "-HSync", "+Vsync"], check=False)
            subprocess.run(["xrandr", "--addmode", "VIRTUAL1", "1440x900_60.00"], check=True)
            subprocess.run(["xrandr", "--output", "VIRTUAL1", "--mode", "1440x900_60.00"], check=True)
            subprocess.run(["xrandr", "--output", "VIRTUAL1", "--scale", "0.7x0.7"], check=True)

            if self.check_deskreen_status():
                subprocess.run(["pkill", "deskreen"])  # Ensure Deskreen is closed before re-enabling it

            self.adjust_mouse_speed()
            
            self.monitor_enabled = self.is_virtual_monitor_active()
            self.update_buttons()
            QMessageBox.information(self, "Success", "Virtual monitor enabled successfully!")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to enable virtual monitor:\n{e}")

    def disable_virtual_monitor(self):
        if not self.monitor_enabled:
            QMessageBox.information(self, "Info", "Virtual monitor is already disabled!")
            return

        try:
            # Ensure Deskreen is properly closed before disabling the monitor
            if self.check_deskreen_status():
                subprocess.run(["pkill", "deskreen"])  # Close Deskreen before disabling the virtual monitor

            # Disable the virtual monitor
            subprocess.run(["xrandr", "--output", "VIRTUAL1", "--off"], check=True)
            subprocess.run(["xrandr", "--delmode", "VIRTUAL1", "1440x900_60.00"], check=True)

            # Ensure the primary monitor is re-enabled correctly
            subprocess.run(["xrandr", "--output", "eDP-1", "--auto"], check=True)
            subprocess.run(["xrandr", "--dpi", "96"], check=True)
            subprocess.run(["xrandr", "--output", "eDP-1", "--primary"], check=True)
            
            time.sleep(2)  # Allow system to process the change
            
            self.monitor_enabled = self.is_virtual_monitor_active()
            self.update_buttons()
            QMessageBox.information(self, "Success", "Virtual monitor disabled successfully!")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to disable virtual monitor:\n{e}")

    def get_mouse_device_name(self):
        """Dynamically finds the first available mouse device"""
        try:
            result = subprocess.run(["xinput", "list"], capture_output=True, text=True)
            match = re.search(r"↳ (.+?Mouse.*?)\s+id=(\d+)", result.stdout)
            if match:
                return match.group(1)
        except Exception:
            pass
        return None

    def adjust_mouse_speed(self):
        """Adjusts mouse speed dynamically based on the detected device"""
        mouse_device = self.get_mouse_device_name()
        if not mouse_device:
            QMessageBox.warning(self, "Warning", "Could not detect mouse device. Skipping speed adjustment.")
            return

        try:
            subprocess.run(["xinput", "--set-prop", mouse_device, "Coordinate Transformation Matrix",
                            "1.42", "0", "0", "0", "1.42", "0", "0", "0", "1"], check=True)
        except subprocess.CalledProcessError:
            QMessageBox.warning(self, "Warning", "Failed to adjust mouse speed. You may experience slow cursor movement.")

    def check_deskreen_status(self):
        """Checks if Deskreen is active and can be restarted"""
        try:
            result = subprocess.run(["ps", "-A"], capture_output=True, text=True)
            if "deskreen" in result.stdout:
                return True
            return False
        except Exception:
            return False

def main():
    app = QApplication(sys.argv)
    window = VirtualMonitorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
