"""Follow-up scheduler for Northbeam Outreach.

Pure functions only, no sending and no network calls.

Follow-up windows from the real system:
  - First follow-up: 4 to 5 business days after the hook
  - Second follow-up: 10 to 12 business days after the hook
After the second follow-up, stop. No third chase.

Business days are Monday to Friday. Weekends are skipped.
"""

import argparse
import sys
from datetime import date, timedelta


def add_business_days(start: date, days: int) -> date:
    """Return the date that is `days` business days after `start`.

    The start date itself does not count. Saturday and Sunday
    are skipped.
    """
    if days < 0:
        raise ValueError("days must be 0 or more")
    result = start
    added = 0
    while added < days:
        result = result + timedelta(days=1)
        if result.weekday() < 5:
            added += 1
    return result


def followup_dates(sent_date: date) -> dict:
    """Return the follow-up windows for a hook sent on sent_date.

    Returns a dict with four dates:
      first_early, first_late, second_early, second_late.
    """
    return {
        "first_early": add_business_days(sent_date, 4),
        "first_late": add_business_days(sent_date, 5),
        "second_early": add_business_days(sent_date, 10),
        "second_late": add_business_days(sent_date, 12),
    }


def parse_date(text: str) -> date:
    """Parse YYYY-MM-DD into a date, with a clear error on bad input."""
    try:
        year, month, day = (int(part) for part in text.split("-"))
        return date(year, month, day)
    except (ValueError, AttributeError):
        raise ValueError(f"Bad date {text!r}, use YYYY-MM-DD, e.g. 2026-11-23")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute Northbeam follow-up dates. No email is sent."
    )
    parser.add_argument("--date", default="",
                        help="Date the hook was sent, YYYY-MM-DD. Default: today.")
    args = parser.parse_args(argv)

    if args.date:
        sent = parse_date(args.date)
    else:
        sent = date.today()

    dates = followup_dates(sent)
    print(f"Hook sent: {sent} ({sent.strftime('%A')})")
    print("First follow-up window: "
          f"{dates['first_early']} to {dates['first_late']} "
          "(4 to 5 business days)")
    print("Second follow-up window: "
          f"{dates['second_early']} to {dates['second_late']} "
          "(10 to 12 business days)")
    print("After the second follow-up, stop. No third chase.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
