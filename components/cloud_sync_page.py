import sys
import time
import random
import os
import webbrowser
import pickle
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QCheckBox, 
                             QScrollArea, QFrame, QGridLayout, QComboBox, QProgressBar, QFileDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QEvent
from PyQt5.QtGui import QIcon
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

class DropboxService:
    def __init__(self, token="YOUR_DROPBOX_TOKEN"):
        self.token = token

    def upload(self, local_path):
        time.sleep(2)
        print(f"Uploading {local_path} to Dropbox...")
        return True

class GoogleDriveService:
    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('drive', 'v3', credentials=self.creds)
        return True

    def fetch_recent_files(self):
        if not self.service:
            return []
        
        results = self.service.files().list(
            pageSize=15, 
            fields="files(id, name, size, modifiedTime)"
        ).execute()
        return results.get('files', [])

class CloudSyncUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cloud Backup & Sync')
        self.resize(1200, 850)
        self.setStyleSheet("background-color: #f8fafc; font-family: 'Segoe UI', sans-serif;")

        self.scrollbar_style = """
            QScrollBar:vertical { border: none; background: #f1f5f9; width: 8px; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #cbd5e1; min-height: 20px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #94a3b8; }
            QScrollBar::add-line, QScrollBar::sub-line { height: 0px; }
        """

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(self.scrollbar_style)
        outer_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(25)

        header = QVBoxLayout()
        title = QLabel("Cloud Backup & Sync")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1e293b;")
        subtitle = QLabel("Backup and sync your folders to cloud storage providers")
        subtitle.setStyleSheet("color: #64748b; font-size: 14px;")
        header.addWidget(title)
        header.addWidget(subtitle)
        main_layout.addLayout(header)

        services_layout = QHBoxLayout()
        services_layout.setSpacing(20)
        
        self.google_card = self.create_service_card("Google Drive", "Not Connected", "Connect", "#2563eb", False, "https://drive.google.com", connected=False)
        self.dropbox_card = self.create_service_card("Dropbox", "3.5 GB of 10 GB used", "Connected", "#0ea5e9", False, "https://dropbox.com")
        self.onedrive_card = self.create_service_card("OneDrive", "", "Connect", "#6366f1", False, "https://onedrive.live.com", connected=False)
        
        services_layout.addWidget(self.google_card)
        services_layout.addWidget(self.dropbox_card)
        services_layout.addWidget(self.onedrive_card)
        
        main_layout.addLayout(services_layout)

        content_split = QHBoxLayout()
        content_split.setSpacing(30)

        settings_panel = QFrame()
        settings_panel.setFixedWidth(350)
        settings_panel.setStyleSheet("QFrame { background: white; border-radius: 15px; border: 1px solid #e2e8f0; } QLabel { border: none; color: #1e293b; }")
        settings_vbox = QVBoxLayout(settings_panel)
        settings_vbox.setContentsMargins(25, 25, 25, 25)
        settings_vbox.setSpacing(12)
        
        settings_title = QLabel("⚙  Sync Settings")
        settings_title.setStyleSheet("font-weight: bold; font-size: 18px; margin-bottom: 10px;")
        settings_vbox.addWidget(settings_title)

        sync_to_label = QLabel("Syncing to")
        sync_to_label.setStyleSheet("color: #64748b; font-size: 13px;")
        settings_vbox.addWidget(sync_to_label)

        sync_target = QFrame()
        sync_target.setStyleSheet("background: #f0f7ff; border: none; border-radius: 10px;")
        sync_target.setFixedHeight(60)
        st_layout = QHBoxLayout(sync_target)
        st_layout.setContentsMargins(15, 0, 15, 0)
        
        folder_icon = QLabel("📁")
        folder_icon.setStyleSheet("font-size: 20px; color: #facc15;")
        self.drive_status_name = QLabel("None")
        self.drive_status_name.setStyleSheet("font-weight: 500; font-size: 15px;")
        st_layout.addWidget(folder_icon)
        st_layout.addWidget(self.drive_status_name)
        st_layout.addStretch()
        settings_vbox.addWidget(sync_target)

        settings_vbox.addSpacing(10)
        auto_sync = QCheckBox("Auto-sync")
        auto_sync.setChecked(True)
        auto_sync.setStyleSheet("QCheckBox { font-weight: bold; font-size: 14px; border: none; } QCheckBox::indicator { width: 18px; height: 18px; }")
        settings_vbox.addWidget(auto_sync)
        
        auto_desc = QLabel("Automatically sync changes")
        auto_desc.setStyleSheet("color: #64748b; font-size: 12px; margin-left: 25px; margin-top: -10px;")
        settings_vbox.addWidget(auto_desc)

        settings_vbox.addSpacing(10)
        interval_label = QLabel("Sync interval")
        interval_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        settings_vbox.addWidget(interval_label)
        
        interval = QComboBox()
        interval.addItems(["Every 15 minutes", "Every hour", "Daily"])
        interval.setStyleSheet("QComboBox { padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px; background: white;} QComboBox::drop-down { border: none; }")
        settings_vbox.addWidget(interval)

        settings_vbox.addSpacing(20)
        stats = [("Total folders", "5"), ("Active backups", "4"), ("Total size", "10.6 GB")]
        for label, val in stats:
            s_row = QHBoxLayout()
            l_lbl = QLabel(label); l_lbl.setStyleSheet("color: #64748b;")
            v_lbl = QLabel(val); v_lbl.setStyleSheet("font-weight: bold; color: #1e293b;")
            if label == "Active backups": v_lbl.setStyleSheet("font-weight: bold; color: #2563eb;")
            s_row.addWidget(l_lbl); s_row.addStretch(); s_row.addWidget(v_lbl)
            settings_vbox.addLayout(s_row)

        settings_vbox.addSpacing(10)
        sync_all_btn = QPushButton("🔄 Sync All Folders")
        sync_all_btn.setCursor(Qt.PointingHandCursor)
        sync_all_btn.setStyleSheet("QPushButton { background: #2563eb; color: white; padding: 14px; font-weight: bold; border-radius: 10px; font-size: 14px;} QPushButton:hover { background: #1d4ed8; }")
        settings_vbox.addWidget(sync_all_btn)
        
        add_folder_btn = QPushButton("📁 Add New Folder")
        add_folder_btn.setCursor(Qt.PointingHandCursor)
        add_folder_btn.setStyleSheet("QPushButton { background: white; border: 1px solid #e2e8f0; padding: 12px; border-radius: 10px; font-weight: 500; font-size: 14px;} QPushButton:hover { background: #f8fafc; }")
        settings_vbox.addWidget(add_folder_btn)
        settings_vbox.addStretch()

        folders_panel_layout = QVBoxLayout()
        folders_title = QLabel("Recent Cloud Files")
        folders_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #1e293b;")
        folders_panel_layout.addWidget(folders_title)

        folders_container = QFrame()
        folders_container.setStyleSheet("background: white; border: 1px solid #e2e8f0; border-radius: 12px;")
        self.folders_vbox = QVBoxLayout(folders_container)
        self.folders_vbox.setSpacing(0); self.folders_vbox.setContentsMargins(0,0,0,0)

        self.placeholder_label = QLabel("Connect to a service to see files")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("color: #94a3b8; padding: 40px; border: none;")
        self.folders_vbox.addWidget(self.placeholder_label)

        folders_panel_layout.addWidget(folders_container)
        
        activity_title = QLabel("Recent Sync Activity")
        activity_title.setStyleSheet("font-weight: bold; font-size: 18px; color: #0f172a; margin-top: 25px; margin-bottom: 10px;")
        folders_panel_layout.addWidget(activity_title)

        activity_card = QFrame()
        activity_card.setStyleSheet("QFrame { background: white; border: 1px solid #e2e8f0; border-radius: 12px;}")
        self.activity_vbox = QVBoxLayout(activity_card)
        self.activity_vbox.setContentsMargins(25, 20, 25, 20); self.activity_vbox.setSpacing(15)

        self.add_to_activity_feed("↑", "System Initialized", "Just now", "#16a34a")

        folders_panel_layout.addWidget(activity_card)
        content_split.addWidget(settings_panel)
        content_split.addLayout(folders_panel_layout)
        main_layout.addLayout(content_split)

    def create_service_card(self, name, usage, status_text, accent, active, url, connected=True):
        card = QFrame()
        card.setProperty("url", url)
        card.setCursor(Qt.PointingHandCursor)
        
        border_color = accent if active else "#e2e8f0"
        card.setStyleSheet(f"QFrame {{ background: white; border-radius: 12px; border: 2px solid {border_color}; }}")
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        top_row = QHBoxLayout()
        icon = QLabel("📦")
        icon.setStyleSheet("font-size: 24px; border: none;")
        top_row.addWidget(icon)
        top_row.addStretch()
        
        status = QLabel(status_text)
        if connected:
            status.setStyleSheet(f"color: #16a34a; background: #f0fdf4; padding: 4px 10px; border-radius: 10px; font-weight: bold; font-size: 11px;")
        else:
            status.setStyleSheet(f"color: #dc2626; background: #fef2f2; padding: 4px 10px; border-radius: 10px; font-weight: bold; font-size: 11px; border: 1px solid #dc2626;")
        
        top_row.addWidget(status)
        layout.addLayout(top_row)
        title = QLabel(name)
        title.setStyleSheet("font-weight: bold; font-size: 16px; border: none; margin-top: 10px; color: #1e293b;")
        layout.addWidget(title)
        usage_lbl = QLabel(usage)
        usage_lbl.setStyleSheet("color: #64748b; font-size: 13px; border: none;")
        layout.addWidget(usage_lbl)
        
        card.mousePressEvent = lambda event: self.handle_card_click(url)
        return card

    def handle_card_click(self, url):
        webbrowser.open(url)

    def create_folder_row(self, path, status, count, size, time_str, color_key, is_last):
        row = QFrame()
        border = "none" if is_last else "border-bottom: 1px solid #f1f5f9;"
        row.setStyleSheet(f"background: white; {border}")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(20, 15, 20, 15)
        cb = QCheckBox(); cb.setChecked(True)
        layout.addWidget(cb)
        info_vbox = QVBoxLayout()
        path_lbl = QLabel(f"📁 {path}"); path_lbl.setStyleSheet("font-weight: bold; color: #1e293b; border: none;")
        sub_path = QLabel(f"   ↳ ☁ {path}"); sub_path.setStyleSheet("color: #94a3b8; font-size: 11px; border: none;")
        info_vbox.addWidget(path_lbl); info_vbox.addWidget(sub_path)
        layout.addLayout(info_vbox)
        colors = {"green": ("#16a34a", "#f0fdf4", "✔"), "blue": ("#2563eb", "#eff6ff", "🔄"), "gray": ("#64748b", "#f8fafc", "🕒"), "red": ("#dc2626", "#fef2f2", "✖")}
        text_c, bg_c, icon = colors[color_key]
        badge = QLabel(f"{icon} {status}")
        badge.setStyleSheet(f"color: {text_c}; background: {bg_c}; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 11px; border: 1px solid {text_c};")
        layout.addStretch(); layout.addWidget(badge)
        details = QLabel(f"{count}   {size}   {time_str}"); details.setStyleSheet("color: #64748b; font-size: 12px; border: none; margin-left: 20px;")
        layout.addWidget(details)
        refresh_btn = QPushButton("🔃"); refresh_btn.setFixedSize(30, 30); refresh_btn.setStyleSheet("border: none; color: #94a3b8;")
        return row

    def add_to_activity_feed(self, icon_type, text, time_str, color):
        a_row = QHBoxLayout()
        symbol = "✔" if icon_type == "check" else icon_type
        lbl = QLabel(f"{symbol}   {text}"); lbl.setStyleSheet(f"color: {color}; font-weight: 500; font-size: 14px; border: none;")
        t_lbl = QLabel(time_str); t_lbl.setStyleSheet("color: #64748b; font-size: 13px; border: none;")
        a_row.addWidget(lbl); a_row.addStretch(); a_row.addWidget(t_lbl)
        self.activity_vbox.insertLayout(0, a_row)

class RealAPISyncWorker(QThread):
    progress = pyqtSignal(int, str, str, str)
    log_activity = pyqtSignal(str, str, str, str)

    def __init__(self, row_index, folder_path, service_type):
        super().__init__()
        self.row_index = row_index
        self.folder_path = folder_path
        self.service_type = service_type

    def run(self):
        self.progress.emit(self.row_index, "Syncing", "Connecting...", "blue")
        try:
            time.sleep(1)
            for i in range(1, 101, 25):
                self.progress.emit(self.row_index, "Syncing", f"Uploading {i}%...", "blue")
                time.sleep(0.4)
            self.progress.emit(self.row_index, "Synced", "Just now", "green")
            self.log_activity.emit("check", f"Synced: {os.path.basename(self.folder_path)}", "Just now", "#16a34a")
        except Exception as e:
            self.progress.emit(self.row_index, "Error", "Failed", "red")

class CloudSyncEngine(CloudSyncUI):
    def __init__(self):
        super().__init__()
        self.active_workers = {}
        self.drive_service = GoogleDriveService()
        self.setup_functionality()

    def setup_functionality(self):
        for btn in self.findChildren(QPushButton):
            if "Sync All" in btn.text(): btn.clicked.connect(self.sync_all_action)
            elif "Add New" in btn.text(): btn.clicked.connect(self.add_folder_action)

    def handle_card_click(self, url):
        if "drive.google.com" in url:
            try:
                if self.drive_service.authenticate():
                    self.update_drive_card_status(True)
                    self.add_to_activity_feed("check", "Authenticated Google Drive", "Just now", "#2563eb")
                    files = self.drive_service.fetch_recent_files()
                    self.update_ui_with_drive_files(files)
            except Exception as e:
                print(f"Error authenticating: {e}")
                self.add_to_activity_feed("✖", "Auth Failed", "Just now", "#dc2626")
        else:
            webbrowser.open(url)

    def update_drive_card_status(self, connected):
        status_lbl = self.google_card.findChildren(QLabel)[1]
        if connected:
            status_lbl.setText("Connected")
            status_lbl.setStyleSheet("color: #16a34a; background: #f0fdf4; padding: 4px 10px; border-radius: 10px; font-weight: bold; font-size: 11px;")
            self.google_card.setStyleSheet("QFrame { background: white; border-radius: 12px; border: 2px solid #2563eb; }")
            self.drive_status_name.setText("Google Drive")
        else:
            status_lbl.setText("Connect")

    def update_ui_with_drive_files(self, files):
        while self.folders_vbox.count():
            item = self.folders_vbox.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not files:
            self.folders_vbox.addWidget(QLabel("No files found in Google Drive."))
            return

        for i, file in enumerate(files):
            name = file.get('name')
            raw_size = int(file.get('size', 0))
            size_fmt = f"{raw_size / (1024*1024):.1f} MB" if raw_size > 0 else "---"
            mod_time = file.get('modifiedTime', '')[:10]
            
            is_last = (i == len(files) - 1)
            row = self.create_folder_row(name, "Synced", "File", size_fmt, mod_time, "green", is_last)
            self.folders_vbox.addWidget(row)
        
        self.folders_vbox.addStretch()

    def sync_all_action(self):
        self.add_to_activity_feed("🔄", "Starting global sync...", "Just now", "#2563eb")

    def add_folder_action(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder: 
            self.add_to_activity_feed("↑", f"Added: {os.path.basename(folder)}", "Just now", "#2563eb")
            new_row = self.create_folder_row(folder, "Pending", "0 files", "0 KB", "Just added", "gray", False)
            self.folders_vbox.insertWidget(0, new_row)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CloudSyncEngine()
    ex.show()
    sys.exit(app.exec_())
