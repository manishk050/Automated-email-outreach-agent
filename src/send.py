"""Send an outreach hook by Gmail.

Demo pack rule: this module NEVER sends without credentials.
Credentials come from the environment, never from a file
committed to the repo. See .env.example for placeholder names.

In this demo pack there are no real credentials, so send_hook
always refuses and prints a clear message. That is the intended
behaviour here. Wire your own Gmail API client in send_real()
when you run this for real, and keep tokens out of git.
"""

import os
import sys
from pathlib import Path

# Daily batch cap from the real system. Up to 100 hooks in one day.
DAILY_BATCH_CAP = 100


def has_credentials() -> bool:
    """Check for Gmail credentials in the environment.

    Expected placeholder names are in .env.example.
    A real setup would check for a Gmail API token or
    OAuth credentials file pointed to by an env var.
    """
    token_path = os.environ.get("GMAIL_TOKEN_PATH", "")
    client_id = os.environ.get("GMAIL_CLIENT_ID", "")
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET", "")
    if token_path and Path(token_path).exists():
        return True
    if client_id and client_secret:
        return True
    return False


def send_hook(to: str, subject: str, body: str) -> bool:
    """Attempt to send one hook. Refuses without credentials.

    Returns True only if a real send happened. In this demo
    pack it always returns False, because no credentials
    are present by design.
    """
    if not to:
        print("Not sent: no recipient email was given. Use --to with --send.")
        return False
    if not has_credentials():
        print("Not sent: no Gmail credentials found.")
        print("Set GMAIL_TOKEN_PATH or GMAIL_CLIENT_ID and "
              "GMAIL_CLIENT_SECRET in your environment, see .env.example.")
        print("Nothing was sent. This demo pack never sends without credentials.")
        return False
    # Credentials present. The real Gmail send lives here in
    # a production copy. This demo pack still refuses, because
    # no real Gmail client is bundled, to avoid accidental sends.
    print("Credentials found, but this demo pack has no Gmail client bundled.")
    print("Not sent. Wire send_real() with your own Gmail API client to send for real.")
    return False


def send_real(to: str, subject: str, body: str):
    """Placeholder for a real Gmail API send.

    Not implemented in the demo pack on purpose. Implement it
    in your own copy with the Gmail API, respect DAILY_BATCH_CAP,
    and log every send through tracker.py.
    """
    raise NotImplementedError(
        "send_real is not implemented in the demo pack. "
        "Add your own Gmail API client in your own copy."
    )


if __name__ == "__main__":
    print("send.py demo check.")
    print(f"Daily batch cap: {DAILY_BATCH_CAP}")
    print(f"Credentials present: {has_credentials()}")
    if not has_credentials():
        print("Result: nothing would be sent. No Gmail credentials found.")
        sys.exit(0)
    print("Result: credentials found, but demo pack still sends nothing.")
    sys.exit(0)
