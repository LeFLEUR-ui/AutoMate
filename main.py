import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QFrame, QLabel, QPushButton,
                             QStackedWidget)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase, QFont

from components.batch_rename_page import BatchRenameUI
from components.cloud_sync_page import CloudSyncUI
from components.dashboard_page import DashboardPage
from components.files_browser_page import FileBrowserUI
from components.organize_download_page import OrganizeDownloadPage
from components.rules_page import RulesPage

class AutoMateUI(QWidget):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont("assets/InstrumentSans-VariableFont_wdth,wght.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family, 10))
        else:
            self.font_family = "'Inter', 'Segoe UI', sans-serif"

        self.setWindowTitle("AutoMate")
        self.setMinimumSize(1280, 720)
        
        self.setStyleSheet("background-color: #F8FAFC;")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.nav_buttons = []
        self.setup_sidebar()
        
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.setup_top_bar()

        self.stack = QStackedWidget()
        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(FileBrowserUI())
        self.stack.addWidget(RulesPage())
        self.stack.addWidget(OrganizeDownloadPage())
        self.batch_rename_page = BatchRenameUI()
        self.stack.addWidget(self.batch_rename_page)
        self.stack.addWidget(CloudSyncUI())
        
        self.content_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.content_container)
        
        self.setup_floating_hamburger()
        
        self.showMaximized()
        self.update_hamburger_position()

    def setup_top_bar(self):
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(60)
        self.top_bar.setStyleSheet("background-color: transparent; border: none;")
        self.content_layout.addWidget(self.top_bar)

    def setup_floating_hamburger(self):
        self.menu_btn = QPushButton("≡", self)
        self.menu_btn.setFixedSize(32, 32)
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        self.menu_btn.setStyleSheet("""
            QPushButton { 
                font-size: 22px; border: 1px solid #E2E8F0; 
                background-color: white; color: #64748B; border-radius: 16px; 
            }
            QPushButton:hover { background-color: #F8FAFC; color: #2563EB; }
        """)
        self.menu_btn.clicked.connect(self.toggle_sidebar)

    def update_hamburger_position(self):
        sidebar_width = self.sidebar.width()
        self.menu_btn.move(sidebar_width - 16, 14)
        self.menu_btn.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_hamburger_position()

    def setup_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet("background-color: white; border-right: 1px solid #E2E8F0;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(12, 40, 12, 24)

        self.logo_container = QWidget()
        logo_layout = QHBoxLayout(self.logo_container)
        logo_layout.setContentsMargins(12, 0, 0, 0)
        self.logo_icon = QLabel()
        self.logo_icon.setPixmap(QPixmap("assets/flash.png").scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_text = QLabel("AutoMate")
        self.logo_text.setStyleSheet("font-size: 20px; font-weight: 500; color: #0F172A;")
        logo_layout.addWidget(self.logo_icon)
        logo_layout.addWidget(self.logo_text)
        logo_layout.addStretch()
        self.sidebar_layout.addWidget(self.logo_container)
        self.sidebar_layout.addSpacing(32)

        nav_items = [
            ("Dashboard", "assets/icons/home.png"),
            ("Files", "assets/icons/folder dashboard.png"),
            ("Rules", "assets/icons/settings.png"),
            ("Organize", "assets/icons/download.png"),
            ("Rename", "assets/icons/edit.png"),
            ("Cloud", "assets/icons/cloud.png")
        ]

        for i, (text, icon_path) in enumerate(nav_items):
            btn = QPushButton(f"   {text}")
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setFixedHeight(45)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(self.make_switch_func(i))
            
            if i == 0: btn.setChecked(True)
            self.apply_button_style(btn)
            self.sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        self.sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

    def toggle_sidebar(self):
        width = self.sidebar.width()
        is_collapsed = width <= 80
        new_width = 260 if is_collapsed else 70

        self.logo_text.setVisible(is_collapsed)
        for btn in self.nav_buttons:
            if not hasattr(btn, 'full_text'): btn.full_text = btn.text()
            btn.setText(btn.full_text if is_collapsed else "")

        self.anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim.setDuration(300)
        self.anim.setStartValue(width)
        self.anim.setEndValue(new_width)
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)

        self.anim_max = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.anim_max.setDuration(300)
        self.anim_max.setStartValue(width)
        self.anim_max.setEndValue(new_width)
        self.anim_max.setEasingCurve(QEasingCurve.InOutQuart)

        self.btn_anim = QPropertyAnimation(self.menu_btn, b"pos")
        self.btn_anim.setDuration(300)
        self.btn_anim.setStartValue(QPoint(width - 16, 14))
        self.btn_anim.setEndValue(QPoint(new_width - 16, 14))
        self.btn_anim.setEasingCurve(QEasingCurve.InOutQuart)

        self.anim.start()
        self.anim_max.start()
        self.btn_anim.start()

    def make_switch_func(self, index):
        def switch():
            self.stack.setCurrentIndex(index)
            for btn in self.nav_buttons: self.apply_button_style(btn)
        return switch

    def apply_button_style(self, btn):
        if btn.isChecked():
            btn.setStyleSheet("QPushButton { text-align: left; padding-left: 12px; border-radius: 8px; font-size: 14px; border: none; font-weight: 500; background-color: #EFF6FF; color: #2563EB; }")
        else:
            btn.setStyleSheet("QPushButton { text-align: left; padding-left: 12px; border-radius: 8px; font-size: 14px; border: none; font-weight: 400; background-color: transparent; color: #64748B; } QPushButton:hover { background-color: #F1F5F9; }")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoMateUI()
    sys.exit(app.exec_())