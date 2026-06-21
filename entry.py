"""Frozen-build entry point.

PyInstaller runs its entry script as the top-level ``__main__`` module with no
package context, which breaks the relative imports inside ``pacebar``.
This launcher uses an absolute import so the package loads normally.
"""

import sys

from pacebar.__main__ import main

if __name__ == "__main__":
    sys.exit(main())
