# test_filereader.py
import os                 # Importing os module (not used here but often for file operations)
import pytest             # Importing pytest for testing framework functionalities
from filereader import FileReader, LineStatsFileReader  # Import classes from your filereader module
import time               # Import time to add delay (used here for demonstration purposes)

def test_add_two_readers(tmp_path):
    # tmp_path is a pytest fixture that provides a temporary directory unique to the test run

    f1 = tmp_path / "f1.txt"  # Create a temporary file path for first file
    f2 = tmp_path / "f2.txt"  # Create a temporary file path for second file

    # Create a LineStatsFileReader instance from a string, saving to the temp file path f1
    reader1 = LineStatsFileReader.from_text(str(f1), "Hi there")

    # Similarly, create another LineStatsFileReader instance with different content
    reader2 = LineStatsFileReader.from_text(str(f2), "General Kenobi")

    # Use the overloaded + operator to merge the two readers into one
    merged = reader1 + reader2

    # Check that the merged object is still a LineStatsFileReader instance
    assert isinstance(merged, LineStatsFileReader)

    # Verify that the total number of lines (headers + content) in merged equals 4
    # Each reader adds 2 lines (probably a header + content line), so total is 4
    assert merged.line_count() == 4

    # Pause the test for 1 second (possibly for timing/debugging purposes)
    time.sleep(1)
