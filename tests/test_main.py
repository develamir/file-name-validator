import os
import tempfile
import unittest

from main import validate_filename, list_valid_files, format_results


class TestValidateFilename(unittest.TestCase):
    """Tests for validate_filename function."""

    def test_valid_text_file(self):
        self.assertTrue(validate_filename("report.txt", "^.*\\.txt$"))

    def test_valid_date_file(self):
        self.assertTrue(validate_filename("2026-11-05.pdf", "^\\d{4}-\\d{2}-\\d{2}\\.pdf$"))

    def test_invalid_no_extension(self):
        self.assertFalse(validate_filename("readme", "^.*\\.txt$"))

    def test_invalid_wrong_extension(self):
        self.assertFalse(validate_filename("data.csv", "^.*\\.txt$"))

    def test_empty_string(self):
        self.assertFalse(validate_filename("", "^\\d{4}-\\d{2}-\\d{2}$"))

    def test_valid_date_only(self):
        self.assertTrue(validate_filename("2026-11-05", "^\\d{4}-\\d{2}-\\d{2}$"))

    def test_partial_match_not_enough(self):
        self.assertFalse(validate_filename("2026-11-05extra.txt", "^\\d{4}-\\d{2}-\\d{2}\\.txt$"))

    def test_none_pattern_returns_false(self):
        self.assertFalse(validate_filename("test.txt", None))


class TestListValidFiles(unittest.TestCase):
    """Tests for list_valid_files function."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.directory = self.tmpdir.name
        # Create test files
        open(os.path.join(self.directory, "report.txt"), "w").close()
        open(os.path.join(self.directory, "notes.md"), "w").close()
        open(os.path.join(self.directory, "2026-11-05.pdf"), "w").close()
        open(os.path.join(self.directory, "invalid.dat"), "w").close()
        # Create a subdirectory to exclude
        subdir = os.path.join(self.directory, "subdir")
        os.mkdir(subdir)
        open(os.path.join(subdir, "should.txt"), "w").close()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_lists_matching_files(self):
        result = list_valid_files(self.directory, "^.*\\.txt$")
        self.assertEqual(sorted(result), ["report.txt"])

    def test_lists_multiple_matches(self):
        result = list_valid_files(self.directory, "^\\d{4}-\\d{2}-\\d{2}\\.pdf$")
        self.assertEqual(result, ["2026-11-05.pdf"])

    def test_excludes_directories(self):
        result = list_valid_files(self.directory, "^.*\\.txt$")
        self.assertNotIn("should.txt", result)

    def test_empty_directory(self):
        empty_dir = tempfile.TemporaryDirectory()
        result = list_valid_files(empty_dir.name, "^.*\\.txt$")
        self.assertEqual(result, [])
        empty_dir.cleanup()

    def test_nonexistent_directory(self):
        with self.assertRaises(FileNotFoundError):
            list_valid_files("/nonexistent/path/12345", "^.*\\.txt$")


class TestFormatResults(unittest.TestCase):
    """Tests for format_results function."""

    def test_all_valid(self):
        results = [("a.txt", True), ("b.txt", True)]
        output = format_results(results)
        self.assertEqual(output, "[OK] a.txt\n[OK] b.txt")

    def test_mixed_results(self):
        results = [("good.txt", True), ("bad.dat", False)]
        output = format_results(results)
        self.assertEqual(output, "[OK] good.txt\n[INVALID] bad.dat")

    def test_empty_results(self):
        output = format_results([])
        self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()
