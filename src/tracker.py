"""Local JSON tracker for Northbeam Outreach.

Counts only, no personal data. The tracker file lives in
data/tracker.json under the repo root in a real run, and it
is gitignored. This demo pack ships demo counts only.

Real numbers from the live system, for docs only:
  637 hooks sent, 2 positive replies, 5 demo sites built,
  up to 100 hooks sent in one day.
Demo data below is fake and clearly labelled as demo.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "data" / "tracker.json"

# Fake demo counts. These are not real results.
DEMO_DATA = {
    "demo": True,
    "hooks_sent": 3,
    "replies": 1,
    "positive_replies": 1,
    "demos_built": 1,
    "followups_sent": 0,
    "notes": "Demo data only. Fake sample counts, not real results.",
}


def empty_tracker() -> dict:
    return {
        "demo": False,
        "hooks_sent": 0,
        "replies": 0,
        "positive_replies": 0,
        "demos_built": 0,
        "followups_sent": 0,
        "prospects": [],
    }


def load_tracker(path: Path = DEFAULT_PATH) -> dict:
    if not path.exists():
        return empty_tracker()
    return json.loads(path.read_text(encoding="utf-8"))


def save_tracker(data: dict, path: Path = DEFAULT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def record_hook(data: dict, business_name: str) -> dict:
    data["hooks_sent"] = data.get("hooks_sent", 0) + 1
    data.setdefault("prospects", []).append(
        {"business_name": business_name, "stage": "hook_sent"}
    )
    return data


def record_reply(data: dict, business_name: str, positive: bool = False) -> dict:
    data["replies"] = data.get("replies", 0) + 1
    if positive:
        data["positive_replies"] = data.get("positive_replies", 0) + 1
    return data


def record_demo(data: dict, business_name: str) -> dict:
    data["demos_built"] = data.get("demos_built", 0) + 1
    return data


def summary(data: dict) -> str:
    reply_rate = 0.0
    if data.get("hooks_sent"):
        reply_rate = 100.0 * data.get("positive_replies", 0) / data["hooks_sent"]
    return (
        f"Hooks sent: {data.get('hooks_sent', 0)}\n"
        f"Replies: {data.get('replies', 0)}\n"
        f"Positive replies: {data.get('positive_replies', 0)}\n"
        f"Demos built: {data.get('demos_built', 0)}\n"
        f"Follow-ups sent: {data.get('followups_sent', 0)}\n"
        f"Positive reply rate: {reply_rate:.1f}%"
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Show or reset the local Northbeam tracker. Demo data only."
    )
    parser.add_argument("--demo", action="store_true",
                        help="Print the fake demo counts.")
    parser.add_argument("--show", action="store_true",
                        help="Show the local tracker file, or empty counts if none.")
    parser.add_argument("--reset", action="store_true",
                        help="Reset the local tracker file to empty counts.")
    args = parser.parse_args(argv)

    if args.demo:
        print("Demo tracker, fake sample counts only.")
        print(summary(DEMO_DATA))
        return 0
    if args.reset:
        save_tracker(empty_tracker())
        print(f"Tracker reset: {DEFAULT_PATH}")
        return 0
    # Default: show.
    data = load_tracker()
    print(summary(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
