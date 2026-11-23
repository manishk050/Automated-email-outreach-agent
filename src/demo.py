"""Build a concept demo site, only after a positive reply.

Bare-yes rule: a bare "yes" does NOT trigger a demo.
A demo is built only when the prospect has shown real intent,
which means at least one of these is true:
  - they booked a call (--booked-call), or
  - they replied with services, prices, and photos (--provided-details)

Without one of those flags, demo.py refuses and builds nothing.
This rule exists because a bare yes costs nothing, so it
produced demos that went nowhere.

The demo is built from templates/demo/index.html, a generic
template with no real business branding.
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "templates" / "demo" / "index.html"


def has_real_intent(booked_call: bool, provided_details: bool) -> bool:
    """True only if the prospect booked a call or sent details."""
    return bool(booked_call or provided_details)


def build_demo(business_name: str, city: str, business_type: str = "",
               booked_call: bool = False, provided_details: bool = False,
               output_dir: str = "") -> Path:
    """Build the demo site, or raise ValueError if intent is missing.

    Returns the path to the built index.html.
    """
    if not has_real_intent(booked_call, provided_details):
        raise ValueError(
            "a bare yes is not enough. "
            "The prospect must book a call or reply with services, "
            "prices, and photos before a demo is built."
        )
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    html = template.replace("{{business_name}}", business_name)
    html = html.replace("{{city}}", city)
    html = html.replace("{{business_type}}", business_type or "business")

    out_dir = Path(output_dir) if output_dir else REPO_ROOT / "out" / "demo"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a concept demo site, only after a positive reply with real intent."
    )
    parser.add_argument("--business", required=True,
                        help='Business name, e.g. "Sample Salon"')
    parser.add_argument("--city", required=True,
                        help='City, e.g. "Sample Town"')
    parser.add_argument("--type", default="", dest="business_type",
                        help="Business type, e.g. salon, spa, dental clinic")
    parser.add_argument("--booked-call", action="store_true",
                        help="Prospect booked a call.")
    parser.add_argument("--provided-details", action="store_true",
                        help="Prospect replied with services, prices, and photos.")
    parser.add_argument("--out", default="",
                        help="Output directory for the demo site. Default: out/demo")
    args = parser.parse_args(argv)

    try:
        out_path = build_demo(
            business_name=args.business,
            city=args.city,
            business_type=args.business_type,
            booked_call=args.booked_call,
            provided_details=args.provided_details,
            output_dir=args.out,
        )
    except ValueError as exc:
        print(f"No demo built: {exc}")
        return 1

    print(f"Demo built: {out_path}")
    print("This is a concept demo from the generic template.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
