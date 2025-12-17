import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QFrame, QLabel, QPushButton, QDesktopWidget,
                             QStackedWidget, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase, QFont

from components.dashboard_page import DashboardPage
from components.files_browser_page import FileBrowserUI
from components.rules_page import RulesPage

class AutoMateUI(QWidget):
    def __init__(self):
        super().__init__()

        # --- Load custom font ---
        font_id = QFontDatabase.addApplicationFont("assets/InstrumentSans-VariableFont_wdth,wght.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family, 10))
        else:
            print("Failed to load font!")

        self.setWindowTitle("AutoMate Dashboard")
        self.resize(1280, 800)
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.nav_buttons = []
        self.setup_sidebar()
        
        self.stack = QStackedWidget()
        self.stack.addWidget(DashboardPage()) 
        self.stack.addWidget(FileBrowserUI())
        self.stack.addWidget(RulesPage())
        # self.stack.addWidget(ActivityPage())
        
        self.main_layout.addWidget(self.stack)
        self.center()

    def setup_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("background-color: white; border-right: 1px solid #E2E8F0;")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(24, 40, 24, 24)

        logo_layout = QHBoxLayout()
        logo_icon = QLabel()
        pixmap = QPixmap("assets/flash.png").scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_icon.setPixmap(pixmap)
        logo_text = QLabel("AutoMate")
        logo_text.setStyleSheet("font-size: 22px; font-weight: 600; color: #0F172A;")
        logo_layout.addWidget(logo_icon)
        logo_layout.addSpacing(8)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        layout.addLayout(logo_layout)
        layout.addSpacing(32)

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
                              "border: none; font-weight: 400; background-color: transparent; color: #64748B;")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icon.ico"))
    window = AutoMateUI()
    window.show()
    sys.exit(app.exec_())
