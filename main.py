import os
import sys
from datetime import datetime
from file_shredder import FileShredder
# main.py
from tes import (
    SAFE_ZONES,
    check_anomaly,
    classify_path,
    is_os_file_type,
    is_reparse_point,
)
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QThread, QTimer, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


APP_NAME = "SecureWipe Pro - Windows Edition"


class AppStyles:
    DARK = """
        QMainWindow, QWidget {
            background: #0b111a;
            color: #dbe6f3;
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 14px;
        }
        #Sidebar {
            background: #080d14;
            border-right: 1px solid #1f2b3a;
        }
        #Brand {
            color: #f8fafc;
            font-size: 19px;
            font-weight: 700;
        }
        #Subtitle, #MutedText {
            color: #8ea0b7;
        }
        #PageTitle {
            color: #f8fafc;
            font-size: 24px;
            font-weight: 700;
        }
        #SectionTitle {
            color: #f8fafc;
            font-size: 16px;
            font-weight: 650;
        }
        QPushButton {
            background: #172235;
            border: 1px solid #2b3b52;
            color: #e5eef8;
            padding: 10px 14px;
            border-radius: 8px;
            font-weight: 600;
        }
        QPushButton:hover {
            background: #20304a;
            border-color: #3b82f6;
        }
        QPushButton:pressed {
            background: #111a29;
        }
        QPushButton:disabled {
            background: #10151f;
            border-color: #1c2636;
            color: #566577;
        }
        QPushButton#PrimaryButton {
            background: #2563eb;
            border-color: #3b82f6;
            color: #ffffff;
        }
        QPushButton#PrimaryButton:hover {
            background: #1d4ed8;
        }
        QPushButton#DangerButton {
            background: #361922;
            border-color: #7f1d1d;
            color: #fecaca;
        }
        QListWidget {
            background: transparent;
            border: none;
            outline: 0;
        }
        QListWidget::item {
            padding: 12px 14px;
            margin: 4px 10px;
            border-radius: 8px;
            color: #9fb0c7;
        }
        QListWidget::item:hover {
            background: #111a29;
            color: #f8fafc;
        }
        QListWidget::item:selected {
            background: #1d3557;
            color: #ffffff;
        }
        QFrame#Card {
            background: #111827;
            border: 1px solid #253247;
            border-radius: 14px;
        }
        QTextEdit, QLineEdit, QComboBox {
            background: #0f1724;
            border: 1px solid #2b3b52;
            color: #e2e8f0;
            border-radius: 8px;
            padding: 9px 10px;
        }
        QTextEdit {
            font-family: "Cascadia Mono", "Consolas", monospace;
            font-size: 12px;
        }
        QLineEdit:disabled {
            color: #8ea0b7;
            background: #101723;
        }
        QComboBox::drop-down {
            border: none;
            width: 28px;
        }
        QCheckBox {
            color: #dbe6f3;
            spacing: 8px;
        }
        QProgressBar {
            background: #0f1724;
            border: 1px solid #2b3b52;
            border-radius: 8px;
            color: #dbe6f3;
            text-align: center;
            height: 22px;
        }
        QProgressBar::chunk {
            background: #2563eb;
            border-radius: 7px;
        }
    """

    LIGHT = """
        QMainWindow, QWidget {
            background: #f4f7fb;
            color: #1f2937;
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 14px;
        }
        #Sidebar {
            background: #ffffff;
            border-right: 1px solid #d8e0ea;
        }
        #Brand, #PageTitle, #SectionTitle {
            color: #111827;
            font-weight: 700;
        }
        #Brand { font-size: 19px; }
        #PageTitle { font-size: 24px; }
        #SectionTitle { font-size: 16px; }
        #Subtitle, #MutedText { color: #64748b; }
        QPushButton {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            color: #1f2937;
            padding: 10px 14px;
            border-radius: 8px;
            font-weight: 600;
        }
        QPushButton:hover {
            background: #eff6ff;
            border-color: #2563eb;
        }
        QPushButton:disabled {
            background: #f1f5f9;
            border-color: #e2e8f0;
            color: #94a3b8;
        }
        QPushButton#PrimaryButton {
            background: #2563eb;
            border-color: #2563eb;
            color: #ffffff;
        }
        QPushButton#DangerButton {
            background: #fff1f2;
            border-color: #fecdd3;
            color: #9f1239;
        }
        QListWidget {
            background: transparent;
            border: none;
            outline: 0;
        }
        QListWidget::item {
            padding: 12px 14px;
            margin: 4px 10px;
            border-radius: 8px;
            color: #475569;
        }
        QListWidget::item:hover {
            background: #eef4fb;
            color: #111827;
        }
        QListWidget::item:selected {
            background: #dbeafe;
            color: #1d4ed8;
        }
        QFrame#Card {
            background: #ffffff;
            border: 1px solid #d8e0ea;
            border-radius: 14px;
        }
        QTextEdit, QLineEdit, QComboBox {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            color: #111827;
            border-radius: 8px;
            padding: 9px 10px;
        }
        QTextEdit {
            font-family: "Cascadia Mono", "Consolas", monospace;
            font-size: 12px;
        }
        QLineEdit:disabled {
            color: #64748b;
            background: #f1f5f9;
        }
        QComboBox::drop-down {
            border: none;
            width: 28px;
        }
        QCheckBox {
            color: #1f2937;
            spacing: 8px;
        }
        QProgressBar {
            background: #e2e8f0;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            color: #1f2937;
            text-align: center;
            height: 22px;
        }
        QProgressBar::chunk {
            background: #2563eb;
            border-radius: 7px;
        }
    """


class Card(QFrame):
    def __init__(self, title=None):
        super().__init__()
        self.setObjectName("Card")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(12)

        if title:
            title_label = QLabel(title)
            title_label.setObjectName("SectionTitle")
            self.layout.addWidget(title_label)


class LogBus:
    def __init__(self):
        self.entries = []
        self.listeners = []

    def subscribe(self, callback):
        self.listeners.append(callback)

    def add(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.entries.append(entry)
        print(entry)
        for listener in self.listeners:
            listener(entry)

    def clear(self):
        self.entries.clear()
        for listener in self.listeners:
            listener(None)


class SimulatedProgress:
    def __init__(self, progress_bar, steps, log_bus, done_message=None):
        self.progress_bar = progress_bar
        self.steps = steps
        self.log_bus = log_bus
        self.done_message = done_message
        self.index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.advance)

    def start(self):
        self.index = 0
        self.progress_bar.setValue(0)
        self.timer.start(550)

    def advance(self):
        if self.index < len(self.steps):
            progress, message = self.steps[self.index]
            self.progress_bar.setValue(progress)
            self.log_bus.add(message)
            self.index += 1
            return

        self.timer.stop()
        self.progress_bar.setValue(100)
        if self.done_message:
            QMessageBox.information(None, "Simulation Complete", self.done_message)


class ShredWorker(QThread):
    """
    Runs FileShredder.shred() on a background thread so the GUI
    stays responsive during a (potentially slow) real overwrite pass.
    """

    progress_updated = Signal(int)
    log_message = Signal(str)
    finished_result = Signal(bool, str)

    def __init__(self, filepath, passes):
        super().__init__()
        self.filepath = filepath
        self.passes = passes

    def run(self):
        try:
            shredder = FileShredder(
                passes=self.passes,
                progress_callback=self.progress_updated.emit,
                log_callback=self.log_message.emit,
            )
            shredder.shred(self.filepath)
            self.finished_result.emit(
                True, "File was securely overwritten and deleted."
            )
        except Exception as exc:  # surfaced in the UI rather than crashing the app
            self.finished_result.emit(False, str(exc))


class FileWiperPage(QWidget):
    """UI for securely overwriting and deleting one user-selected file."""

    WIPE_MODES = [
        ("Quick wipe (1 pass)", 1),
        ("Secure wipe (3 passes)", 3),
        ("Maximum wipe (7 passes)", 7),
    ]

    def __init__(self, log_bus):
        super().__init__()
        self.log_bus = log_bus
        self.selected_file = ""
        self.worker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        title = QLabel("File Wiper")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        card = Card("Secure File Deletion")
        layout.addWidget(card)

        choose_button = QPushButton("Choose File")
        choose_button.clicked.connect(self.pick_file)
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("MutedText")
        self.file_label.setWordWrap(True)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems([label for label, _ in self.WIPE_MODES])
        self.mode_combo.setCurrentIndex(1)

        self.start_button = QPushButton("Securely Delete File")
        self.start_button.setObjectName("DangerButton")
        self.start_button.clicked.connect(self.start_wipe)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(150)

        card.layout.addWidget(choose_button)
        card.layout.addWidget(self.file_label)
        card.layout.addWidget(QLabel("Wipe mode"))
        card.layout.addWidget(self.mode_combo)
        card.layout.addWidget(self.start_button)
        card.layout.addWidget(self.progress)
        card.layout.addWidget(self.output)
        layout.addStretch()

    def pick_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File to Securely Delete")
        if path:
            self.selected_file = path
            self.file_label.setText(path)
            self.log_bus.add(f"File selected for secure wipe: {path}")

    def start_wipe(self):
        if not self.selected_file or not os.path.isfile(self.selected_file):
            QMessageBox.warning(self, "No File Selected", "Choose an existing file before starting a wipe.")
            return

        name = os.path.basename(self.selected_file)
        answer = QMessageBox.question(
            self,
            "Confirm Secure File Deletion",
            f"This will permanently overwrite and delete:\n\n{name}\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            self.log_bus.add("File wipe cancelled by user")
            return

        _, passes = self.WIPE_MODES[self.mode_combo.currentIndex()]
        self.start_button.setEnabled(False)
        self.progress.setValue(0)
        self.output.clear()
        self.log_bus.add(f"Starting secure file wipe: {self.selected_file} ({passes} pass(es))")

        self.worker = ShredWorker(self.selected_file, passes)
        self.worker.progress_updated.connect(self.progress.setValue)
        self.worker.log_message.connect(self.append_log)
        self.worker.finished_result.connect(self.wipe_finished)
        self.worker.start()

    def append_log(self, message):
        self.output.append(message)
        self.log_bus.add(message)

    def wipe_finished(self, success, message):
        self.start_button.setEnabled(True)
        self.log_bus.add(f"File Wiper: {message}")
        if success:
            self.selected_file = ""
            self.file_label.setText("No file selected")
            QMessageBox.information(self, "File Wipe Complete", message)
        else:
            QMessageBox.critical(self, "File Wipe Failed", message)


class FolderShredWorker(QThread):
    file_evaluated   = Signal(str, bool, str)   # path, skipped, reason
    progress_updated = Signal(int)
    log_message      = Signal(str)
    finished_result  = Signal(bool, str, list)  # success, message, skipped_paths

    def __init__(self, folder, passes, include_subfolders):
        super().__init__()
        self.folder = folder
        self.passes = passes
        self.include_subfolders = include_subfolders

    def run(self):
        try:
            files = self._collect_files()
            to_delete, skipped = [], []
            scope = "including subfolders" if self.include_subfolders else "in the selected folder"
            self.log_message.emit(f"Found {len(files)} file(s) {scope}.")

            for i, fp in enumerate(files):
                zone = classify_path(fp)
                anomaly = check_anomaly(fp, zone)

                if is_os_file_type(fp):
                    skipped.append(fp)
                    extension = os.path.splitext(fp)[1].lower()
                    self.file_evaluated.emit(
                        fp, True, f"Protected OS/application file type: {extension}"
                    )
                elif zone not in SAFE_ZONES:
                    skipped.append(fp)
                    self.file_evaluated.emit(fp, True, f"Zone: {zone}")
                elif anomaly:
                    skipped.append(fp)
                    self.file_evaluated.emit(fp, True, anomaly)
                else:
                    to_delete.append(fp)
                    self.file_evaluated.emit(fp, False, f"Zone: {zone}")

                self.progress_updated.emit(int((i + 1) / max(len(files), 1) * 40))

            shredder = FileShredder(
                passes=self.passes,
                progress_callback=lambda p: self.progress_updated.emit(40 + int(p * 0.6)),
                log_callback=self.log_message.emit,
            )
            for fp in to_delete:
                shredder.shred(fp)

            # A scan that only finds protected files does not invoke the
            # shredder's callback, so explicitly mark the completed run.
            self.progress_updated.emit(100)
            msg = f"Deleted {len(to_delete)} file(s). Skipped {len(skipped)} (OS/app-critical or flagged)."
            self.finished_result.emit(True, msg, skipped)
        except Exception as exc:
            self.finished_result.emit(False, str(exc), [])

    def _collect_files(self):
        files = []
        if self.include_subfolders:
            for dp, dns, fns in os.walk(self.folder, topdown=True):
                dns[:] = [d for d in dns if not is_reparse_point(os.path.join(dp, d))]
                files.extend(os.path.join(dp, fn) for fn in fns)
        else:
            files = [os.path.join(self.folder, n) for n in os.listdir(self.folder)
                      if os.path.isfile(os.path.join(self.folder, n))]
        return files

class DashboardPage(QWidget):
    def __init__(self, log_bus, navigate_callback):
        super().__init__()
        self.log_bus = log_bus
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(16)
        layout.addLayout(grid)

        status = Card("System Status")
        status.layout.addWidget(self.muted_label("Windows Environment Detected"))
        status.layout.addWidget(
            self.muted_label(
                "File Wiper performs real secure deletion. Folder/Disk wiping is still simulated."
            )
        )
        grid.addWidget(status, 0, 0)

        device = Card("Selected Device")
        drive_box = QComboBox()
        drive_box.addItems(["HDD 0 - C: - 512 GB - System", "HDD 1 - D: - 1 TB - Archive"])
        device.layout.addWidget(drive_box)
        device.layout.addWidget(self.muted_label("Dummy HDD inventory for UI demonstration only."))
        grid.addWidget(device, 0, 1)

        quick = Card("Quick Actions")
        buttons = QHBoxLayout()
        for text, page_index in [("Wipe File", 1), ("Wipe Folder", 2), ("Wipe Disk", 3)]:
            button = QPushButton(text)
            button.setObjectName("PrimaryButton")
            button.clicked.connect(lambda checked=False, t=text, i=page_index: self.quick_action(t, i, navigate_callback))
            buttons.addWidget(button)
        quick.layout.addLayout(buttons)
        grid.addWidget(quick, 1, 0, 1, 2)

        layout.addStretch()

    def quick_action(self, action, page_index, navigate_callback):
        self.log_bus.add(f"Quick action selected: {action}")
        navigate_callback(page_index)

    @staticmethod
    def muted_label(text):
        label = QLabel(text)
        label.setObjectName("MutedText")
        label.setWordWrap(True)
        return label


class FolderWiperPage(QWidget):
    def __init__(self, log_bus):
        super().__init__()
        self.log_bus = log_bus
        self.worker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        title = QLabel("Folder Wiper")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        card = Card("Secure Folder Deletion")
        layout.addWidget(card)

        pick_button = QPushButton("Choose Folder")
        pick_button.clicked.connect(self.pick_folder)

        self.folder_label = QLabel("No folder selected")
        self.folder_label.setObjectName("MutedText")
        self.folder_label.setWordWrap(True)

        self.include_subfolders = QCheckBox("Include subfolders")
        self.include_subfolders.setChecked(True)

        warning = QLabel(
            "This scans the folder and permanently deletes files classified as "
            "safe (user/app data). OS-critical files are automatically skipped. This cannot be undone."
        )
        warning.setStyleSheet("color: #fca5a5; font-weight: 700;")
        warning.setWordWrap(True)

        self.start_button = QPushButton("Start Secure Folder Wipe")
        self.start_button.setObjectName("DangerButton")
        self.start_button.clicked.connect(self.start_wipe)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setMinimumHeight(220)

        card.layout.addWidget(pick_button)
        card.layout.addWidget(self.folder_label)
        card.layout.addWidget(self.include_subfolders)
        card.layout.addWidget(warning)
        card.layout.addWidget(self.start_button)
        card.layout.addWidget(self.progress_bar)
        card.layout.addWidget(self.log_panel)

        layout.addStretch()

    def pick_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder to Wipe")
        if path:
            self.folder_label.setText(path)
            self.log_bus.add(f"Folder selected for secure wipe: {path}")

    def start_wipe(self):
        folder = self.folder_label.text()
        if folder == "No folder selected":
            QMessageBox.warning(self, "No Folder Selected", "Choose a folder before starting a wipe.")
            return

        response = QMessageBox.warning(
            self,
            "Confirm Secure Folder Wipe",
            f"This will scan and permanently delete non-critical files in:\n\n{folder}\n\n"
            "OS/application-critical files will be automatically skipped.\n"
            "This action CANNOT be undone. Continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if response != QMessageBox.Yes:
            self.log_bus.add("Folder wipe cancelled by user")
            return

        self.log_panel.clear()
        self.progress_bar.setValue(0)
        self.start_button.setEnabled(False)

        self.append_log(f"Starting secure folder wipe: {folder}")

        self.worker = FolderShredWorker(
            folder,
            passes=3,
            include_subfolders=self.include_subfolders.isChecked(),
        )
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.log_message.connect(self.append_log)
        self.worker.file_evaluated.connect(self.log_evaluation)
        self.worker.finished_result.connect(self.on_wipe_finished)
        self.worker.start()

    def log_evaluation(self, path, skipped, reason):
        tag = "SKIP" if skipped else "DELETE"
        self.append_log(f"[{tag}] {os.path.basename(path)} — {reason}")

    def on_wipe_finished(self, success, message, skipped_paths):
        self.start_button.setEnabled(True)
        self.append_log(message)
        if success:
            QMessageBox.information(self, "Folder Wipe Complete", message)
        else:
            QMessageBox.critical(self, "Folder Wipe Failed", message)
        self.worker = None

    def append_log(self, message):
        self.log_panel.append(message)
        self.log_bus.add(f"Folder Wiper: {message}")


class DiskWiperPage(QWidget):
    def __init__(self, log_bus):
        super().__init__()
        self.log_bus = log_bus
        self.progress = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        title = QLabel("Disk Wiper")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        card = Card("Disk Wipe Simulation")
        layout.addWidget(card)

        self.drive = QComboBox()
        self.drive.addItems(["C:  |  512 GB  |  HDD  |  System", "D:  |  1 TB  |  HDD  |  Archive"])
        self.drive.currentTextChanged.connect(self.update_drive_info)

        self.drive_info = QLabel()
        self.drive_info.setObjectName("MutedText")
        self.drive_info.setWordWrap(True)
        self.update_drive_info(self.drive.currentText())

        self.level = QComboBox()
        self.level.addItems(["Quick format (simulated)", "Secure overwrite (simulated)"])

        warning = QLabel("This operation will permanently erase all data (SIMULATION ONLY)")
        warning.setStyleSheet("color: #fca5a5; font-weight: 700;")
        warning.setWordWrap(True)

        start_button = QPushButton("Start Disk Wipe Simulation")
        start_button.setObjectName("DangerButton")
        start_button.clicked.connect(self.confirm_and_start)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setMinimumHeight(220)

        card.layout.addWidget(QLabel("Select HDD drive"))
        card.layout.addWidget(self.drive)
        card.layout.addWidget(self.drive_info)
        card.layout.addWidget(QLabel("Wipe level"))
        card.layout.addWidget(self.level)
        card.layout.addWidget(warning)
        card.layout.addWidget(start_button)
        card.layout.addWidget(self.progress_bar)
        card.layout.addWidget(self.log_panel)

        layout.addStretch()

    def update_drive_info(self, value):
        drive_letter = value.split("|")[0].strip()
        capacity = "512 GB" if drive_letter == "C:" else "1 TB"
        self.drive_info.setText(
            f"Drive: {drive_letter}\nCapacity: {capacity}\nType: HDD\nStatus: Dummy UI data only"
        )

    def confirm_and_start(self):
        response = QMessageBox.warning(
            self,
            "Confirm Simulation",
            "This is a UI-only simulation. No disk operation will run.\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if response != QMessageBox.Yes:
            self.log_bus.add("Disk wipe simulation cancelled")
            return

        self.log_panel.clear()
        selected = self.drive.currentText().split("|")[0].strip()
        self.log_panel.append(f"Simulated disk wipe started for {selected}")
        self.log_bus.add(f"Simulated disk wipe started for {selected}")
        steps = [
            (12, "Lock request simulated..."),
            (28, "Scanning dummy drive metadata..."),
            (52, "Writing simulated overwrite pattern..."),
            (78, "Verifying fake wipe report..."),
            (100, "Disk wipe complete (SIMULATED)"),
        ]
        self.progress = SimulatedProgress(
            self.progress_bar,
            steps,
            self.append_log,
            "Disk wipe simulation completed.",
        )
        self.progress.start()

    def append_log(self, message):
        self.log_panel.append(message)
        self.log_bus.add(f"Disk Wiper: {message}")


class LogsPage(QWidget):
    def __init__(self, log_bus):
        super().__init__()
        self.log_bus = log_bus
        self.log_bus.subscribe(self.receive_log)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        title = QLabel("Logs")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        card = Card("Action Console")
        layout.addWidget(card)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(420)

        clear_button = QPushButton("Clear Logs")
        clear_button.clicked.connect(self.clear_logs)

        card.layout.addWidget(self.console)
        card.layout.addWidget(clear_button)
        layout.addStretch()

    def receive_log(self, entry):
        if entry is None:
            self.console.clear()
            return
        self.console.append(entry)

    def clear_logs(self):
        self.log_bus.clear()
        print("Logs cleared (UI only)")


class SettingsPage(QWidget):
    def __init__(self, apply_theme):
        super().__init__()
        self.apply_theme = apply_theme

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        title = QLabel("Settings")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        card = Card("Application Preferences")
        layout.addWidget(card)

        theme_row = QHBoxLayout()
        theme_label = QLabel("Theme")
        self.theme_toggle = QComboBox()
        self.theme_toggle.addItems(["Dark", "Light"])
        self.theme_toggle.currentTextChanged.connect(self.apply_theme)
        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.theme_toggle)

        self.default_mode = QComboBox()
        self.default_mode.addItems([label for label, _ in FileWiperPage.WIPE_MODES])

        self.audit = QCheckBox("Enable audit logging")
        self.audit.setChecked(True)

        self.key = QLineEdit("SWP-DEMO-KEY-0000-0000")
        self.key.setDisabled(True)

        card.layout.addLayout(theme_row)
        card.layout.addWidget(QLabel("Default wipe mode"))
        card.layout.addWidget(self.default_mode)
        card.layout.addWidget(self.audit)
        card.layout.addWidget(QLabel("Dummy security key"))
        card.layout.addWidget(self.key)

        layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1180, 760)
        self.setMinimumSize(980, 640)

        self.log_bus = LogBus()

        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = self.create_sidebar()
        root_layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        root_layout.addWidget(self.stack)

        self.pages = [
            DashboardPage(self.log_bus, self.navigate_to),
            FileWiperPage(self.log_bus),
            FolderWiperPage(self.log_bus),
            DiskWiperPage(self.log_bus),
            LogsPage(self.log_bus),
            SettingsPage(self.apply_theme),
        ]
        for page in self.pages:
            wrapper = QWidget()
            wrapper_layout = QVBoxLayout(wrapper)
            wrapper_layout.setContentsMargins(28, 26, 28, 26)
            wrapper_layout.addWidget(page)
            self.stack.addWidget(wrapper)

        self.nav.setCurrentRow(0)
        self.apply_theme("Dark")
        self.log_bus.add("SecureWipe Pro GUI started")

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(250)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 24, 0, 20)
        layout.setSpacing(14)

        brand = QLabel("SecureWipe Pro")
        brand.setObjectName("Brand")
        brand.setAlignment(Qt.AlignCenter)
        subtitle = QLabel("Windows Edition")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(brand)
        layout.addWidget(subtitle)

        self.nav = QListWidget()
        self.nav.addItems(["Dashboard", "File Wiper", "Folder Wiper", "Disk Wiper", "Logs", "Settings"])
        self.nav.currentRowChanged.connect(self.navigate_to)
        layout.addWidget(self.nav)

        mode = QLabel("File Wiper performs real, permanent secure deletion.\nFolder/Disk wiping is still simulated.")
        mode.setObjectName("MutedText")
        mode.setWordWrap(True)
        mode.setAlignment(Qt.AlignCenter)
        mode.setContentsMargins(18, 0, 18, 0)
        layout.addWidget(mode)

        return sidebar

    def navigate_to(self, index):
        self.stack.setCurrentIndex(index)
        if self.nav.currentRow() != index:
            self.nav.setCurrentRow(index)

        animation = QPropertyAnimation(self.stack.currentWidget(), b"windowOpacity")
        animation.setDuration(150)
        animation.setStartValue(0.72)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        self._animation = animation

    def apply_theme(self, theme):
        QApplication.instance().setStyleSheet(AppStyles.LIGHT if theme == "Light" else AppStyles.DARK)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
