"""Regression tests for file-type protection used by the folder wiper."""

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from tes import is_os_file_type  # noqa: E402

try:
    from main import FolderShredWorker  # noqa: E402
except ModuleNotFoundError as exc:
    FolderShredWorker = None
    PYSIDE6_AVAILABLE = exc.name != "PySide6"
else:
    PYSIDE6_AVAILABLE = True


class ProtectedFileTypeTests(unittest.TestCase):
    def test_os_and_application_binary_types_are_protected(self):
        for extension in (".exe", ".dll", ".sys", ".drv", ".msi", ".efi"):
            with self.subTest(extension=extension):
                self.assertTrue(is_os_file_type(f"C:/Temp/sample{extension}"))

    def test_regular_user_file_types_are_not_marked_as_os_files(self):
        for extension in (".txt", ".jpg", ".pdf", ".zip"):
            with self.subTest(extension=extension):
                self.assertFalse(is_os_file_type(f"C:/Temp/sample{extension}"))

    @unittest.skipUnless(PYSIDE6_AVAILABLE, "PySide6 is required for FolderShredWorker")
    def test_folder_wiper_collects_files_in_subfolders_when_enabled(self):
        with tempfile.TemporaryDirectory() as folder:
            nested = Path(folder, "nested")
            nested.mkdir()
            top_file = Path(folder, "top.txt")
            nested_file = nested / "inside.txt"
            top_file.touch()
            nested_file.touch()

            worker = FolderShredWorker(folder, passes=1, include_subfolders=True)
            found = {Path(path) for path in worker._collect_files()}

            self.assertEqual(found, {top_file, nested_file})


if __name__ == "__main__":
    unittest.main()
