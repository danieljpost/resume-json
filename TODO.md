### Stuff currently not done, but should be done

1) [X] Split Gigs out into gigs.json
1) [X] Split Companies out into companies.json
1) [X] Split Skills out into skills.json
1) [ ] and so forth — `versions` and `intros` still have no split file
1) [ ] When I want to update those sections, update the small file, commit the changes, then update the main resume.json file — not yet the actual practice; as of 2026-08-12 the split files were regenerated *from* resume.json
1) [ ] locate who recruited me for each of the last like 15 years worth of gigs, link them in LinkedIn
1) [ ] write a script or 7 to reduce the canonicals .json file into standard formats like https://jsonresume.org/schema, based on query e.g. jobtype=devops & verbosity=2. Probably just fucking brute-force the generation as a CI/CD step
1) [ ] publish schemas at https://eatthebillionaires.pro/schema/resume.schema.json et al.
1) [X] use like https://schema.org/Person — `me` carries @context=https://schema.org, @type=Person, see=https://schema.org/Person. Note only 2 of 33 companies carry see=https://schema.org/Organization, so the Organization side is barely started
1) [ ] use https://jsonresume.org/schema
1) [ ] push those things into mongodb for maintenance
1) [ ] write an API using express or Rust or whatever to serve those files as if they weren't just static data
1) [ ] find a good tool to serve those out also as an API with like GraphQL
1) [ ] find a new url shortener; danieljpost.net is moot
1) [ ] offer Career Profile and Career Highlights, per the attached PDF example, as the first element of resume - point being that the recruiter is only going to read page 1 anyway. Only robots look for the list of "relevant" skills which should be at the bottom of the exported page
1) [ ] write up a list of things I intend to learn and start learning them!
1) [ ] create a quick bash script to concatenate all .json files into $timestamp.resume.json then open that file in code for formatting and testing.
1) [ ] Recommendations should be instance of https://schema.org/Recommendation
1) [X] flesh out Target role — done 2026-08-18 in 5452eca: 6 responsibilities, 8 accomplishments, 11 technologies, and a blurb for all 10 declared tiers. Project Slingshot was a Jira-backed CMS for Target.com; the ZF2/PHP interface layer abstracted JQL behind a query builder and repository layer so content staff never wrote a Jira query. See the gig-record spec below for the shape the rest of the gigs should follow

### What every gig record should contain

Derived 2026-08-18 from the records that already work — `8e91e4c7…` (Lead DevOps &
Full-Stack), `267c4d1c…` (ThreatLVL), and `target`. Everything else in gigs.json is
below this line.

**`responsibilities` — the mandate.** What I was engaged to own, stated as scope. No
metrics, no outcomes. Answers "what was the job."

> Led the full Firebase-to-PostgreSQL database migration using Drizzle ORM with
> TypeScript-strict schema definitions

**`accomplishments` — the evidence.** The same work carrying magnitude, result, or
consequence. Answers "what came of it."

> Led a complete Firebase-to-PostgreSQL migration: 25-table schema, 115-file repository
> abstraction layer, UUIDv7 primary keys — …

The discriminator is **numbers and outcomes**. No number and no outcome means it is a
responsibility, not an accomplishment. If a responsibility and an accomplishment read
the same, one of them has not been written yet — that was exactly the defect in `target`
before 2026-08-18, where the lone responsibility duplicated accomplishments[0] verbatim.

**`technologies` — the skill index.** `{skillName, relevance}` where relevance is 1–10
*for that gig*, not career-wide. In practice the scale runs 2–10 with 10 as the mode:
10 = the gig was built in it, 8–9 = daily, 5–7 = substantial, 2–4 = touched lightly.
`skillName` must resolve to an `sname` in skills.json.

**`blurbs` — the same gig retold per role.** A `{tier: prose}` object, one entry per
declared tier, each retelling the engagement from that role's angle so a reader who
selected "DevOps" gets the DevOps story. Denser than an accomplishment; the good ones
run 300–600 characters. The only narrative field.

#### Volume, scaled to the engagement

| Engagement | resp | acc | tech | blurbs |
|---|---|---|---|---|
| Major (6+ months, or career-defining) | 8–12 | 10–15 | 25–40 | one per tier |
| Standard (2–6 months) | 4–6 | 5–8 | 10–20 | one per tier |
| Short (≤1 month) | 1–3 | 2–4 | 5–10 | one per tier |

`blurbs` does not scale — its count is fixed by `tiers`, because a tier with no blurb
renders empty for anyone who selected that role.

#### Invariants

1. Every `technologies[].skillName` resolves in skills.json. **Clean as of 2026-08-18.**
2. `set(blurbs) ⊆ set(tiers)`. **Clean as of 2026-08-18.**
3. Every gig declares at least one tier. **Violated** by ezXchanges, starkey,
   fedexPkgHandler, fedexPkgHandler2.

Goal state promotes #2 to equality: `set(blurbs) == set(tiers)`.

#### Where this stands (2026-08-18)

4 of 28 gigs meet the spec (2026-08-18: validator reports 6 errors, 107 warnings).

1) [ ] blurbs are the big gap: 21 gigs have no `blurbs` key at all
1) [ ] 3 gigs carry exactly 1 blurb against 5–9 declared tiers: danieljpost.pro (1/9),
   btg (1/6), acf4ddf5… (1/5). danieljpost.pro and btg hold the *identical*
   "Software Engineering is an Art…" boilerplate — philosophy, not a gig blurb — and
   acf4ddf5…'s is the empty string. lacek was the fourth; fixed 2026-08-18 in 672d06c,
   and it now clears the validator outright
1) [ ] 14 gigs have exactly 1 responsibility, most paired with 1–2 accomplishments —
   the thin-record pattern target had
1) [ ] starkey has 0 responsibilities; fedexPkgHandler and fedexPkgHandler2 have 0
   accomplishments and 0 technologies. These are broken records, not thin ones
1) [X] write a validator — `./validate.py` as of 2026-08-18 in 31c671d. Single-file
   Python 3, no deps. Errors are provably wrong (broken refs, unknown enum values,
   format drift, split files disagreeing with resume.json, skill _ids that do not
   reproduce); warnings are gaps against this spec. Exits 1 on errors only, so CI can
   gate on correctness while the content backlog is open; `--strict` fails on warnings
   too. It also subsumes the format check, so CI needs one command, not two
1) [ ] wire `./validate.py` into the CI/CD step alongside the generation work above
1) [ ] Jake Jones's recommendation carries `gigId: "brokerbin"` and no such gig exists.
   The company does (BrokerBin, employer) and the recommendation is dated 2008-02-26,
   so a gig record looks to be missing outright rather than misnamed. Write it
1) [ ] uuids.md rule 2 is wrong as written: it says `company._id = uuid5(NS, url)`, but
   irishtitan is deliberately two records — contractor and recruiter — sharing one url,
   and two ids cannot come from one input. None of the 35 company ids reproduce from
   url, name, fullname, or hostname under my namespace or ns:DNS/ns:URL; they are valid
   v5 with unrecorded inputs. Either pick a new key that is actually unique per record
   and regenerate, or amend uuids.md to admit companies are not reproducible. Skills are
   clean — all 151 reproduce exactly
