import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QCheckBox, 
                             QScrollArea, QFrame, QGridLayout, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt

class BatchRenameUI(QWidget):
    def __init__(self):
        super().__init__()
        self.all_rows = [] 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Batch Rename Files')
        self.resize(1100, 700)
        self.setStyleSheet("background-color: #f8fafc;")

        self.scrollbar_style = """
            QScrollBar:vertical { border: none; background: #f1f5f9; width: 8px; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #cbd5e1; min-height: 20px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #94a3b8; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """

        main_outer_layout = QVBoxLayout(self)
        main_outer_layout.setContentsMargins(0, 0, 0, 0)
        master_scroll = QScrollArea()
        master_scroll.setWidgetResizable(True)
        master_scroll.setFrameShape(QFrame.NoFrame)
        master_scroll.setStyleSheet(self.scrollbar_style + "background-color: #f8fafc;")
        main_outer_layout.addWidget(master_scroll)

        container = QWidget()
        master_scroll.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Batch Rename Files")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b;")
        subtitle = QLabel("Rename multiple files at once using patterns and rules")
        subtitle.setStyleSheet("font-size: 13px; color: #64748b;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        # --- LEFT COLUMN ---
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame { background-color: white; border-radius: 8px; border: 1px solid #e2e8f0; }
            QLabel { border: none; color: #475569; font-weight: bold; font-size: 11px; }
            QLineEdit { border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px; background: white; }
        """)
        left_vbox = QVBoxLayout(left_panel)
        left_vbox.setContentsMargins(20, 20, 20, 20)
        left_vbox.setSpacing(15)

        left_vbox.addWidget(QLabel("Select Folder"))
        folder_hbox = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        self.browse_btn.setStyleSheet("""
            QPushButton { 
                background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 4px; 
                padding: 6px 12px; font-size: 11px; color: #475569; font-weight: bold;
            }
            QPushButton:hover { background: #e2e8f0; border: 1px solid #94a3b8; }
        """)
        folder_hbox.addWidget(self.folder_input)
        folder_hbox.addWidget(self.browse_btn)
        left_vbox.addLayout(folder_hbox)

        left_vbox.addWidget(QLabel("Rename Pattern (optional)"))
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("e.g., Photo_{n}")
        left_vbox.addWidget(self.pattern_input)

        num_grid = QGridLayout()
        num_grid.addWidget(QLabel("Start Number"), 0, 0)
        num_grid.addWidget(QLabel("Padding"), 0, 1)
        self.start_num = QLineEdit("1")
        self.padding_num = QLineEdit("3")
        num_grid.addWidget(self.start_num, 1, 0)
        num_grid.addWidget(self.padding_num, 1, 1)
        left_vbox.addLayout(num_grid)

        left_vbox.addWidget(QLabel("Find and Replace (optional)"))
        self.find_input = QLineEdit(placeholderText="Find text...")
        self.replace_input = QLineEdit(placeholderText="Replace with...")
        left_vbox.addWidget(self.find_input)
        left_vbox.addWidget(self.replace_input)

        fix_grid = QGridLayout()
        fix_grid.addWidget(QLabel("Prefix"), 0, 0)
        fix_grid.addWidget(QLabel("Suffix"), 0, 1)
        self.prefix_input = QLineEdit(placeholderText="Add prefix...")
        self.suffix_input = QLineEdit(placeholderText="Add suffix...")
        fix_grid.addWidget(self.prefix_input, 1, 0)
        fix_grid.addWidget(self.suffix_input, 1, 1)
        left_vbox.addLayout(fix_grid)

        left_vbox.addStretch()

        stats_layout = QGridLayout()
        stats_layout.addWidget(QLabel("Total files"), 0, 0)
        self.total_lbl = QLabel("0")
        stats_layout.addWidget(self.total_lbl, 0, 1, Qt.AlignRight)
        stats_layout.addWidget(QLabel("Selected"), 1, 0)
        self.selected_lbl = QLabel("0")
        stats_layout.addWidget(self.selected_lbl, 1, 1, Qt.AlignRight)
        left_vbox.addLayout(stats_layout)

        self.apply_btn = QPushButton("Apply Changes")
        self.apply_btn.setCursor(Qt.PointingHandCursor)
        self.apply_btn.setFixedHeight(45)
        self.apply_btn.setStyleSheet("""
            QPushButton { 
                background-color: transparent;
                color: #2563eb; 
                border: 2px solid #2563eb;
                border-radius: 6px; 
                font-weight: bold; 
                font-size: 13px;
            }
            QPushButton:hover { 
                background-color: #2563eb;
                color: white;
            }
            QPushButton:pressed { 
                background-color: #1e40af;
                border-color: #1e40af;
                color: white;
            }
        """)
        left_vbox.addWidget(self.apply_btn)

        # --- RIGHT COLUMN ---
        right_panel = QVBoxLayout()
        right_header = QHBoxLayout()
        right_header.addWidget(QLabel("Files Preview", styleSheet="font-size: 14px; font-weight: bold; color: #1e293b;"))
        right_header.addStretch()
        right_panel.addLayout(right_header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self.scrollbar_style + "border: 1px solid #e2e8f0; border-radius: 8px; background-color: white;")
        
        self.file_list_widget = QWidget()
        self.file_list_layout = QVBoxLayout(self.file_list_widget)
        self.file_list_layout.setContentsMargins(0, 0, 0, 0)
        self.file_list_layout.setSpacing(0)
        
        scroll.setWidget(self.file_list_widget)
        right_panel.addWidget(scroll)

        content_layout.addWidget(left_panel, 1)
        content_layout.addLayout(right_panel, 2)
        main_layout.addLayout(content_layout)

        # --- LOGIC CONNECTIONS ---
        self.browse_btn.clicked.connect(self.select_directory)
        self.apply_btn.clicked.connect(self.run_rename)
        
        settings_widgets = [self.pattern_input, self.find_input, self.replace_input, 
                            self.prefix_input, self.suffix_input, self.start_num, self.padding_num]
        for w in settings_widgets:
            w.textChanged.connect(self.refresh_preview)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if dir_path:
            self.folder_input.setText(dir_path)
            self.refresh_preview()

    def refresh_preview(self):
        for i in reversed(range(self.file_list_layout.count())): 
            widget = self.file_list_layout.itemAt(i).widget()
            if widget: widget.setParent(None)
        self.all_rows = []

        path = self.folder_input.text()
        if not os.path.isdir(path): return

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        self.total_lbl.setText(str(len(files)))
        self.selected_lbl.setText(str(len(files)))

        try:
            start = int(self.start_num.text())
            padding = int(self.padding_num.text())
        except ValueError:
            start, padding = 1, 1

        for i, filename in enumerate(files):
            new_name = self.calculate_new_name(filename, i + start, padding)
            self.add_file_row(filename, new_name)
        self.file_list_layout.addStretch()

    def calculate_new_name(self, old_name, index, padding):
        name_part, ext = os.path.splitext(old_name)
        pattern = self.pattern_input.text()
        res = pattern.replace("{n}", str(index).zfill(padding)) if "{n}" in pattern else name_part
        find_val = self.find_input.text()
        if find_val:
            res = res.replace(find_val, self.replace_input.text())
        return f"{self.prefix_input.text()}{res}{self.suffix_input.text()}{ext}"

    def add_file_row(self, old_name, new_name):
        row = QFrame()
        row.setStyleSheet("border-bottom: 1px solid #f1f5f9; padding: 10px; border-radius: 0px; background: white;")
        row_layout = QHBoxLayout(row)
        cb = QCheckBox()
        cb.setChecked(True)
        name_lbl = QLabel(f"{old_name}  →  {new_name}")
        name_lbl.setStyleSheet("color: #475569; font-size: 12px; border: none;")
        row_layout.addWidget(cb)
        row_layout.addWidget(name_lbl)
        row_layout.addStretch()
        self.file_list_layout.addWidget(row)
        self.all_rows.append((cb, old_name, new_name))

    def run_rename(self):
        path = self.folder_input.text()
        count = 0
        for cb, old, new in self.all_rows:
            if cb.isChecked() and old != new:
                try:
                    os.rename(os.path.join(path, old), os.path.join(path, new))
                    count += 1
                except Exception as e:
                    print(f"Error: {e}")
        
        QMessageBox.information(self, "Rename Complete", f"Successfully renamed {count} files.")
        self.refresh_preview()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BatchRenameUI()
    ex.show()
    sys.exit(app.exec_())