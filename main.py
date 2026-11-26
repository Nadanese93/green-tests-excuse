#!/usr/bin/env python3
"""Write the one-liner entry for the Green Tests, Nothing Works excuse contest.

Stdlib only, deterministic, no network. Writes the exact entry text
(110 chars, no trailing newline) as UTF-8 bytes to
$MAKEFUN_OUTPUT_DIR/entry.txt, then reads it back and verifies it.
"""

import hashlib
import os
import sys

ENTRY = (
    "At standup I said the tests are green. "
    "Nobody asked whether the app does anything, "
    "and I did not volunteer it."
)

EXPECTED_SHA256 = "1c290551f67eac92ab00a1bef287521cdc28bdf3096c38b8c298f8d0c3450eb8"


def verify(path):
    """Read entry.txt back and fail loudly if it is not exactly the entry.

    Checks: valid UTF-8, 1-140 chars, no trailing newline, no control
    characters, and sha256 matches the expected constant.
    Returns 0 on success, 1 on any mismatch.
    """
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError as exc:
        print(f"verify: cannot read {path}: {exc}", file=sys.stderr)
        return 1
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"verify: not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 140:
        print(f"verify: length {len(text)} outside 1-140", file=sys.stderr)
        return 1
    if text.endswith("\n"):
        print("verify: trailing newline present", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 for ch in text):
        print("verify: control character present", file=sys.stderr)
        return 1
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        print(
            f"verify: sha256 mismatch: got {digest}, "
            f"expected {EXPECTED_SHA256}",
            file=sys.stderr,
        )
        return 1
    return 0


def main():
    out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    if verify(path) != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
