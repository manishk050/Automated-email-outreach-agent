"""Prospect research for Northbeam Outreach.

Demo code only. All data here is fake sample data.
No real prospect names, emails, or addresses are used.

A prospect is a business with no website. Tier-1 regions
(US, UK, CA, AU) are preferred, but the check works worldwide.
"""

from dataclasses import dataclass


@dataclass
class Prospect:
    business_name: str
    city: str
    region: str = ""
    business_type: str = ""
    has_website: bool = False
    contact_email: str = ""


# Fake sample prospects, for demo and tests only.
SAMPLE_PROSPECTS = [
    Prospect(
        business_name="Sample Salon",
        city="Sample Town",
        region="UK",
        business_type="salon",
        has_website=False,
    ),
    Prospect(
        business_name="Sample Spa",
        city="Sample Town",
        region="UK",
        business_type="spa",
        has_website=False,
    ),
    Prospect(
        business_name="Sample Dental Clinic",
        city="Sample Town",
        region="UK",
        business_type="dental clinic",
        has_website=False,
    ),
]


def has_website(prospect: Prospect) -> bool:
    """Return True if the prospect already has a website.

    In the real system this checks search results and directories.
    In this demo pack it returns the stored flag, so no network
    call and no real business is looked up.
    """
    return prospect.has_website


def needs_website(prospect: Prospect) -> bool:
    """A prospect qualifies for outreach only if it has no website."""
    return not has_website(prospect)


def research_prospect(business_name: str, city: str,
                      business_type: str = "", region: str = "") -> Prospect:
    """Build a Prospect record from fake demo inputs.

    No network call is made here. Real research (search, maps,
    directory checks) lives outside this demo pack and needs
    the operator's own API keys.
    """
    prospect = Prospect(
        business_name=business_name.strip(),
        city=city.strip(),
        region=region.strip(),
        business_type=business_type.strip(),
        has_website=False,
    )
    return prospect


def sample_prospects():
    """Return the fake sample prospect list."""
    return list(SAMPLE_PROSPECTS)


if __name__ == "__main__":
    for prospect in sample_prospects():
        status = "has a website" if prospect.has_website else "no website"
        print(f"{prospect.business_name}, {prospect.city}: {status}")
        print(f"  Qualifies for outreach: {needs_website(prospect)}")
