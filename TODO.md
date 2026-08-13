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
1) [ ] flesh out Target role — retitled to Software Architect 2026-08-12, but the record is still thin: 1 responsibility (which duplicates accomplishments[0] verbatim), 3 accomplishments, and `blurbs: null` despite 10 declared tiers. Project Slingshot was an internal CMS adopted across multiple departments and saved millions vs the legacy tool — the architecture and adoption story deserve writing up