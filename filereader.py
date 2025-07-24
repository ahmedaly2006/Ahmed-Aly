# -------
# PART 1#
# -------
# filereader.py

# Imports
import os  # For file and system operations
from typing import Generator, List  # For better type hinting and code clarity
from functools import wraps  # To preserve function metadata in decorators
import pyttsx3  # Text-to-speech engine

# Constants
"allows colored text to be appeared"
ANSI_COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "reset": "\033[0m",
}


# --------------------------
# Decorators
# --------------------------
def color_output(color: str):
    """
    Decorator to print the output of a function in a specified ANSI color.
    """

    def decorator(func):
        @wraps(func)  # Preserves the original function’s name, docstring, etc.
        def wrapper(*args, **kwargs):
            print(ANSI_COLORS.get(color, ""), end="")  # start color
            result = func(*args, **kwargs)
            print(ANSI_COLORS["reset"], end="")  # reset to default
            return result

        return wrapper

    return decorator


# -------
# PART 2#
# -------


# --------------------------
# Base File Reader /the first class
# --------------------------
class FileReader:
    """
    Base class to read and write text files.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def read_lines(self) -> Generator[str, None, None]:
        """
        Yield lines from the file without newline characters.
        """
        if not os.path.exists(self.filepath):
            print(f"File not found: {self.filepath}")
            return iter([])
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                yield line.rstrip("\n")  # yeild zay return bas t3eed nafsaha

    # the @ methods
    @property  # --->decorator in Python is used to define a method that can be accessed like an attribute
    def lines(self) -> List[str]:
        """
        Return all lines as a list.
        """
        return list(self.read_lines())

    @lines.setter  # ---->allows us to control how an attribute is changed
    def lines(self, new_lines: List[str]):
        """
        Overwrite the file with the provided list of lines.
        """
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(line.rstrip("\n") for line in new_lines) + "\n")

    @staticmethod  # imp #---> #It behaves just like a plain function, but is logically grouped inside a class.
    def file_exists(path: str) -> bool:
        """
        Check if a file exists at the given path.
        """
        return os.path.exists(path)

    @classmethod  # You want to create alternate constructors.
    def from_text(cls, path: str, content: str):
        """
        Create a new file with given content and return a FileReader instance.
        """
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return cls(path)

    def __str__(self):
        return f"FileReader(filepath='{self.filepath}')"

    def __add__(self, other):
        """
        Merge two FileReader instances by concatenating their lines into a new file.
        """
        if not isinstance(other, FileReader):
            raise ValueError("Can only add another FileReader")
        new_path = "merged.txt"
        with open(new_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines + other.lines))
        return FileReader(new_path)

    def concat_files(self, *others, output_name="concat_all.txt"):
        """
        Concatenate multiple FileReader files into one output file.
        """
        all_lines = self.lines[:]
        for other in others:
            if not isinstance(other, FileReader):
                raise TypeError("All arguments must be FileReader instances")
            all_lines.extend(other.lines)
        with open(output_name, "w", encoding="utf-8") as f:
            f.write("\n".join(all_lines))
        return FileReader(output_name)

    @color_output("blue")
    def display(self):
        """
        Print the content of the file in blue.
        """
        for line in self.read_lines():
            print(line)


# -------
# PART 3#/2nd class
# -------
# --------------------------
# Extended Stats Reader
# --------------------------
class LineStatsFileReader(FileReader):
    """
    Extension of FileReader that provides line and word counts.
    """

    def line_count(self) -> int:
        """
        Return the number of lines in the file.
        """
        return len(self.lines)

    def word_count(self) -> int:
        """
        Return the total number of words in the file.
        """
        return sum(len(line.split()) for line in self.lines)

    def __str__(self):
        return (
            f"LineStatsFileReader(filepath='{self.filepath}', "
            f"lines={self.line_count()}, words={self.word_count()})"
        )

    def __add__(self, other):
        """
        Merge two LineStatsFileReader instances with a header describing the merge.
        """
        if not isinstance(other, FileReader):
            raise ValueError("Can only add another FileReader")
        new_path = "merged_with_stats.txt"
        header = f"# Merged by LineStatsFileReader\n# Files: {self.filepath}, {other.filepath}\n"
        with open(new_path, "w", encoding="utf-8") as f:
            f.write(header + "\n".join(self.lines + other.lines))
        return LineStatsFileReader(new_path)


# --------------------------
# Text-to-Speech Reader
# --------------------------
class SpeakingFileReader(FileReader):
    """
    FileReader subclass that reads the content aloud using text-to-speech.
    """

    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.engine = pyttsx3.init()

    def speak(self, text: str):
        """
        Use text-to-speech to speak the given text.
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def display_and_speak(self):
        """
        Print and speak the file contents line-by-line.
        """
        for line in self.read_lines():
            print(line)
            self.speak(line)


# --------------------------
# Command-line Interface (CLI) Menu
# part 5
# --------------------------
def main_menu():
    """
    Display the main menu and handle user commands.
    """
    readers = {}

    while True:
        print("\n--- File Reader Menu ---")
        print("1. Create new file")
        print("2. Display file")
        print("3. Show line and word count")
        print("4. Merge two files")
        print("5. Display & Speak file")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            name = input("Give a name to this file reader: ").strip()  # FIXED HERE
            filename = input("Enter file name to create: ").strip()
            content = input("Enter file content (use \\n for new lines): ").replace(
                "\\n", "\n"
            )
            reader = LineStatsFileReader.from_text(filename, content)
            readers[name] = reader
            print(f"File '{filename}' created and stored as '{name}'.")

        elif choice == "2":
            name = input("Enter file reader name to display: ").strip()
            reader = readers.get(name)
            if reader:
                reader.display()
            else:
                print("File not found in memory.")

        elif choice == "3":
            name = input("Enter file reader name for stats: ").strip()
            reader = readers.get(name)
            if isinstance(reader, LineStatsFileReader):
                print(f"Lines: {reader.line_count()} | Words: {reader.word_count()}")
            else:
                print("This file doesn't support statistics.")

        elif choice == "4":
            name1 = input("Enter first file reader name: ").strip()
            name2 = input("Enter second file reader name: ").strip()
            output_name = input("Name for merged result: ").strip()
            r1 = readers.get(name1)
            r2 = readers.get(name2)
            if r1 and r2:
                merged = r1 + r2
                readers[output_name] = merged
                print(
                    f"Files merged into '{merged.filepath}' and saved as '{output_name}'."
                )
            else:
                print("One or both file readers not found.")

        elif choice == "5":
            name = input("Enter file reader name to display and speak: ").strip()
            reader = readers.get(name)
            if reader:
                if not isinstance(reader, SpeakingFileReader):
                    reader = SpeakingFileReader(reader.filepath)
                reader.display_and_speak()
            else:
                print("File not found in memory.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid input. Please choose a number between 1 and 6.")


# --------------------------
# Main Entry Point
# --------------------------
if __name__ == "__main__":
    main_menu()

# we should use black haga aashan ne test our score of the code this is cicd thing related to github docstrings
