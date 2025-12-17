import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QFrame, QLabel, QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Automation Dashboard")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #F8FAFC;")  # Light grey background

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(32)

        # --- Header ---
        header = QVBoxLayout()
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: 700; color: #0F172A; border: none;")
        subtitle = QLabel("Monitor your file automation activity and performance")
        subtitle.setStyleSheet("color: #64748B; font-size: 14px; border: none;")
        header.addWidget(title)
        header.addWidget(subtitle)
        main_layout.addLayout(header)

        # --- Metrics Grid ---
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(20)
        metrics_layout.addWidget(self.create_metric_card("12", "Active Rules", "+2 this week", "⚡", "#EFF6FF", "#3B82F6"))
        metrics_layout.addWidget(self.create_metric_card("1,247", "Files Processed", "+156 today", "📁", "#F0FDF4", "#22C55E"))
        metrics_layout.addWidget(self.create_metric_card("32h", "Time Saved", "+4.5h today", "🕒", "#FAF5FF", "#A855F7"))
        metrics_layout.addWidget(self.create_metric_card("98.5%", "Success Rate", "+0.3% this week", "📈", "#FFF7ED", "#F97316"))
        main_layout.addLayout(metrics_layout)

        # --- Bottom Section (Lists) ---
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Recent Activity Card
        recent_activity = self.create_list_container("Recent Activity", "View All")
        self.add_activity_row(recent_activity, "Move PDFs to Documents", "Moved 5 files", "2 minutes ago")
        self.add_activity_row(recent_activity, "Organize Screenshots", "Renamed 12 files", "15 minutes ago")
        self.add_activity_row(recent_activity, "Archive Old Files", "Archived 8 files", "1 hour ago")
        self.add_activity_row(recent_activity, "Backup Important Docs", "Copied 3 files", "3 hours ago")
        bottom_layout.addWidget(recent_activity)

        # Most Active Rules Card
        active_rules = self.create_list_container("Most Active Rules", "Manage Rules")
        self.add_rule_row(active_rules, "Move PDFs to Documents", "247 executions", "Active")
        self.add_rule_row(active_rules, "Organize Screenshots", "189 executions", "Active")
        self.add_rule_row(active_rules, "Archive Old Files", "156 executions", "Active")
        self.add_rule_row(active_rules, "Backup Important Docs", "134 executions", "Paused")
        bottom_layout.addWidget(active_rules)

        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()

    def create_metric_card(self, value, label, trend, icon, icon_bg, accent_color):
        card = QFrame()
        card.setStyleSheet(f"background-color: white; border: 1px solid #E2E8F0; border-radius: 12px;")
        l = QVBoxLayout(card)
        l.setContentsMargins(20, 20, 20, 20)
        
        ico = QLabel(icon)
        ico.setFixedSize(40, 40)
        ico.setAlignment(Qt.AlignCenter)
        ico.setStyleSheet(f"background-color: {icon_bg}; border-radius: 8px; font-size: 18px; border: none;")
        
        val_label = QLabel(value)
        val_label.setStyleSheet("font-size: 24px; font-weight: 700; color: #0F172A; border: none; margin-top: 10px;")
        
        txt_label = QLabel(label)
        txt_label.setStyleSheet("color: #64748B; font-size: 14px; border: none;")
        
        trend_label = QLabel(trend)
        trend_label.setStyleSheet(f"color: {accent_color}; font-size: 12px; font-weight: 600; border: none; margin-top: 4px;")
        
        l.addWidget(ico)
        l.addWidget(val_label)
        l.addWidget(txt_label)
        l.addWidget(trend_label)
        return card

    def create_list_container(self, title, btn_text):
        card = QFrame()
        card.setStyleSheet("background-color: white; border: 1px solid #E2E8F0; border-radius: 12px;")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header_h = QHBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 700; color: #0F172A; border: none;")
        btn = QPushButton(btn_text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("color: #2563EB; font-weight: 600; border: none; font-size: 12px; background: transparent;")
        
        header_h.addWidget(title_lbl)
        header_h.addStretch()
        header_h.addWidget(btn)
        layout.addLayout(header_h)
        
        return card

    def add_activity_row(self, card, title, desc, time):
        row = QWidget()
        row.setStyleSheet("border: none;")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 5, 0, 5)

        dot = QLabel("●")
        dot.setStyleSheet("color: #22C55E; font-size: 10px; margin-right: 5px;")
        
        texts = QVBoxLayout()
        t = QLabel(title)
        t.setStyleSheet("font-weight: 500; color: #1E293B; font-size: 13px;")
        d = QLabel(desc)
        d.setStyleSheet("color: #64748B; font-size: 12px;")
        texts.addWidget(t)
        texts.addWidget(d)

        time_lbl = QLabel(time)
        time_lbl.setStyleSheet("color: #94A3B8; font-size: 11px;")

        layout.addWidget(dot, 0, Qt.AlignTop)
        layout.addLayout(texts)
        layout.addStretch()
        layout.addWidget(time_lbl, 0, Qt.AlignTop)
        card.layout().addWidget(row)

    def add_rule_row(self, card, title, execs, status):
        row = QWidget()
        row.setStyleSheet("border: none;")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 5, 0, 5)

        texts = QVBoxLayout()
        t = QLabel(title)
        t.setStyleSheet("font-weight: 500; color: #1E293B; font-size: 13px;")
        e = QLabel(execs)
        e.setStyleSheet("color: #64748B; font-size: 12px;")
        texts.addWidget(t)
        texts.addWidget(e)

        status_badge = QLabel(status)
        bg = "#F0FDF4" if status == "Active" else "#F1F5F9"
        fg = "#16A34A" if status == "Active" else "#64748B"
        status_badge.setStyleSheet(f"""
            background-color: {bg}; color: {fg}; 
            padding: 4px 10px; border-radius: 10px; 
            font-size: 11px; font-weight: 600;
        """)

        layout.addLayout(texts)
        layout.addStretch()
        layout.addWidget(status_badge)
        card.layout().addWidget(row)