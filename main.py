from __future__ import annotations

import sys

from shakar_desktop.bootstrap import run


if __name__ == "__main__":
    try:
        raise SystemExit(run())
    except ImportError as exc:
        missing = getattr(exc, "name", None) or str(exc)
        print(
            "Shakar desktop dependencies are missing. Install them with: "
            "python -m pip install -r requirements-desktop.txt",
            file=sys.stderr,
        )
        print(f"Missing module: {missing}", file=sys.stderr)
        raise
