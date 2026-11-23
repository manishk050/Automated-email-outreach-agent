"""Draft a personalized outreach hook from templates/hook.txt.

Demo behaviour:
  python src/hook.py --business "Sample Salon" --city "Sample Town"

prints a draft hook to stdout and sends NOTHING.

Sending needs both an explicit --send flag and Gmail
credentials. See send.py. Without credentials, send.py
refuses and prints a clear message.
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "templates" / "hook.txt"


def load_template() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def render_hook(template: str, business_name: str, city: str,
                business_type: str = "") -> str:
    """Fill the hook template placeholders.

    Placeholders: {{business_name}}, {{city}}, {{business_type}}.
    """
    text = template.replace("{{business_name}}", business_name)
    text = text.replace("{{city}}", city)
    text = text.replace("{{business_type}}", business_type or "business")
    return text


def draft_hook(business_name: str, city: str, business_type: str = "") -> str:
    template = load_template()
    return render_hook(template, business_name, city, business_type)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Draft a Northbeam outreach hook. Sends nothing by default."
    )
    parser.add_argument("--business", required=True,
                        help='Business name, e.g. "Sample Salon"')
    parser.add_argument("--city", required=True,
                        help='City, e.g. "Sample Town"')
    parser.add_argument("--type", default="", dest="business_type",
                        help="Business type, e.g. salon, spa, dental clinic")
    parser.add_argument("--send", action="store_true",
                        help="Also attempt to send. Needs Gmail credentials, see send.py.")
    parser.add_argument("--to", default="",
                        help="Recipient email, only used with --send.")
    args = parser.parse_args(argv)

    hook = draft_hook(args.business, args.city, args.business_type)
    print("Demo hook, not sent unless --send is given with credentials.")
    print("---")
    print(hook)
    print("---")

    if not args.send:
        print("Nothing sent. This was a draft only.")
        return 0

    # Lazy import so a plain draft never needs the send module.
    from send import send_hook

    sent = send_hook(
        to=args.to,
        subject=f"Quick question about {args.business}",
        body=hook,
    )
    return 0 if sent else 1


if __name__ == "__main__":
    sys.exit(main())
