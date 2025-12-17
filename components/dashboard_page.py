import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QFrame, QLabel, QPushButton, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Automation Dashboard")
        self.resize(1200, 900)
        
        self.font_family = "'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif"
        
        self.window_layout = QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: #F8FAFC;
            }}
            QScrollBar:vertical {{
                border: none;
                background: #F8FAFC;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #CBD5E1;
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #94A3B8;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet(f"background-color: #F8FAFC; font-family: {self.font_family};")
        self.main_layout = QVBoxLayout(self.content_widget)
        self.main_layout.setContentsMargins(40, 32, 40, 32)
        self.main_layout.setSpacing(28)

        header = QVBoxLayout()
        header.setSpacing(4)
        header.addWidget(QLabel("Dashboard", styleSheet="font-size: 24px; font-weight: 600; color: #0F172A;"))
        header.addWidget(QLabel(
            "Automate your file organization with powerful tools",
            styleSheet="font-size: 14px; font-weight: 400; color: #64748B;"
        ))
        self.main_layout.addLayout(header)

        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(20)
        metrics_layout.addWidget(self.create_metric_card(
            "12", "Active Rules", "+2 this week", "#EFF6FF", "#3B82F6", "assets/icons/thunder.png"
        ))
        metrics_layout.addWidget(self.create_metric_card(
            "1,247", "Files Processed", "+156 today", "#F0FDF4", "#22C55E", "assets/icons/folder.png"
        ))
        metrics_layout.addWidget(self.create_metric_card(
            "32h", "Time Saved", "+4.5h today", "#FAF5FF", "#A855F7", "assets/icons/clock.png"
        ))
        metrics_layout.addWidget(self.create_metric_card(
            "98.5%", "Success Rate", "+0.3% this week", "#FFF7ED", "#F97316", "assets/icons/graph.png"
        ))
        self.main_layout.addLayout(metrics_layout)

        self.main_layout.addWidget(QLabel(
            "Quick Actions",
            styleSheet="font-size: 16px; font-weight: 600; color: #0F172A; margin-top: 8px;"
        ))

        quick_actions_layout = QHBoxLayout()
        quick_actions_layout.setSpacing(20)
        quick_actions_layout.addWidget(self.create_action_card(
            "Organize Downloads",
            "Sort files by type or date automatically",
            "247 files organized",
            "#EFF6FF",
            "#3B82F6",
            "assets/icons/download.png"
        ))
        quick_actions_layout.addWidget(self.create_action_card(
            "Batch Rename",
            "Rename multiple files with patterns",
            "189 files renamed",
            "#FAF5FF",
            "#A855F7",
            "assets/icons/batch-processing.png"
        ))
        quick_actions_layout.addWidget(self.create_action_card(
            "Cloud Backup",
            "Sync folders to Google Drive or Dropbox",
            "10.6 GB synced",
            "#F0FDF4",
            "#22C55E",
            "assets/icons/cloud.png"
        ))
        self.main_layout.addLayout(quick_actions_layout)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(24)

        self.recent_activity = self.create_container_card("Recent Activity", "View All")
        self.add_activity_item(
            "Organize Downloads by Type",
            "Moved 12 files to appropriate folders",
            "2 minutes ago"
        )
        self.add_activity_item(
            "Batch Rename Photos",
            "Renamed 24 files with date prefix",
            "15 minutes ago"
        )
        self.add_activity_item(
            "Cloud Backup - Work",
            "Synced 8 files to Google Drive",
            "1 hour ago"
        )
        self.add_activity_item(
            "Organize Downloads by Date",
            "Sorted 15 files into month folders",
            "3 hours ago"
        )

        self.getting_started = self.create_container_card("Getting Started", None)
        self.add_guide_item(
            "Organize your Downloads",
            "Automatically sort files by type into Documents and Pictures.",
            "#EFF6FF",
            "#3B82F6",
            "assets/icons/download.png"
        )
        self.add_guide_item(
            "Batch rename files",
            "Use patterns like dates and custom text to rename files.",
            "#FAF5FF",
            "#A855F7",
            "assets/icons/batch-processing.png"
        )
        self.add_guide_item(
            "Backup to the cloud",
            "Connect Google Drive to backup important folders.",
            "#F0FDF4",
            "#22C55E",
            "assets/icons/cloud.png"
        )

        bottom_row.addWidget(self.recent_activity, 2)
        bottom_row.addWidget(self.getting_started, 1)
        self.main_layout.addLayout(bottom_row)
        
        self.main_layout.addStretch()

        self.scroll.setWidget(self.content_widget)
        self.window_layout.addWidget(self.scroll)

    def set_icon(self, label, path, size):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            label.setPixmap(pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            label.setText("?")

    def create_metric_card(self, value, label, trend, bg, color, icon_path):
        card = QFrame()
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet(f"""
            QFrame {{ 
                background-color: white; 
                border: 1px solid #E2E8F0; 
                border-radius: 12px; 
            }}
            QFrame:hover {{
                border: 1px solid #3B82F6;
                background-color: #FCFDFF;
            }}
            QFrame:pressed {{
                background-color: #F1F5F9;
                border: 1px solid #2563EB;
                margin: 1px;
            }}
        """)
        l = QVBoxLayout(card)
        l.setContentsMargins(20, 20, 20, 20)
        
        ico = QLabel(styleSheet=f"background-color: {bg}; border-radius: 8px; border: none;")
        ico.setFixedSize(36, 36)
        ico.setAlignment(Qt.AlignCenter)
        self.set_icon(ico, icon_path, 20)
        
        l.addWidget(ico)
        l.addWidget(QLabel(value, styleSheet="font-size: 24px; font-weight: 700; color: #0F172A; margin-top: 12px; border: none; background: transparent;"))
        l.addWidget(QLabel(label, styleSheet="font-size: 13px; font-weight: 500; color: #64748B; border: none; background: transparent;"))
        l.addWidget(QLabel(trend, styleSheet=f"font-size: 12px; font-weight: 600; color: {color}; margin-top: 4px; border: none; background: transparent;"))
        return card

    def create_action_card(self, title, desc, stats, bg, color, icon_path):
        card = QFrame()
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border: 1px solid #E2E8F0; 
                border-radius: 12px; 
            }
            QFrame:hover {
                border: 1px solid #3B82F6;
                background-color: #FCFDFF;
            }
            QFrame:pressed {
                background-color: #F1F5F9;
                border: 1px solid #2563EB;
                margin: 2px;
            }
        """)
        l = QVBoxLayout(card)
        l.setContentsMargins(24, 24, 24, 24)
        
        h = QHBoxLayout()
        ico = QLabel(styleSheet=f"background-color: {bg}; border-radius: 10px; border: none;")
        ico.setFixedSize(40, 40)
        ico.setAlignment(Qt.AlignCenter)
        self.set_icon(ico, icon_path, 24)

        h.addWidget(ico)
        h.addStretch()
        h.addWidget(QLabel("→", styleSheet="color: #94A3B8; font-size: 20px; border: none; background: transparent;"))
        l.addLayout(h)

        l.addSpacing(16)
        l.addWidget(QLabel(title, styleSheet="font-size: 15px; font-weight: 600; color: #0F172A; border: none; background: transparent;"))
        l.addWidget(QLabel(desc, styleSheet="font-size: 13px; font-weight: 400; color: #64748B; line-height: 1.4; border: none; background: transparent;"))
        l.addWidget(QLabel(stats, styleSheet="font-size: 12px; font-weight: 500; color: #94A3B8; margin-top: 6px; border: none; background: transparent;"))
        return card

    def create_container_card(self, title, btn_text):
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border: 1px solid #E2E8F0; border-radius: 12px; }")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        h = QHBoxLayout()
        h.addWidget(QLabel(title, styleSheet="font-size: 16px; font-weight: 600; color: #0F172A; border: none;"))
        if btn_text:
            h.addStretch()
            btn = QPushButton(btn_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { 
                    color: #2563EB; font-size: 13px; font-weight: 600; 
                    background: transparent; border: none; 
                }
                QPushButton:hover { color: #1D4ED8; }
                QPushButton:pressed { color: #1E40AF; }
            """)
            h.addWidget(btn)
        layout.addLayout(h)
        layout.addSpacing(8)
        return card

    def add_activity_item(self, title, desc, time):
        row = QWidget()
        l = QHBoxLayout(row)
        l.setContentsMargins(0, 12, 0, 12)
        dot = QLabel("●", styleSheet="color: #22C55E; font-size: 12px; margin-right: 10px; border: none;")
        text_v = QVBoxLayout()
        text_v.setSpacing(2)
        text_v.addWidget(QLabel(title, styleSheet="font-size: 14px; font-weight: 500; color: #1E293B; border: none;"))
        text_v.addWidget(QLabel(desc, styleSheet="font-size: 12px; font-weight: 400; color: #64748B; border: none;"))
        l.addWidget(dot, 0, Qt.AlignTop)
        l.addLayout(text_v)
        l.addStretch()
        l.addWidget(QLabel(time, styleSheet="font-size: 11px; font-weight: 400; color: #94A3B8; border: none;"), 0, Qt.AlignTop)
        self.recent_activity.layout().addWidget(row)

    def add_guide_item(self, title, desc, bg, color, icon_path):
        item = QFrame()
        item.setCursor(Qt.PointingHandCursor)
        item.setStyleSheet(f"""
            QFrame {{ 
                background-color: {bg}; 
                border-radius: 10px; 
                border: 1px solid transparent; 
            }}
            QFrame:hover {{ border: 1px solid {color}; }}
            QFrame:pressed {{ background-color: #E2E8F0; border: 1px solid {color}; }}
        """)
        
        l = QHBoxLayout(item)
        l.setContentsMargins(16, 14, 16, 14)
        l.setSpacing(12)
        
        ico = QLabel(styleSheet="border: none; background: transparent;")
        ico.setFixedSize(20, 20)
        self.set_icon(ico, icon_path, 20)
        
        text_v = QVBoxLayout()
        text_v.setSpacing(2)
        
        t_lbl = QLabel(title, styleSheet="font-size: 13px; font-weight: 600; color: #1E293B; border: none; background: transparent;")
        d_lbl = QLabel(desc, styleSheet="font-size: 11px; font-weight: 400; color: #64748B; border: none; background: transparent;")
        d_lbl.setWordWrap(True)
        
        text_v.addWidget(t_lbl)
        text_v.addWidget(d_lbl)
        
        l.addWidget(ico, 0, Qt.AlignTop)
        l.addLayout(text_v)
        l.addStretch()
        
        self.getting_started.layout().addWidget(item)
