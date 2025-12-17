import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QFrame, QTreeView, 
                             QFileSystemModel, QHeaderView)
from PyQt5.QtCore import Qt, QDir, QSize
from PyQt5.QtGui import QIcon

class FileBrowserUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Browser")
        self.resize(1100, 700)
        self.setStyleSheet("background-color: white; font-family: 'Segoe UI', sans-serif;")
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 20)
        self.main_layout.setSpacing(0)

        # --- HEADER SECTION ---
        self.title = QLabel("File Browser")
        self.title.setStyleSheet("font-size: 20px; font-weight: 600; color: #0F172A;")
        
        self.subtitle = QLabel("Browse and manage your files and folders")
        self.subtitle.setStyleSheet("font-size: 14px; color: #64748B; margin-bottom: 25px;")
        
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.subtitle)

        # --- TOOLBAR SECTION ---
        toolbar_container = QFrame()
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 15)
        toolbar_layout.setSpacing(10)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search files and folders...")
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet("border: 1px solid #E2E8F0; border-radius: 6px; padding-left: 15px;")
        
        self.upload_btn = QPushButton("  Upload")
        self.upload_btn.setFixedHeight(40)
        self.upload_btn.setFixedWidth(110)
        self.upload_btn.setStyleSheet("background-color: #2563EB; color: white; border-radius: 6px; font-weight: 500;")

        self.new_folder_btn = QPushButton("  New Folder")
        self.new_folder_btn.setFixedHeight(40)
        self.new_folder_btn.setFixedWidth(120)
        self.new_folder_btn.setStyleSheet("background-color: white; border: 1px solid #E2E8F0; border-radius: 6px;")

        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.upload_btn)
        toolbar_layout.addWidget(self.new_folder_btn)
        self.main_layout.addWidget(toolbar_container)

        # --- FILE SYSTEM VIEW ---
        self.model = QFileSystemModel()
        root_path = QDir.homePath() 
        self.model.setRootPath(root_path)
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(root_path))
        self.tree.setIndentation(25)
        self.tree.setAnimated(True)
        self.tree.setFrameShape(QFrame.NoFrame)
        
        # Hide headers to match the clean UI look
        self.tree.header().hide()
        self.tree.header().setSectionResizeMode(0, QHeaderView.Stretch)

        self.tree.setStyleSheet("""
            QTreeView { border: 1px solid #F1F5F9; border-radius: 8px; color: #475569; outline: none; }
            QTreeView::item { padding: 10px; height: 45px; border-bottom: 1px solid #F8FAFC; }
            QTreeView::item:selected { background-color: #F1F5F9; color: #2563EB; }
        """)

        self.main_layout.addWidget(self.tree)

        # --- FOOTER SECTION ---
        footer_frame = QFrame()
        footer_frame.setFixedHeight(60)
        footer_layout = QHBoxLayout(footer_frame)
        
        self.stats_label = QLabel("Select a file to see details")
        self.stats_label.setStyleSheet("color: #64748B; font-size: 13px;")
        
        self.size_label = QLabel("")
        self.size_label.setStyleSheet("color: #0F172A; font-weight: 600; font-size: 13px;")
        
        footer_layout.addWidget(self.stats_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.size_label)
        
        self.main_layout.addWidget(footer_frame)

        # --- CONNECTIONS ---
        self.tree.doubleClicked.connect(self.open_file)
        # Connect selection change to our update function
        self.tree.selectionModel().selectionChanged.connect(self.update_footer_info)

    def format_size(self, size):
        """Converts bytes to a human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"

    def update_footer_info(self):
        """Updates the footer with the selected file's name and size."""
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        file_name = self.model.fileName(index)
        
        if os.path.isdir(file_path):
            self.stats_label.setText(f"Folder: {file_name}")
            self.size_label.setText("--") # Calculating folder size is slow; usually left blank
        else:
            file_size = self.model.size(index)
            self.stats_label.setText(f"File: {file_name}")
            self.size_label.setText(f"Size: {self.format_size(file_size)}")

    def open_file(self, index):
        path = self.model.filePath(index)
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':
            import subprocess
            subprocess.call(['open', path])
        else:
            import subprocess
            subprocess.call(['xdg-open', path])
