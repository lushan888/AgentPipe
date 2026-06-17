"""Entry point so the workflow can run ``python -m oracle``."""

import sys

from .improve import main

if __name__ == "__main__":
    sys.exit(main())
