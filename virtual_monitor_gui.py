import sys
import subprocess
import time
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
        """ Show only the correct button based on the monitor state """
        self.enable_button.setVisible(not self.monitor_enabled)
        self.disable_button.setVisible(self.monitor_enabled)

    def is_virtual_monitor_active(self):
        """ Check if the virtual monitor is currently enabled """
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
            subprocess.run(["xrandr", "--newmode", "1112x834_60.00", "75.81", "1112", "1168", "1288", "1464", "834", "835", "838", "863", "-HSync", "+Vsync"], check=False)
            subprocess.run(["xrandr", "--addmode", "VIRTUAL1", "1112x834_60.00"], check=True)
            subprocess.run(["xrandr", "--output", "VIRTUAL1", "--mode", "1112x834_60.00"], check=True)

            # Ensure the monitor state is updated correctly
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
            # Turn off the virtual monitor
            subprocess.run(["xrandr", "--output", "VIRTUAL1", "--off"], check=True)

            # Remove the virtual mode safely
            subprocess.run(["xrandr", "--delmode", "VIRTUAL1", "1112x834_60.00"], check=True)

            # Reset display configuration to prevent freeze
            subprocess.run(["xrandr", "--output", "eDP-1", "--auto"], check=True)  # Adjust for your primary monitor
            subprocess.run(["xrandr", "--dpi", "96"], check=True)  # Reset DPI
            subprocess.run(["xrandr", "--output", "eDP-1", "--primary"], check=True)

            # Ensure the monitor state is updated correctly
            self.monitor_enabled = self.is_virtual_monitor_active()
            self.update_buttons()

            QMessageBox.information(self, "Success", "Virtual monitor disabled successfully!")

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to disable virtual monitor:\n{e}")

    def retry_command(self, command, retries=3, delay=2):
        """ Retry the command a specified number of times with delay in case of failure """
        for _ in range(retries):
            try:
                subprocess.run(command, check=True)
                return True
            except subprocess.CalledProcessError:
                time.sleep(delay)
        return False

def main():
    app = QApplication(sys.argv)
    window = VirtualMonitorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
~                     
