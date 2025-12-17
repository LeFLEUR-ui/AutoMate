import sys
import os
import datetime
import platform
import shutil
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QLabel, QPushButton, QScrollArea, QCheckBox, 
                             QRadioButton, QButtonGroup, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR) 

class ClickableFrame(QFrame):
    doubleClicked = pyqtSignal(str)
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.doubleClicked.emit(self.file_path)

class OrganizeDownloadPage(QWidget):
    def __init__(self):
        super().__init__()
        self.downloads_path = str(Path.home() / "Downloads")
        
        self.EXT_GROUPS = {
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv'],
            'Images': ['.jpg', '.jpeg', '.png', '.svg', '.gif', '.bmp'],
            'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
            'Music': ['.mp3', '.wav', '.flac'],
            'Archives': ['.zip', '.rar', '.7z', '.tar'],
            'Code': ['.py', '.html', '.css', '.js', '.cpp'],
        }

        def get_asset(name):
            return os.path.join(BASE_DIR, 'assets', 'icons', name)

        self.ICON_MAPPING = {
            '.pdf': get_asset('pdf.png'), '.doc': get_asset('google-docs.png'),
            '.docx': get_asset('word.png'), '.txt': get_asset('txt.png'),
            '.xlsx': get_asset('xlxs.png'), '.pptx': get_asset('pptx.png'),
            '.jpg': get_asset('jpg.png'), '.jpeg': get_asset('jpg.png'),
            '.png': get_asset('png.png'), '.svg': get_asset('svg.png'),
            '.mp4': get_asset('mp4.png'), '.zip': get_asset('zip.png'),
            'default': get_asset('generic.png'),
            'settings': get_asset('settings.png'),
            'folder': get_asset('folder.png')
        }

        self.file_checkboxes = {}
        self.setup_ui()
        self.load_real_data()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        header = QVBoxLayout()
        title = QLabel("Organize Downloads")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #0F172A;")
        subtitle = QLabel("Automatically sort files in your Downloads folder by type or date")
        subtitle.setStyleSheet("font-size: 13px; color: #64748B;")
        header.addWidget(title)
        header.addWidget(subtitle)
        self.main_layout.addLayout(header)

        content = QHBoxLayout()
        content.setSpacing(30)

        sidebar = QFrame()
        sidebar.setFixedWidth(380)
        sidebar.setStyleSheet("QFrame { background-color: white; border: 1px solid #E2E8F0; border-radius: 12px; }")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(24, 24, 24, 24)
        sidebar_layout.setSpacing(15)

        s_header = QHBoxLayout()
        gear_icon = QLabel()
        pix = QPixmap(self.ICON_MAPPING['settings'])
        if not pix.isNull():
            gear_icon.setPixmap(pix.scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        s_header.addWidget(gear_icon)
        s_header.addWidget(QLabel("Organization Settings", styleSheet="font-size: 16px; font-weight: 600; color: #0F172A; border: none;"))
        s_header.addStretch()
        sidebar_layout.addLayout(s_header)

        sidebar_layout.addWidget(QLabel("Organize by", styleSheet="color: #64748B; font-size: 12px; font-weight: 500; border: none;"))
        self.group = QButtonGroup(self)
        sidebar_layout.addWidget(self.create_selection_card("File Type", "Documents, Images, Videos, etc.", True, 0))
        sidebar_layout.addWidget(self.create_selection_card("Date", "Year/Month folders", False, 1))

        auto_card = QFrame()
        auto_card.setStyleSheet("QFrame { background-color: #EFF6FF; border: none; border-radius: 10px; }")
        auto_lay = QHBoxLayout(auto_card)
        self.auto_cb = QCheckBox()
        auto_txt = QVBoxLayout()
        at = QLabel("Auto-organize")
        at.setStyleSheet("font-weight: 600; color: #1E293B; border: none;")
        ad = QLabel("Automatically organize new downloads")
        ad.setStyleSheet("font-size: 11px; color: #475569; border: none;")
        auto_txt.addWidget(at)
        auto_txt.addWidget(ad)
        auto_lay.addWidget(self.auto_cb)
        auto_lay.addLayout(auto_txt)
        auto_lay.addStretch()
        sidebar_layout.addWidget(auto_card)

        self.total_val = QLabel("0")
        self.selected_val = QLabel("0")
        for lbl, val, color in [("Total files", self.total_val, "#0F172A"), ("Selected", self.selected_val, "#2563EB")]:
            row = QHBoxLayout()
            l = QLabel(lbl)
            l.setStyleSheet("color: #64748B; border: none;")
            val.setStyleSheet(f"font-weight: 600; color: {color}; border: none;")
            row.addWidget(l)
            row.addStretch()
            row.addWidget(val)
            sidebar_layout.addLayout(row)

        self.preview_btn = QPushButton(" Preview Organization")
        self.preview_btn.setFixedHeight(45)
        self.preview_btn.setCursor(Qt.PointingHandCursor)
        self.preview_btn.setIcon(QIcon(self.ICON_MAPPING['folder']))
        self.preview_btn.clicked.connect(self.preview_organization)
        self.preview_btn.setStyleSheet("""
            QPushButton { background-color: #2563EB; color: white; border-radius: 8px; font-weight: 600; border: none; }
            QPushButton:hover { background-color: #1D4ED8; }
            QPushButton:pressed { background-color: #1E40AF; }
        """)

        self.organize_btn = QPushButton(" Organize Now")
        self.organize_btn.setFixedHeight(45)
        self.organize_btn.setCursor(Qt.PointingHandCursor)
        self.organize_btn.clicked.connect(self.run_organization)
        self.organize_btn.setStyleSheet("""
            QPushButton { background-color: white; color: #0F172A; border: 1px solid #E2E8F0; border-radius: 8px; font-weight: 500; }
            QPushButton:hover { background-color: #F8FAFC; border-color: #CBD5E1; }
            QPushButton:pressed { background-color: #F1F5F9; }
        """)

        sidebar_layout.addWidget(self.preview_btn)
        sidebar_layout.addWidget(self.organize_btn)
        sidebar_layout.addStretch()

        right_panel = QVBoxLayout()
        list_header = QHBoxLayout()
        list_header.addWidget(QLabel("Downloads Folder", styleSheet="font-weight: 600; color: #0F172A;"))
        list_header.addStretch()
        self.deselect_btn = QPushButton("Deselect All")
        self.deselect_btn.clicked.connect(self.toggle_all)
        self.deselect_btn.setStyleSheet("color: #2563EB; border: none; font-size: 12px; font-weight: 500; background: transparent;")
        list_header.addWidget(self.deselect_btn)
        right_panel.addLayout(list_header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.scroll_content = QWidget()
        self.file_list_layout = QVBoxLayout(self.scroll_content)
        self.file_list_layout.setContentsMargins(0, 0, 0, 0)
        self.file_list_layout.setSpacing(8)
        self.scroll.setWidget(self.scroll_content)
        right_panel.addWidget(self.scroll)

        content.addWidget(sidebar)
        content.addLayout(right_panel, 1)
        self.main_layout.addLayout(content)

    def create_selection_card(self, title, desc, checked, id):
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border: 1px solid #E2E8F0; border-radius: 10px; }")
        lay = QHBoxLayout(card)
        rb = QRadioButton()
        rb.setChecked(checked)
        self.group.addButton(rb, id)
        v = QVBoxLayout()
        v.addWidget(QLabel(title, styleSheet="font-weight: 600; color: #1E293B; border: none;"))
        v.addWidget(QLabel(desc, styleSheet="font-size: 11px; color: #64748B; border: none;"))
        lay.addWidget(rb)
        lay.addLayout(v)
        lay.addStretch()
        return card

    def load_real_data(self):
        self.file_checkboxes = {}
        while self.file_list_layout.count():
            child = self.file_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        try:
            files = [f for f in os.scandir(self.downloads_path) if f.is_file()]
            for entry in files:
                ext = os.path.splitext(entry.name)[1].lower()
                row, cb = self.create_file_row(entry.name, entry.stat(), ext, entry.path)
                cb.stateChanged.connect(self.update_counters)
                self.file_list_layout.addWidget(row)
                self.file_checkboxes[entry.path] = cb
            self.total_val.setText(str(len(files)))
            self.update_counters()
            self.file_list_layout.addStretch()
        except Exception as e:
            print(f"Error: {e}")

    def create_file_row(self, name, stats, ext, path):
        row = QFrame()
        row.setStyleSheet("QFrame { background: white; border: 1px solid #F1F5F9; border-radius: 6px; }")
        lay = QHBoxLayout(row)
        cb = QCheckBox()
        cb.setChecked(True)
        icon = QLabel()
        icon.setFixedSize(24, 24)
        pix = QPixmap(self.ICON_MAPPING.get(ext, self.ICON_MAPPING['default']))
        if not pix.isNull():
            icon.setPixmap(pix.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            icon.setText("📄")
        v = QVBoxLayout()
        v.addWidget(QLabel(name, styleSheet="font-weight: 500; font-size: 13px; color: #1E293B; border: none;"))
        date = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d')
        size = self.format_size(stats.st_size)
        v.addWidget(QLabel(f"{size} • {date}", styleSheet="font-size: 11px; color: #94A3B8; border: none;"))
        tag = QLabel(ext.replace('.', '').upper() or "FILE")
        tag.setStyleSheet("background: #F0FDF4; color: #166534; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; border: none;")
        lay.addWidget(cb)
        lay.addWidget(icon)
        lay.addLayout(v)
        lay.addStretch()
        lay.addWidget(tag)
        return row, cb

    def update_counters(self):
        count = sum(1 for cb in self.file_checkboxes.values() if cb.isChecked())
        self.selected_val.setText(str(count))
        self.deselect_btn.setText("Deselect All" if count > 0 else "Select All")

    def toggle_all(self):
        state = not any(cb.isChecked() for cb in self.file_checkboxes.values())
        for cb in self.file_checkboxes.values():
            cb.setChecked(state)

    def get_dest(self, path):
        if self.group.checkedId() == 0:
            ext = os.path.splitext(path)[1].lower()
            for cat, exts in self.EXT_GROUPS.items():
                if ext in exts:
                    return cat
            return "Others"
        return datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m')

    def preview_organization(self):
        plan = {}
        for path, cb in self.file_checkboxes.items():
            if cb.isChecked() and os.path.exists(path):
                d = self.get_dest(path)
                plan[d] = plan.get(d, 0) + 1
        if not plan:
            return QMessageBox.warning(self, "Preview", "No files selected.")
        msg = "Summary:\n" + "\n".join([f"• {k}: {v} files" for k, v in plan.items()])
        QMessageBox.information(self, "Preview", msg)

    def run_organization(self):
        moved = 0
        for path, cb in self.file_checkboxes.items():
            if cb.isChecked() and os.path.exists(path):
                dest_dir = os.path.join(self.downloads_path, self.get_dest(path))
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(path, os.path.join(dest_dir, os.path.basename(path)))
                moved += 1
        QMessageBox.information(self, "Success", f"Moved {moved} files.")
        self.load_real_data()

    def format_size(self, b):
        for u in ['B', 'KB', 'MB', 'GB']:
            if b < 1024:
                return f"{b:.1f}{u}"
            b /= 1024
        return f"{b:.1f}GB"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = OrganizeDownloadPage()
    win.show()
    sys.exit(app.exec_())
