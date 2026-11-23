# Architecture - Northbeam Outreach

## Pipeline

```
Prospecting -> Hook -> Send -> Reply tracking -> Follow-up -> Demo (only on intent) -> Delivery
     |           |        |           |              |                |                  |
 prospect.py  hook.py  send.py   tracker.py    followup.py       demo.py          tracker.py
```

## Stage 1: Hook

1. `prospect.py` finds businesses with no website. Tier-1 regions (US, UK, CA, AU) are preferred, but the check works worldwide.
2. `hook.py` renders `templates/hook.txt` with `{{business_name}}`, `{{city}}`, and `{{business_type}}`.
3. `send.py` sends the hook by Gmail, with a daily batch cap of 100. No attachment, no demo link, no deceptive subject line.
4. `tracker.py` logs the send in a local JSON file: hooks sent, replies, demos built.

## Stage 2: Demo, only on interest

1. A reply is tracked in `tracker.py`.
2. `followup.py` computes the follow-up windows if there is no reply: first follow-up at 4 to 5 business days, second at 10 to 12 business days. After the second follow-up, stop.
3. `demo.py` builds a concept demo from `templates/demo/index.html` only after real intent is shown.
4. The demo is sent with pricing (from $399, 50% deposit and 50% on delivery), delivery in 2-4 days, unlimited revisions, and a $49/month care plan.

## The bare-yes rule

A bare "yes" does NOT trigger a demo.

A demo is built only when the prospect has shown real intent, which means at least one of these is true:

- they booked a call, or
- they replied with services, prices, and photos.

This rule came from a real leak: a bare yes costs nothing, so it produced demos that went nowhere. `demo.py` enforces it. Without `--booked-call` or `--provided-details`, it refuses and builds nothing.

## Real numbers, for docs only

These are the live system results, already in the README. Do not invent new metrics.

- 637 hooks sent
- 2 positive replies
- 5 demo sites built
- Up to 100 hooks sent in one day

Demo output in this repo uses fake sample data only, and says it is a demo.

## What is not in this repo

- Real prospect lists, email addresses, or sent-mail history
- Real client demo sites with business names, photos, or addresses
- Gmail OAuth tokens, API keys, or `.env` files
- Pricing negotiation history

## Files

- `src/prospect.py`: prospect research, no-website check, fake samples only
- `src/hook.py`: hook drafting from `templates/hook.txt`
- `src/send.py`: Gmail send, refuses without credentials, daily cap 100
- `src/followup.py`: 4 to 5 and 10 to 12 business day follow-up dates, pure functions
- `src/demo.py`: concept demo generator, gated by the bare-yes rule
- `src/tracker.py`: local JSON tracker, counts only
