
# test_filereader.py
import os
import pytest
from filereader import FileReader, LineStatsFileReader
import time

def test_add_two_readers(tmp_path):
    f1 = tmp_path / "f1.txt"
    f2 = tmp_path / "f2.txt"
    reader1 = LineStatsFileReader.from_text(str(f1), "Hi there")
    reader2 = LineStatsFileReader.from_text(str(f2), "General Kenobi")
    merged = reader1 + reader2
    assert isinstance(merged, LineStatsFileReader)
    assert merged.line_count() == 4  # 2 header lines + 2 content lines
    time.sleep(1)


