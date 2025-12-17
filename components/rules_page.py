import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont, QPixmap, QIcon

class RuleCard(QFrame):
    def __init__(self, title, executions, last_run, when_text, then_actions, is_active=True):
        super().__init__()
        self.setFixedHeight(180)
        self.setObjectName("Card")
        self.setStyleSheet("""
            #Card {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 10))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)

        top_row = QHBoxLayout()

        status_dot = QLabel()
        dot_color = "#22C55E" if is_active else "#CBD5E1"
        status_dot.setFixedSize(10, 10)
        status_dot.setStyleSheet(f"background-color: {dot_color}; border-radius: 5px; border: none;")

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #0F172A; border: none;")

        top_row.addWidget(status_dot)
        top_row.addWidget(title_label)
        top_row.addStretch()
        
        icons = [
            "assets/video-pause-button.png" if is_active else "assets/play-button.png",
            "assets/edit.png",
            "assets/trashcan.png"
        ]
        
        for icon_path in icons:
            btn = QPushButton()
            btn.setIcon(QIcon(icon_path))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("""
                QPushButton { border: none; background: transparent; }
                QPushButton:hover { background-color: #F1F5F9; border-radius: 6px; }
            """)
            top_row.addWidget(btn)

        layout.addLayout(top_row)

        stats_label = QLabel(f"{executions} executions • Last run: {last_run}")
        stats_label.setStyleSheet("color: #64748B; font-size: 13px; font-weight: 400; border: none;")
        layout.addWidget(stats_label)

        pills_layout = QHBoxLayout()
        pills_layout.setSpacing(10)

        when_pill = self.create_pill("WHEN", when_text, "#EFF6FF", "#3B82F6")
        pills_layout.addWidget(when_pill)

        for action in then_actions:
            then_pill = self.create_pill("THEN", action, "#FAF5FF", "#A855F7")
            pills_layout.addWidget(then_pill)

        pills_layout.addStretch()
        layout.addLayout(pills_layout)

    def create_pill(self, prefix, text, bg, color):
        container = QFrame()
        container.setStyleSheet(f"background-color: {bg}; border-radius: 6px; border: none;")
        l = QHBoxLayout(container)
        l.setContentsMargins(10, 5, 10, 5)
        l.setSpacing(6)

        pre = QLabel(prefix)
        pre.setStyleSheet(f"color: {color}; font-weight: 700; font-size: 10px;")

        txt = QLabel(text)
        txt.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: 500;")

        l.addWidget(pre)
        l.addWidget(txt)
        return container

class RulesPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Automation Rules")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #F8FAFC;")

        font_id = QFontDatabase.addApplicationFont("assets/InstrumentSans-VariableFont_wdth,wght.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family))

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        header_layout = QHBoxLayout()
        header_text = QVBoxLayout()

        title = QLabel("Automation Rules")
        title.setStyleSheet("font-size: 24px; font-weight: 600; color: #0F172A; border: none;")
        subtitle = QLabel("Create and manage automation rules for your files")
        subtitle.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 400; border: none;")

        header_text.addWidget(title)
        header_text.addWidget(subtitle)
        header_layout.addLayout(header_text)
        header_layout.addStretch()

        self.create_btn = QPushButton("+ Create Rule")
        self.create_btn.setFixedSize(140, 45)
        self.create_btn.setCursor(Qt.PointingHandCursor)
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #1D4ED8; }
        """)
        header_layout.addWidget(self.create_btn)
        main_layout.addLayout(header_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.scroll.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical { border: none; background: transparent; width: 8px; }
            QScrollBar::handle:vertical { background: #CBD5E1; border-radius: 4px; min-height: 40px; }
            QScrollBar::handle:vertical:hover { background: #94A3B8; }
            QScrollBar::add-line, QScrollBar::sub-line { height: 0px; }
        """)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        self.cards_layout = QVBoxLayout(self.content_widget)
        self.cards_layout.setSpacing(20)
        self.cards_layout.setAlignment(Qt.AlignTop)
        self.cards_layout.setContentsMargins(0, 0, 10, 0)

        self.add_rules()

        self.scroll.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll)

    def add_rules(self):
        rules_data = [
            ("Move PDFs to Documents", "247", "2m ago", "File type is PDF", ["Move to Reports", "Add Date Prefix"]),
            ("Organize Screenshots", "189", "15m ago", "Filename contains 'screenshot'", ["Move to Screenshots", "Compress"]),
            ("Archive Old Files", "156", "1h ago", "Older than 90 days", ["Archive Zip"]),
            ("Backup Important Docs", "134", "3h ago", "Folder is 'Documents'", ["Cloud Backup"], False)
        ]

        for title, execs, time, when, thens, *active in rules_data:
            is_active = active[0] if active else True
            card = RuleCard(title, execs, time, when, thens, is_active)
            self.cards_layout.addWidget(card)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RulesPage()
    window.show()
    sys.exit(app.exec_())