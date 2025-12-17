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
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(8)

        top_row = QHBoxLayout()

        status_dot = QLabel()
        dot_color = "#22C55E" if is_active else "#CBD5E1"
        status_dot.setFixedSize(10, 10)
        status_dot.setStyleSheet(f"background-color: {dot_color}; border-radius: 5px;")

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: 500; color: #1E293B; margin-left: 10px;")

        top_row.addWidget(status_dot)
        top_row.addWidget(title_label)
        top_row.addStretch()

        icons = [
            "assets/video-pause-button.png" if is_active else "assets/play-button.png",
            "assets/edit.png",
            "assets/copy.png",
            "assets/trashcan.png"
        ]
        colors = ["#64748B", "#64748B", "#64748B", "#EF4444"]

        for icon_path, color in zip(icons, colors):
            btn = QPushButton()
            icon = QIcon(QPixmap(icon_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            btn.setIcon(icon)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(32, 32)
            btn.setStyleSheet(f"""
                QPushButton {{ border: none; color: {color}; }}
                QPushButton:hover {{ background-color: #F1F5F9; border-radius: 6px; }}
            """)
            top_row.addWidget(btn)

        layout.addLayout(top_row)

        stats_label = QLabel(f"{executions} executions    Last run: {last_run}")
        stats_label.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 400; margin-bottom: 10px;")
        layout.addWidget(stats_label)

        pills_layout = QHBoxLayout()
        pills_layout.setSpacing(12)

        when_pill = self.create_pill("WHEN", when_text, "#EFF6FF", "#3B82F6")
        pills_layout.addWidget(when_pill)

        for action in then_actions:
            then_pill = self.create_pill("THEN", action, "#FAF5FF", "#A855F7")
            pills_layout.addWidget(then_pill)

        pills_layout.addStretch()
        layout.addLayout(pills_layout)

    def create_pill(self, prefix, text, bg, color):
        container = QFrame()
        container.setStyleSheet(f"background-color: {bg}; border-radius: 8px;")
        l = QHBoxLayout(container)
        l.setContentsMargins(12, 6, 12, 6)
        l.setSpacing(8)

        pre = QLabel(prefix)
        pre.setStyleSheet(f"color: {color}; font-weight: 600; font-size: 10px; letter-spacing: 0.5px;")

        arrow = QLabel("›")
        arrow.setStyleSheet(f"color: {color}; font-weight: 500; font-size: 14px;")

        txt = QLabel(text)
        txt.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: 400;")

        l.addWidget(pre)
        l.addWidget(arrow)
        l.addWidget(txt)
        return container


class RulesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation Rules")
        self.resize(1200, 850)
        self.setStyleSheet("background-color: #FFFFFF;")

        font_id = QFontDatabase.addApplicationFont("assets/InstrumentSans-VariableFont_wdth,wght.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family, 10))
        else:
            print("Failed to load font!")

        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_frame = QFrame()
        self.bg_frame.setStyleSheet("background-color: #F8FAFC;")
        bg_layout = QVBoxLayout(self.bg_frame)
        bg_layout.setContentsMargins(60, 40, 60, 40)
        bg_layout.setSpacing(30)

        header_layout = QHBoxLayout()
        header_text_layout = QVBoxLayout()

        title = QLabel("Automation Rules")
        title.setStyleSheet("font-size: 24px; font-weight: 600; color: #0F172A;")
        subtitle = QLabel("Create and manage automation rules for your files")
        subtitle.setStyleSheet("font-size: 14px; color: #64748B; font-weight: 400;")

        header_text_layout.addWidget(title)
        header_text_layout.addWidget(subtitle)

        self.create_btn = QPushButton("+ Create Rule")
        self.create_btn.setFixedSize(140, 45)
        self.create_btn.setCursor(Qt.PointingHandCursor)
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 8px;
                font-weight: 500;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #1D4ED8; }
        """)

        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.create_btn)
        bg_layout.addLayout(header_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("""
            QScrollArea { background-color: transparent; border: none; }
            QScrollBar:vertical { border: none; background: transparent; width: 8px; margin: 0px; }
            QScrollBar::handle:vertical { background: #CBD5E1; min-height: 40px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #94A3B8; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar:horizontal { border: none; background: transparent; height: 8px; margin: 0px; }
            QScrollBar::handle:horizontal { background: #CBD5E1; min-width: 40px; border-radius: 4px; }
            QScrollBar::handle:horizontal:hover { background: #94A3B8; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
            QAbstractScrollArea::corner { background: transparent; }
        """)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        self.cards_layout = QVBoxLayout(self.content_widget)
        self.cards_layout.setSpacing(25)
        self.cards_layout.setAlignment(Qt.AlignTop)

        self.add_rules()

        self.scroll.setWidget(self.content_widget)
        bg_layout.addWidget(self.scroll)
        main_v_layout.addWidget(self.bg_frame)

    def add_rules(self):
        rules = [
            ("Move PDFs to Documents", "247", "2 minutes ago", "When file type is PDF", ["Move to Documents/Reports", "Rename with date prefix"]),
            ("Organize Screenshots", "189", "15 minutes ago", "When filename contains 'screenshot'", ["Move to Pictures/Screenshots", "Rename with timestamp", "Compress image"]),
            ("Archive Old Files", "156", "1 hour ago", "When file is older than 90 days", ["Move to Archive", "Create zip file"]),
            ("Backup Important Docs", "134", "3 hours ago", "When folder is Documents/Important", ["Cloud Backup"], False)
        ]

        for title, execs, time, when, thens, *active in rules:
            is_active = active[0] if active else True
            card = RuleCard(title, execs, time, when, thens, is_active)
            self.cards_layout.addWidget(card)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RulesPage()
    window.show()
    sys.exit(app.exec_())
