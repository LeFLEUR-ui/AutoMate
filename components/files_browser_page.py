import sys
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QFrame, QTreeView, 
                             QFileSystemModel, QHeaderView, QFileDialog, QInputDialog, QMessageBox)
from PyQt5.QtCore import Qt, QDir, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QFont

class FileBrowserUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Browser")
        self.resize(1100, 700)
        self.setStyleSheet("background-color: white; font-family: 'Segoe UI', sans-serif;")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 20)
        self.main_layout.setSpacing(0)

        self.title = QLabel("File Browser")
        self.title.setStyleSheet("font-size: 20px; font-weight: 600; color: #0F172A;")
        
        self.subtitle = QLabel("Browse drives, files, and folders")
        self.subtitle.setStyleSheet("font-size: 14px; color: #64748B; margin-bottom: 25px;")
        
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.subtitle)

        toolbar_container = QFrame()
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 15)
        toolbar_layout.setSpacing(10)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search drives, files, and folders...")
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E2E8F0; 
                border-radius: 6px; 
                padding-left: 15px;
                background-color: #F8FAFC;
            }
            QLineEdit:focus {
                border: 1px solid #2563EB;
            }
        """)
        
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.setFixedHeight(40)
        self.upload_btn.setFixedWidth(110)
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB; 
                color: white; 
                border-radius: 6px; 
                font-weight: 500;
            }
            QPushButton:hover { background-color: #1D4ED8; }
        """)

        self.new_folder_btn = QPushButton("New Folder")
        self.new_folder_btn.setFixedHeight(40)
        self.new_folder_btn.setFixedWidth(120)
        self.new_folder_btn.setCursor(Qt.PointingHandCursor)
        self.new_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: white; 
                border: 1px solid #E2E8F0; 
                border-radius: 6px;
                color: #475569;
            }
            QPushButton:hover { background-color: #F8FAFC; }
        """)

        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.upload_btn)
        toolbar_layout.addWidget(self.new_folder_btn)
        self.main_layout.addWidget(toolbar_container)

        self.model = QFileSystemModel()
        self.model.setRootPath("") 

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setRecursiveFilteringEnabled(True)

        self.tree = QTreeView()
        self.tree.setModel(self.proxy_model)

        self.tree.setRootIndex(self.proxy_model.mapFromSource(self.model.index("")))
        
        self.tree.setIndentation(25)
        self.tree.setAnimated(True)
        self.tree.setFrameShape(QFrame.NoFrame)
        self.tree.header().hide()
        self.tree.header().setSectionResizeMode(0, QHeaderView.Stretch)

        self.tree.setStyleSheet("""
            QTreeView { 
                border: 1px solid #F1F5F9; 
                border-radius: 8px; 
                color: #475569; 
                outline: none; 
            }
            QTreeView::item { 
                padding: 10px; 
                height: 45px; 
                border-bottom: 1px solid #F8FAFC; 
            }
            QTreeView::item:selected { 
                background-color: #F1F5F9; 
                color: #2563EB; 
            }
            QScrollBar:vertical {
                border: none; background: transparent; width: 8px; margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1; min-height: 40px; border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover { background: #94A3B8; }
            QScrollBar:horizontal {
                border: none; background: transparent; height: 8px; margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #CBD5E1; min-width: 40px; border-radius: 4px;
            }
        """)

        self.main_layout.addWidget(self.tree)

        footer_frame = QFrame()
        footer_frame.setFixedHeight(60)
        footer_layout = QHBoxLayout(footer_frame)
        
        self.stats_label = QLabel("Select a drive or file to see details")
        self.stats_label.setStyleSheet("color: #64748B; font-size: 13px;")
        
        self.size_label = QLabel("")
        self.size_label.setStyleSheet("color: #0F172A; font-weight: 600; font-size: 13px;")
        
        footer_layout.addWidget(self.stats_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.size_label)
        
        self.main_layout.addWidget(footer_frame)

        self.tree.doubleClicked.connect(self.open_file)
        self.tree.selectionModel().selectionChanged.connect(self.update_footer_info)
        self.upload_btn.clicked.connect(self.handle_upload)
        self.new_folder_btn.clicked.connect(self.handle_new_folder)
        self.search_input.textChanged.connect(self.handle_search)

    def handle_search(self, text):
        reg_exp = QRegExp(text, Qt.CaseInsensitive, QRegExp.Wildcard)
        self.proxy_model.setFilterRegExp(reg_exp)

    def handle_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if file_path:
            index = self.tree.currentIndex()
            source_index = self.proxy_model.mapToSource(index)

            dest_dir = self.model.filePath(source_index) if os.path.isdir(self.model.filePath(source_index)) else QDir.homePath()
            try:
                shutil.copy(file_path, dest_dir)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not upload file: {str(e)}")

    def handle_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, 'New Folder', 'Enter folder name:')
        if ok and folder_name:
            index = self.tree.currentIndex()
            source_index = self.proxy_model.mapToSource(index)
            parent_path = self.model.filePath(source_index) if os.path.isdir(self.model.filePath(source_index)) else QDir.homePath()
            new_path = os.path.join(parent_path, folder_name)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            else:
                QMessageBox.warning(self, "Warning", "Folder already exists.")

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"

    def update_footer_info(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return
        
        source_index = self.proxy_model.mapToSource(index)
        file_path = self.model.filePath(source_index)
        file_name = self.model.fileName(source_index)
        
        if not file_name: # Handle Drive root cases
            file_name = file_path

        if os.path.isdir(file_path):
            self.stats_label.setText(f"Folder/Drive: {file_name}")
            self.size_label.setText("--")
        else:
            file_size = self.model.size(source_index)
            self.stats_label.setText(f"File: {file_name}")
            self.size_label.setText(f"Size: {self.format_size(file_size)}")

    def open_file(self, index):
        source_index = self.proxy_model.mapToSource(index)
        path = self.model.filePath(source_index)
        try:
            if sys.platform == 'win32':
                os.startfile(path)
            elif sys.platform == 'darwin':
                import subprocess
                subprocess.call(['open', path])
            else:
                import subprocess
                subprocess.call(['xdg-open', path])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open file: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = FileBrowserUI()
    window.show()
    sys.exit(app.exec_())