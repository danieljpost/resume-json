#!/usr/bin/env python3
"""Validate the canonical resume JSON.

Errors are things that are provably wrong: broken references, invalid enum
values, formatting drift, split files disagreeing with resume.json, UUIDs that
do not reproduce under the scheme in uuids.md.

Warnings are gaps against the gig-record spec in TODO.md: missing blurbs,
responsibilities that merely restate an accomplishment, records below the
volume targets for their engagement length.

Exit 1 on any error. Exit 1 on warnings too with --strict.

    ./validate.py [--strict] [--quiet]
"""

import json
import os
import sys
import uuid
from datetime import date

NS = uuid.UUID("2d21c062-ad99-5909-a8f9-ca62f3f2901c")  # uuid5(NS_DNS, danieljpost.pro)
INDENT = 2  # what bare `jq .` emits

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def canonical(data) -> str:
    """Byte-for-byte what `jq .` produces."""
    return json.dumps(data, indent=INDENT, ensure_ascii=False) + "\n"


def load_all() -> dict:
    """Parse every .json file. Formatting drift is an error, not a reformat."""
    out = {}
    for fn in sorted(f for f in os.listdir(".") if f.endswith(".json")):
        raw = open(fn, encoding="utf-8").read()
        try:
            data = json.loads(raw)
        except ValueError as e:
            err(f"{fn}: does not parse — {e}")
            continue
        if canonical(data) != raw:
            err(f"{fn}: not canonically formatted (run: jq . {fn} > t && mv t {fn})")
        if "\\u" in raw:
            err(f"{fn}: contains \\u escapes; this repo stores literal UTF-8")
        out[fn] = data
    return out


def section(data, key):
    """Split files are sometimes a bare array, sometimes {about, <key>: [...]}."""
    if isinstance(data, dict) and key in data:
        return data[key]
    return data


def months(start: str | None, end: str | None) -> int:
    if not start:
        return 0
    def parse(s):
        y, m, *_ = (s.split("-") + ["01"])
        return int(y) * 12 + int(m)
    today = date.today()
    fin = parse(end) if end else today.year * 12 + today.month
    return max(0, fin - parse(start))


# Volume targets from TODO.md, keyed by engagement class.
TARGETS = {
    "major":    {"responsibilities": 8, "accomplishments": 10, "technologies": 25},
    "standard": {"responsibilities": 4, "accomplishments": 5,  "technologies": 10},
    "short":    {"responsibilities": 1, "accomplishments": 2,  "technologies": 5},
}


def engagement_class(n_months: int) -> str:
    if n_months >= 6:
        return "major"
    if n_months >= 2:
        return "standard"
    return "short"


def check_ids(records, label, key, hard: bool) -> None:
    """UUIDv5 reproducibility per uuids.md, plus uniqueness.

    skills hold the rule exactly, so a mismatch there is an error. companies do
    not and cannot: uuids.md says company._id = uuid5(NS, url), but irishtitan
    is deliberately two records — contractor and recruiter — sharing one url,
    which the rule cannot express. Their ids are all valid v5 but derived from
    inputs that are not recorded anywhere, so this is reported as a single
    aggregate warning rather than one error per record.
    """
    seen = set()
    drift = []
    for r in records:
        rid = r.get("_id")
        if rid in seen:
            err(f"{label}: duplicate _id {rid!r}")
        seen.add(rid)
        src = r.get(key)
        if src is None:
            continue
        expect = str(uuid.uuid5(NS, src))
        if rid != expect:
            if hard:
                err(f"{label} {src!r}: _id is {rid}, but uuid5(NS, {key}) is {expect}")
            else:
                drift.append(src)
    if drift:
        warn(f"{label}: {len(drift)}/{len(records)} _id values do not reproduce as "
             f"uuid5(NS, {key}) as uuids.md specifies (all are valid v5, inputs unrecorded)")


def main() -> int:
    strict = "--strict" in sys.argv
    quiet = "--quiet" in sys.argv

    files = load_all()
    if "resume.json" not in files:
        err("resume.json missing")
        return report(strict, quiet)

    resume = files["resume.json"]
    gigs = section(files.get("gigs.json", []), "gigs")
    skills = section(files.get("skills.json", []), "skills")
    companies = section(files.get("companies.json", []), "companies")
    recs = section(files.get("recommendations.json", []), "recommendations")
    tiers = set(section(files.get("tiers.json", {}), "tiers"))
    gig_types = set(section(files.get("gigTypes.json", {}), "gigTypes"))
    categories = set(section(files.get("skillCategories.json", {}), "skillCategories"))

    # --- split files must agree with the monolith -------------------------
    for fn, key in (("gigs.json", "gigs"), ("skills.json", "skills"),
                    ("companies.json", "companies"),
                    ("recommendations.json", "recommendations"),
                    ("tiers.json", "tiers"), ("gigTypes.json", "gigTypes"),
                    ("skillCategories.json", "skillCategories"), ("me.json", "me")):
        if fn in files and key in resume:
            if section(files[fn], key) != resume[key]:
                err(f"{fn} disagrees with resume.json[{key!r}]")

    # --- identity ---------------------------------------------------------
    check_ids(skills, "skills.json", "sname", hard=True)
    check_ids(companies, "companies.json", "url", hard=False)

    dup_urls = {}
    for c in companies:
        dup_urls.setdefault(c.get("url"), []).append(c.get("name"))
    for url, names in dup_urls.items():
        if len(names) > 1:
            warn(f"companies.json: {len(names)} records share url {url!r} ({', '.join(names)})")

    snames = {s.get("sname") for s in skills}
    company_ids = {c.get("_id") for c in companies}
    gig_ids = {g.get("_id") for g in gigs}

    for s in skills:
        if s.get("category") not in categories:
            err(f"skill {s.get('sname')!r}: unknown category {s.get('category')!r}")
        for t in s.get("tiers") or []:
            if t not in tiers:
                err(f"skill {s.get('sname')!r}: unknown tier {t!r}")

    for r in recs:
        if r.get("gigId") not in gig_ids:
            err(f"recommendation {r.get('name')!r}: unknown gigId {r.get('gigId')!r}")
        if r.get("company") not in company_ids:
            err(f"recommendation {r.get('name')!r}: unknown company {r.get('company')!r}")

    # --- gigs -------------------------------------------------------------
    blurb_text: dict[str, list[str]] = {}

    for g in gigs:
        gid = g.get("_id", "<no id>")
        gt = g.get("tiers") or []

        if not gt:
            err(f"gig {gid}: declares no tiers")
        for t in gt:
            if t not in tiers:
                err(f"gig {gid}: unknown tier {t!r}")

        if g.get("gigType") not in gig_types:
            err(f"gig {gid}: unknown gigType {g.get('gigType')!r}")

        for field in ("companyId", "contractorId"):
            v = g.get(field)
            if v is not None and v not in company_ids:
                err(f"gig {gid}: {field} {v!r} resolves to no company")

        for t in g.get("technologies") or []:
            name = t.get("skillName")
            if name not in snames:
                err(f"gig {gid}: technology {name!r} is not a skill in skills.json")
            rel = t.get("relevance")
            if not isinstance(rel, int) or not 1 <= rel <= 10:
                err(f"gig {gid}: technology {name!r} relevance {rel!r} outside 1-10")

        # blurbs: object keyed by tier, one per declared tier
        b = g.get("blurbs")
        if b is None:
            warn(f"gig {gid}: no blurbs, but declares {len(gt)} tier(s)")
        elif not isinstance(b, dict):
            err(f"gig {gid}: blurbs is {type(b).__name__}, must be an object keyed by tier")
        else:
            for k, v in b.items():
                if k not in tiers:
                    err(f"gig {gid}: blurb key {k!r} is not a tier")
                elif k not in gt:
                    err(f"gig {gid}: blurb key {k!r} is not declared in the gig's tiers")
                if not str(v).strip():
                    err(f"gig {gid}: blurb {k!r} is empty")
                else:
                    blurb_text.setdefault(str(v).strip(), []).append(f"{gid}[{k}]")
            missing = [t for t in gt if t not in b]
            if missing:
                warn(f"gig {gid}: {len(b)}/{len(gt)} blurbs, missing {', '.join(missing)}")

        # responsibilities restating accomplishments
        resp = [str(x).strip().lower().rstrip(".") for x in g.get("responsibilities") or []]
        acc = [str(x).strip().lower().rstrip(".") for x in g.get("accomplishments") or []]
        for r in set(resp) & set(acc):
            warn(f"gig {gid}: a responsibility duplicates an accomplishment verbatim — {r[:60]!r}")

        # volume
        cls = engagement_class(months(g.get("startDate"), g.get("endDate")))
        for field, floor in TARGETS[cls].items():
            have = len(g.get(field) or [])
            if have < floor:
                warn(f"gig {gid}: {field} {have} < {floor} ({cls} engagement)")

    for text, where in blurb_text.items():
        if len(where) > 1:
            warn(f"identical blurb text reused by {', '.join(where)} — {text[:60]!r}")

    return report(strict, quiet)


def report(strict: bool, quiet: bool) -> int:
    if errors:
        print(f"ERRORS ({len(errors)})")
        for e in errors:
            print(f"  {e}")
    if warnings and not quiet:
        if errors:
            print()
        print(f"WARNINGS ({len(warnings)})")
        for w in warnings:
            print(f"  {w}")
    if not errors and not warnings:
        print("clean")
    elif not errors:
        print(f"\nno errors; {len(warnings)} warning(s)")
    return 1 if errors or (strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
