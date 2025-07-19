# AI-Dump: Codebase Flattener for LLM Analysis

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A command-line utility to intelligently flatten a project's directory structure by copying specific file types, handling naming conflicts, and generating a map of the original structure. Ideal for preparing codebases for analysis by Large Language Models (LLMs).

## Overview

When working with Large Language Models, it's often necessary to provide a large amount of context, such as the entire codebase of a project. However, many models work best with a flat list of files rather than a complex, nested directory structure.

**AI-Dump** simplifies this process. It traverses a project directory, finds all relevant source files (like `.py`, `.js`, `.html`, etc.), and copies them to a single, flat folder. To avoid conflicts where multiple files share the same name (e.g., `__init__.py`), it automatically renames duplicates sequentially.

Crucially, it also generates a `tree.txt` file that preserves a visual map of the original folder hierarchy, so you never lose the architectural context of your code.

## Features

-   **Smart File Discovery**: Recursively finds and copies files with specified extensions (default: `.py`, `.html`, `.css`, `.js`).
-   **Directory Flattening**: Consolidates all found files into a single output directory.
-   **Automatic De-confliction**: Intelligently handles duplicate filenames by appending a numerical suffix (e.g., `utils.py` becomes `utils_2.py`).
-   **Preserves Original Structure**: Generates an easy-to-read `tree.txt` file that maps out the original location of all copied files.
-   **Zero Dependencies**: Runs with standard Python libraries, no `pip install` required.
-   **CLI Interface**: Simple and straightforward to run from the command line.

## Requirements

-   Python 3.6 or higher.
-   No external libraries needed.

## Installation

1.  Clone the repository or download the `ai_dump.py` script.
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
2.  That's it! The script is ready to run.

## Usage

Run the script from your terminal, passing the path to the project folder you want to process as the only argument.

### Syntax

```sh
python ai_dump.py /path/to/your/project
```

### Contributing
Contributions are welcome! If you have an idea for an improvement or have found a bug, please feel free to open an issue or submit a pull request.

### License
This project is licensed under the MIT License.