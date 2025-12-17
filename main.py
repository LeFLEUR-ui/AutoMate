import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,

                             QFrame, QLabel, QPushButton, QDesktopWidget,

                             QStackedWidget, QSizePolicy)

from PyQt5.QtCore import Qt

from components.dashboard_page import DashboardPage
from components.files_browser_page  import FileBrowserUI

class AutoMateUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoMate Dashboard")
        self.resize(1280, 800)
        self.setStyleSheet("background-color: #F8FAFC; font-family: 'Segoe UI', sans-serif;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.nav_buttons = []
        self.setup_sidebar()
        
        self.stack = QStackedWidget()
        
        self.stack.addWidget(DashboardPage()) 
        self.stack.addWidget(FileBrowserUI())
        # self.stack.addWidget(RulesPage())
        # self.stack.addWidget(ActivityPage())
        
        self.main_layout.addWidget(self.stack)
        self.center()

    def setup_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("background-color: white; border-right: 1px solid #E2E8F0;")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(24, 40, 24, 24)

        logo = QLabel("⚡ AutoMate")
        logo.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; margin-bottom: 32px;")
        layout.addWidget(logo)

        nav_items = ["Dashboard", "Files", "Automation Rules", "Activity Log"]
        for i, text in enumerate(nav_items):
            btn = QPushButton(f"  {text}")
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(self.make_switch_func(i))
            
            if i == 0: btn.setChecked(True)
            self.apply_button_style(btn)
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        layout.addStretch()
        self.main_layout.addWidget(sidebar)

    def make_switch_func(self, index):
        def switch():
            self.stack.setCurrentIndex(index)
            for btn in self.nav_buttons:
                self.apply_button_style(btn)
        return switch

    def apply_button_style(self, btn):
        if btn.isChecked():
            btn.setStyleSheet("text-align: left; padding: 12px; border-radius: 8px; font-size: 14px; "
                              "border: none; font-weight: 500; background-color: #EFF6FF; color: #2563EB;")
        else:
            btn.setStyleSheet("text-align: left; padding: 12px; border-radius: 8px; font-size: 14px; "
                              "border: none; font-weight: 500; background-color: transparent; color: #64748B;")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AutoMateUI()
    window.show()
    sys.exit(app.exec_())