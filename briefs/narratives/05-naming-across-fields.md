# Research — How other disciplines name and catalogue recurring stories

Researcher brief, 2026-09-19. Every rule quoted below was read in the primary
document unless marked otherwise. Where a source is a published standard, the
clause number is given so the rule can be checked.

**Verification note.** `loc.gov` returns HTTP 403 to this environment, so the
Subject Headings Manual sheets H 180 / H 170 could not be read directly. The two
H 180 rules quoted in §1 are taken from mirrors that quote them verbatim (Tulane
Technical Services; ACRL ANSS Cataloging Q&A) and are flagged in place. Everything
else in this brief — Cutter 1904, IFLA ICP 2016, ANSI/NISO Z39.19, Uther's ATU
introduction, Allport & Postman 1946–47, schema.org, Google's ClaimReview
reference, WHO 2015/2021/2022, Snopes' current ratings page, Phillips 2018, the
Debunking Handbook 2020 — was extracted from the document itself.

**The short version.** Six fields, five of them with decades of practice, have
converged on the same architecture: **a stable meaningless identifier, a neutral
authorised name, an unlimited set of recorded variant wordings, and a dated
history note explaining every change.** They disagree sharply on exactly one
question — *whose words do you use?* — and that disagreement is the interesting
part for Narrative Radar.

---

## 1. Library and archival authority control

### The standards that actually exist

| Document | Status | What it governs |
|---|---|---|
| Cutter, *Rules for a Dictionary Catalog*, 4th ed. (1904) | Historical, still the source of the principles | Specific entry, choice between synonyms |
| IFLA, *Statement of International Cataloguing Principles* (ICP) 2016 | Current international standard | The general principles, ranked |
| ANSI/NISO Z39.19-2005 (R2010) | Current American National Standard | Construction and **maintenance** of controlled vocabularies |
| LC *Subject Headings Manual*, H 180 | Current LC policy | Assigning and constructing LCSH |
| MARC 21 Format for Authority Data | Current | The record structure: 1XX / 4XX / 670 |
| RDA | Current | Preferred title (formerly "uniform title") |

### The rules, quoted

**Specific entry — Cutter rule 161:**

> "Enter a work under its subject-heading, not under the heading of a class which includes that subject."

Cutter's own gloss: this "is the main distinction between the dictionary catalog
and the alphabetico-classed."

**The precondition for having a name at all.** Cutter is explicit that a topic
must earn a heading before it can get one. On subjects that exist but are not yet
nameable:

> "…before the catalog can profitably follow its 'specific' rule in regard to them they must attain a certain individuality as objects of inquiry, and be given some sort of name, otherwise we must assign them class-entry."

This is an admission test, written in 1904. A thing with no settled name gets
filed under its class, not given an invented one.

**Whose words. Cutter, §2 "Choice between different names":**

> "Usage in both cases is the supreme arbiter, — the usage, in the present case, not of the cataloger but of the public in speaking of subjects."

**Cutter rule 169 — the tie-break order between synonyms.** Prefer the one that:
(a) is most familiar to the class of people who consult the library; (b) is most
used in other catalogs; (c) **"has fewest meanings other than the sense in which
it is to be employed"**; (d) comes first in the alphabet; (e) brings the subject
near related subjects. Note (c): ambiguity is a disqualifier, ranked above
convenience of filing.

**Cutter rule 171 — opposites collapse into one heading:**

> "Of two subjects exactly opposite choose one and refer from the other."

His examples: Temperance and Intemperance; Free Trade and Protection. A claim and
its denial are one entry, not two.

**IFLA ICP 2016 §2, the ranked general principles.** Convenience of the user
ranks first; 2.2–2.13 are unranked except that interoperability wins conflicts.
The four that matter here, verbatim:

- **2.2 Common usage.** "Vocabulary used in descriptions and access points should be in accordance with that of the majority of users."
- **2.3 Representation.** "A description should represent a resource as it appears. Controlled forms of names of persons, corporate bodies and families should be based on the way an entity describes itself."
- **2.4 Accuracy.** "Bibliographic and authority data should be an accurate portrayal of the entity described."
- **2.6 Significance.** "Data elements should be relevant to the description, noteworthy, and allow for distinctions among entities."

**ANSI/NISO Z39.19-2005 §5.3.5 — the three warrants.** Term selection is
justified by "the natural language used to describe content objects (literary
warrant), the language of users (user warrant), and the needs and priorities of
the organization (organizational warrant)." §6.6.1.1: "When two or more variants
have literary warrant, the most frequently used term should be selected as the
term."

**§6.6.1 — neutrality is a written rule, with an example:**

> "Neutral terms should be selected, e.g., developing nations rather than underdeveloped countries."

**§6.6.4 — slang and coinages are admitted, not banned:**

> "When no widely accepted alternative exists, the neologism, slang, or jargon term should be accepted as a term."

Such a term "may be labeled **provisional** … and may be elevated to full term
status as the term becomes accepted into the language" (§6.6.4.1). Where a
well-established alternative does exist, the slang becomes an entry term pointing
at it: "shrinks USE psychiatrists" (§6.6.4.2).

**§6.2.3 / §11.3 — how a vocabulary changes without breaking.** This is the part
most naming schemes get wrong, and NISO writes it out:

- A History Note "is used to track the development of terms over time … If appropriate, the history note may also include the date discontinued, the term that succeeded the term, and/or the term that preceded it." (§6.2.3)
- On modification: "If a term is modified, the date of the change should be recorded in the history note … and a USE reference should be made from the old form to the new form. If the controlled vocabulary is used in an indexing system, the date on which an old term was last assigned should be included in the history note." (§11.3.1.2)
- A retired term "may be retained in the controlled vocabulary for retrieval or historical purposes only. If it is retained, it must be marked, e.g., 'for retrieval purposes only,' and the date of its change in status must be recorded in the history note and displayed to users." (§11.3.2.1a)
- "Each term should have a history note recording its date of entry." (§11.3.2.2)
- And the honest caveat: "In very large systems, the cost of such re-indexing could be prohibitive."

**LC Subject Headings Manual H 180 — specificity and objectivity.** *(quoted via
mirrors; loc.gov unreachable from here)*

> "Assign headings that are as specific as the topics they cover."

H 180 also sets a coverage floor: a heading is assigned for a topic that
represents roughly **20% or more of the work**. And the objectivity rule, as
quoted by ACRL's ANSS cataloging guidance:

> "Avoid assigning headings that label topics or express personal value judgments regarding topics or materials."

The same guidance says catalogers must "treat the work as the author intended in
terms of whether the statements are fact or fiction" — the cataloguer's job is to
record what the work claims, not to adjudicate it. LCSH's own heading for this
material is **Common fallacies**, with *Misinformation*, *Misconceptions,
Popular* and *Errors, Popular* as non-preferred variants pointing to it.

### The record structure: name, variants, and where you found it

A MARC 21 authority record separates four things that Narrative Radar currently
mixes:

| Field | Job |
|---|---|
| **1XX** | The authorised heading — one, unique |
| **4XX** | See-from tracings: every rejected variant, pointing in |
| **5XX** | See-also: related authorised headings |
| **670** | **Source Data Found** — the citation where the term was actually observed, with the information found |

Field 670 is the evidence log for the name. "$a" (the source citation) is always
required. The name is not an opinion; it is a claim with a footnote.

### Uniform title / preferred title

AACR2's "uniform title" became RDA's **preferred title**: one controlled title
chosen to collocate every manifestation of a work regardless of what any
particular copy calls itself. The operative property:

> The title proper may vary from manifestation to manifestation, but the authorized access point will always be the same.

### Contested terms: the "Illegal aliens" case

LCSH's most-studied heading change is the clearest published example of what
happens when a heading with strong literary warrant becomes pejorative.

- 2014 and 2016: change proposed through the normal SACO process.
- 2016–2017: Congress directed the Library to hold the change.
- **12 November 2021:** LC announced cancellation. *Aliens* → **Noncitizens**;
  *Illegal aliens* → **Noncitizens** and **Illegal immigration** (later
  *Unauthorized immigration*).
- The stated reasoning: a heading "referring to the act of residing in a place
  without authorization should be used rather than a heading that describes the
  people as illegal or unauthorized"; *Aliens* is "often misunderstood"; the
  phrase *illegal aliens* "has become pejorative."
- The old heading survives as a **former heading** reference — a pointer, not a
  deletion. OCLC updated roughly 41,000 WorldCat records.
- No reversal since; the change stands as of this brief.

Two things to take from it. First, the rule that broke the tie was **describe the
act, not the person**. Second, the change took seven years and was resisted
politically — which is the real cost of having put a contested word in the
authorised position in the first place.

### What transfers to naming a narrative

1. **Four layers, not three.** ID (1XX-equivalent), authorised claim name,
   *recorded variant wordings* (4XX), and *where each variant was observed* (670).
   Narrative Radar has the first two. It has no variant register and no evidence
   field for the name itself.
2. **Describe the act, not the people.** The single transferable tie-break from
   the 2021 LC decision.
3. **Never delete a name.** Cancel it, mark it, date it, and point it at the
   successor. "Deleting a term in the database without replacing it with another
   term could, over time, seriously reduce access."
4. **Ambiguity disqualifies** (Cutter 169c). A name that already means three
   things loses to a duller name that means one.
5. **A claim and its denial are one narrative** (Cutter 171), with a cross-
   reference — not two cards competing for the same corpus.
6. **A narrative too young to have a settled name gets class-entry**, not an
   invented name. This is Cutter's rule and it is the honest answer to the
   `question` hook shape in SYSTEM.md §3.
7. **Slang and insider coinages are admissible but flagged `provisional`** until
   they settle — NISO's mechanism, and exactly right for a live YouTube corpus.

---

## 2. Folklore: tale-type and motif indexes

### What the indexes are

- **Aarne–Thompson–Uther (ATU)**, *The Types of International Folktales*, FFC
  284–286, Academia Scientiarum Fennica. Uther's comprehensive 2004 revision of
  Aarne (1910) / Thompson; revised and supplemented edition reissued 2024. The
  2024 introduction is the document quoted here.
- **Thompson, *Motif-Index of Folk-Literature*** (1932–36; rev. 1955–58), six
  volumes, alphanumeric classes A–Z.
- **Brunvand, *Encyclopedia of Urban Legends*** — the modern-legend equivalent,
  with a Type Index. Dutch and Belgian researchers assign **"Brunvand numbers"**
  with the prefix BRUN (e.g. **BRUN 02000 = The Microwaved Pet**; BRUN 03000 =
  The Babysitter and the Man Upstairs).

### What a "type" is, in the index's own words

> "Each 'tale type' presented here consists of a number, title, and a description of its contents, and must be understood to be flexible. It is not a constant unit of measure or a way to refer to lifeless material from the past. Instead, as part of a greater dynamic, it is adaptable, and can be integrated into new thematic compositions and media."

Thompson's definition of a motif: "the smallest element in a tale having a power
to persist in tradition." Uther is candid that the two do not cleanly separate:

> "On pragmatic grounds, a clear distinction between motif and type is not possible because the boundaries are not distinct."

And, on the whole enterprise:

> "Just as genres of narrative are only intellectual constructs, so, then, is any typology."

### The admission test

> "Each description represents an independent tale type that has been documented among at least three ethnic groups or over a long time period."

**Three independent groups, or long duration.** Types limited to a single ethnic
group "have been excised … except when they have reached a significant temporal,
ethnic, or geographic distribution." Types "with very brief or diffuse
descriptions have also been eliminated, particularly when the texts turned out to
be heterogeneous."

### How the index handles a story that mutates

This is folklore's specialist subject, and it uses three distinct devices.

**Oikotypes are folded in, not split off.** Regional variants (von Sydow's
*oikotype*) are absorbed:

> "many oikotypes have been integrated into widely-distributed types with significant regional variations (an oikotypical substratum), rather than as additional types or numbered subtypes."

**Subtypes get letters — and the letters mean nothing systematic.** Uther says so
outright: Thompson's practice of designating subtypes with A, B, C, A*, ** is
"problematic", and in ATU "such notations have no consistent significance: the
letters or asterisks are not necessarily intended to represent either a separate
type or a dependent subtype."

**Unclassifiable stories get a "miscellaneous type"**, "described only by their
theme, which is expressed through a common structure. Sometimes the best solution
has been to provide a summary of a single text as an example."

### How numbers and titles change

**Numbers are frozen. Titles are not.**

> "Because of the need for compatibility with the many old and new regional and international folktale catalogs, the type numbers that have been in use for nearly one hundred years remain unchanged."

> "For historical reasons, the existing numbering system for the tale types has been retained here — there was no need to reinvent the wheel."

Renumbering happens only to fix duplication, and is logged as a mapping:
**AaTh 1587 → ATU 927D.** Meanwhile:

> "The titles of the tale types have been partly revised, and the descriptions of the plots have been completely rewritten and expanded. For reference, **the former titles are also listed**."

### The house style for a type description

> "The main characters, both active and passive, and their opponents, must be named, and the tale's actions and objects and especially its situation must be recognizable."

And three concrete editorial rules, each of them a naming rule in disguise:

- **De-bias the actors.** "it was necessary to correct gender biases in the characterization of the main actors."
- **Say the thing instead of gesturing at it.** Be "explicit about sexual elements and themes (in contrast to the general AaTh description, 'obscene')."
- **Normalise drifting vocabulary.** "Terms that alternated in AaTh (e.g. ape vs. monkey) have been standardized. Others have been changed because of a shift of meaning (e.g. ass has become donkey)."

### The rule about counting

> "The numbers of variants in each of the regions are not reported because the compilers of different catalogs have used different criteria for inclusion. Users of these catalogs know how arbitrary and questionable such figures can be, because no guidelines or standards exist to prevent variants derived recently from printed sources from inflating the numbers."

### What the field admits is broken

- Alan Dundes, an outspoken critic who also called the indexes "two of the most valuable tools in the professional folklorist's arsenal", showed that types and motifs **overlap** — the conceptualisation itself leaks.
- The Motif-Index is criticised for overlapping subcategories, **censorship of obscene material**, and missing motifs.
- Uther's 2024 edition concedes the taxonomy "was developed specifically for (Northern) European folk tales" and that "unavoidable post-colonial echoes are observable in the entries owing to the history of research and its categorizations."

### What transfers to naming a narrative

1. **Number ≠ name.** Freeze the number forever; revise the title freely and keep
   the old titles visible. This is the cleanest published answer to "how do you
   rename without breaking the record".
2. **Adopt a hard admission test with a number in it.** ATU's is *three
   independent groups, or long duration*. Narrative Radar's equivalent — "told
   repeatedly by independent voices over time" — has no threshold. Give it one.
3. **Fold regional and format variants into one type** unless they show
   "structural or functional unity" of their own. Resist splitting.
4. **Ship a `miscellaneous` bucket** rather than forcing a bad name. Describe by
   theme, or quote one representative example.
5. **Do not publish variant counts across sources with different inclusion
   rules.** This is the single strongest external support for SYSTEM.md's
   requirement that every number in a title be re-derived and its basis recorded.
6. **Name the actors in the description.** A type description that does not name
   the villain, the victim and the situation is not usable.
7. **Multiple ID namespaces can coexist.** The Dutch Volksverhalenbank indexes one
   story under ATU, BRUN, VDK, SIN* and TM prefixes simultaneously. A Narrative
   Radar narrative can carry an external ClaimReview or ATU-style cross-reference
   without giving up its own ID.

---

## 3. Rumour and urban-legend cataloguing

### Allport and Postman, 1947 — and the finding almost nobody quotes

Gordon Allport and Leo Postman, "An Analysis of Rumor," *Public Opinion
Quarterly* 10(4), Winter 1946–47, pp. 501–517; expanded as *The Psychology of
Rumor* (Holt, 1947).

**The basic law of rumour**, verbatim:

> "R ~ i × a"
>
> "In plain words this formula means that the amount of rumor in circulation will vary with the importance of the subject to the individuals concerned times the ambiguity of the evidence pertaining to the topic at issue. The relation between importance and ambiguity is not additive but multiplicative, for if either importance or ambiguity is zero, there is no rumor."

**The three distortions**, verbatim:

- **Leveling.** "As a rumor travels, it tends to grow shorter, more concise, more easily grasped and told. In successive versions, more and more of the original details are leveled out."
- **Sharpening.** "the selective perception, retention, and reporting of a few details from the originally larger context." Universal sharpeners include "items distinguished by unusual size, and by striking, attention-getting phrases."
- **Assimilation.** "the powerful attractive force exerted upon rumor by habits, interests, and sentiments existing in the listener's mind … Items become sharpened or leveled to fit the leading motif of the story."

**The finding that should change how Narrative Radar thinks about names.** In
their worked case analysis, Allport and Postman observe:

> "when a scene is set, the label conferred upon the incident (especially if the label introduces the story and thus benefits from the primacy effect) tends to remain unchanged."

Their 51-question analysis guide makes it a coding field: **Q26. "Does its label
or locale persist?"** The label is the part of a rumour that survives leveling.
Everything else erodes; the name does not. Two corollaries they note in the same
passage:

- **Naming a person personalises the rumour.** "to specify a well known individual is a common device for personalizing a rumor and for assimilating it to common and conventional subject-matter, of current interest."
- **Precise numbers manufacture credibility.** "We find the use of concreteness to lend plausibility to the story. The precise amounts — $500 and $7000 — are mentioned. Part of the rationalizing process is to surround the item with the pseudo-authority of detail."

That third point cuts against Narrative Radar's own house style: the `tally` and
`scale` hook shapes use exactly the device Allport and Postman identify as the
rumour-monger's plausibility trick. It is legitimate when the number is audited
and the basis is published — which SYSTEM.md rules 6 and 7 already require — and
it is indistinguishable from the trick when it is not.

**The 51-question guide is itself a cataloguing schema.** It codes each rumour for
topical reference, verifiability, the ambiguity/importance balance, the kernel of
truth, leveling, sharpening, assimilation to expectancy, to linguistic habits, to
occupational/class/racial self-interest, and to prejudice.

### Snopes: what a canonical rumour record actually looks like

Snopes' current ratings page (last updated **7 May 2026**) states the governing
rule:

> "It's important to note the 'claim' statement on each fact check. Ratings evaluate the specific wording of that claim."

The record structure, from a live legend entry ("The Hook", Barbara Mikkelson,
published 2 December 1998):

| Element | Content |
|---|---|
| **Short name** | *The Hook* |
| **Standfirst** | "An escaped killer interrupts a young couple's make-out session." |
| **Claim** | A neutral third-person plot synopsis: "A couple's late night make-out session is cut short when they hear a report on the car radio about an escaped killer (who has a hook for a hand) in the vicinity…" |
| **Rating** | Legend |
| **Examples** | Multiple dated collected variants with source citations — `[Baker, 1982]`, `[Emrich, 1972]` — reproduced in full |

The **Claim is a synopsis, not an assertion, and not a quotation.** It is written
the way an ATU type description is written. The variants are the evidence, dated
and attributed, reproduced verbatim — Snopes' own note is that folklore examples
are reproduced "exactly as they find them" without correcting orthography.

**The "Legend" rating** is Snopes' equivalent of an unscorable verdict:

> "events so general or lacking in detail they could have happened to someone, somewhere, at some time, and are therefore essentially unprovable."

**Rating vocabulary changes are logged.** *Unproven*, *Unfounded*, *Lost Legend*
and *Research In Progress* are marked "(retired)" on the page with an explanation
of what replaced them, and the previous version of the page is archived and
linked. That is a NISO history note in journalistic clothing.

### What transfers to naming a narrative

1. **The name is the sticky part.** Allport and Postman measured it: details
   level out, the label persists. A name is not a convenience label on top of the
   narrative; it is the component most likely to outlive the corpus that produced
   it. SYSTEM.md's instinct — "a name is itself one more repetition" — is right,
   and understated.
2. **Write the claim name as a synopsis, not an assertion or a quotation.**
   Snopes and ATU independently arrived at the same form: neutral third person,
   present tense, names the actors and the situation.
3. **Keep a dated variant register with sources.** Snopes' `Examples` block is the
   4XX/670 pattern again, arrived at from folklore rather than from cataloguing.
4. **Have a rating for "unprovable by construction."** Snopes' *Legend* and
   STANDARD.md's *UNSCORABLE* are the same instrument. Say so, and use the folklore
   framing — it is more legible to a reader than "unscorable".
5. **Audit the plausibility devices you borrow.** Named individuals and precise
   numbers are documented rumour-amplifiers. Using them is defensible only under
   SYSTEM.md's `title_basis` discipline.
6. **Retire ratings in public.** Mark them retired, say what replaced them, archive
   the old page.

---

## 4. Fact-checking and claim standards

### ClaimReview: the formal schema

`ClaimReview` is a schema.org type extending `Review`. The relevant properties:

| Property | schema.org definition |
|---|---|
| `claimReviewed` | "A short summary of the specific claims reviewed in a ClaimReview." |
| `itemReviewed` | "The item that is being reviewed/rated." |
| `reviewRating` | "The rating given in this review." |

Google's structured-data reference makes `claimReviewed`, `reviewRating` and
`url` **required**; `author` and `itemReviewed` recommended. Two explicit wording
rules:

> "Try to keep this less than 75 characters to minimize wrapping when displayed on a mobile device."

> "Don't include the rating in the `claimReviewed` field. Instead, specify the rating in the `reviewRating` field."

**What the standard does *not* say.** There is no rule in schema.org or in
Google's reference about quoting versus paraphrasing, about attribution, or about
avoiding a misleading summary. The separation of *claim* from *verdict* is
enforced; the fairness of the claim's wording is not. That is delegated to the
IFCN and to house style, and it is the largest gap in the standard.

### IFCN Code of Principles

Five commitments, assessed against 31 criteria by independent assessors:

1. **Non-partisanship and fairness** — signatories "fact-check claims using the same standard for every fact check. They do not concentrate their fact-checking on any one side."
2. **Standards and transparency of sources** — "provide all sources in enough detail that readers can replicate their work."
3. **Transparency of funding and organization.**
4. **Standards and transparency of methodology** — "explain the methodology they use to select, research, write, edit, publish and correct their fact checks."
5. **Open and honest corrections policy** — "publish their corrections policy and follow it scrupulously."

Two sub-criteria bear directly on naming. On **selection**, applicants select
"based primarily on the reach and importance of the claims, and where possible
[explain] the reason" — which is Allport and Postman's *importance* variable,
turned into an editorial rule. On **representation**, fact-checkers must set out
"relevant evidence that appears to support the claim as well as relevant evidence
that appears to undermine it."

### Does naming a claim spread it? The current evidence

*The Debunking Handbook 2020* (Lewandowsky, Cook, Ecker et al.; a consensus
document with 22 named authors) settles a question Narrative Radar's naming rule
implicitly assumes.

On the **familiarity backfire effect**:

> "Repetition makes information more familiar, and familiar information is generally perceived to be more truthful than novel information … Early evidence was supportive of this idea, but more recently, exhaustive experimental attempts to induce a backfire effect through familiarity alone have come up empty. Thus, while repeating misinformation generally increases familiarity and truth ratings, **repeating a myth while refuting it has been found to be safe in many circumstances**, and can even make the correction more salient and effective."

And the handbook's own summary line: "Backfire effects are not as common as we
used to think. We cannot reliably predict the circumstances under which they
occur."

The prescribed structure is **FACT → (warning) → MYTH → FALLACY → FACT**:

- "If it's easy to do in a few clear words, state what is true first. This allows you to frame the message — you lead with your talking points, not someone else's."
- "The best corrections are as prominent (in the headlines, not buried in questions) as the misinformation."
- "Repeat the misinformation, only once, directly prior to the correction. One repetition of the myth is beneficial to belief updating."
- "But needless repetitions of the misinformation should be avoided: Although backfire effects are uncommon, we know that repetition makes information appear true."

### What transfers to naming a narrative

1. **Separate the claim from the verdict at the schema level.** ClaimReview
   enforces it: the rating may not appear in `claimReviewed`. Narrative Radar
   should enforce the same — no claim name may contain a verdict word.
2. **75 characters.** An independently arrived-at limit, for the same reason as
   SYSTEM.md's 60: mobile wrapping. The 60-char hook rule has external support.
3. **Naming a claim once, attached to the finding, is safe.** The familiarity
   backfire is not reliably reproducible. This licenses SYSTEM.md's attributed
   claim names — the risk it guards against is smaller than it assumes. What is
   *not* licensed is repeating the claim across the ID, the card heading, the
   hook and the body: "needless repetitions … should be avoided."
4. **Lead with the finding, not the claim.** "You lead with your talking points,
   not someone else's" is the empirical case for SYSTEM.md's preference for
   `tally` / `clock` / `split` / `scale` over the `question` shape.
5. **Publish the selection rule.** IFCN requires a public statement of how claims
   are chosen. Narrative Radar's docket has no published selection statement.
6. **Fill the gap the standard leaves.** No published standard governs the
   fairness of the claim's wording. Narrative Radar's believer test — "it passes
   if a believer would call it a fair statement of what they believe" — is
   *better specified than the international standard*. That is a defensible
   public differentiator; write it up as a rule, not a note.

---

## 5. Epidemiology and disease naming

### WHO, *Best Practices for the Naming of New Human Infectious Diseases* (WHO/HSE/FOS/15.1, May 2015)

The only document in this brief written *because names caused measurable harm*.
Its stated aim is to "minimize unnecessary negative impact of disease names on
trade, travel, tourism or animal welfare, and avoid causing offence to any
cultural, social, national, regional, professional or ethnic groups."

**Terms that SHOULD be used:**

| Category | Examples given |
|---|---|
| Generic descriptive terms | respiratory disease, neurologic syndrome, watery diarrhoea |
| Specific descriptive terms (when supported by information) | progressive, juvenile, severe, winter |
| Pathogen, when known | coronavirus, influenza virus, salmonella |

**Terms that should be AVOIDED:**

| Banned category | Examples given |
|---|---|
| Geographic locations | Middle East Respiratory Syndrome, Spanish Flu, Rift Valley fever |
| People's names | Creutzfeldt-Jakob disease, Chagas disease |
| Animal or food species | swine flu, bird flu, monkey pox |
| Cultural, population, industry or occupational references | legionnaires |
| Terms that incite undue fear | unknown, fatal, epidemic |

Dr Keiji Fukuda, then Assistant Director-General for Health Security:

> "Disease names really do matter to the people who are directly affected. We've seen certain disease names provoke a backlash against members of particular religious or ethnic communities, create unjustified barriers to travel, commerce and trade, and trigger needless slaughtering of food animals."

Note the ban on **fear words** — "unknown, fatal, epidemic". SYSTEM.md rule 4
("no fear word beside an urgency word") is the same rule, arrived at
independently, and WHO's version is stricter: the fear word is banned outright,
not just in combination.

### The two-layer solution: SARS-CoV-2 variant labels, 31 May 2021

WHO assigned Greek-letter labels to variants of interest and concern. The stated
problem was precisely a naming failure:

> "While [scientific] names have their advantages, these names can be difficult to say and recall and are prone to misreporting … as a result, people often resort to calling variants by the places where they are detected, which is stigmatizing and discriminatory."

And the critical design decision:

> "These labels do not replace existing scientific names (e.g. those assigned by GISAID, Nextstrain and Pango), which convey important scientific information and will continue to be used in research."

**Two registers, both official, neither replacing the other:** a short public
label optimised for saying and remembering (Alpha, Delta, Omicron), and a precise
technical identifier optimised for lineage tracking (B.1.617.2). WHO also states
the labels were chosen "after wide consultation and a review of many potential
naming systems" by a convened expert group.

### Retiring a name in public: mpox, 2022

Two separate WHO actions in 2022:

- **12 August:** virus clades renamed away from geography. Former *Congo Basin
  (Central African)* clade → **Clade I**; former *West African* clade → **Clade
  II**, with subclades IIa and IIb.
- **28 November:** the disease name. WHO adopted **mpox** as the preferred term,
  with an explicit **one-year dual-use transition** during which both names were
  used simultaneously while "monkeypox" was phased out.

The trigger is documented: "racist and stigmatizing language online and in other
settings was observed and reported to WHO."

### What transfers to naming a narrative

1. **Ban the proper noun by default.** Place names and personal names go in the
   description, never in the identifier. A narrative called
   `canada-condo-crash` is already carrying a geographic slur risk that
   `condo-oversupply-crash-claim` does not.
2. **Ban fear vocabulary from the identifier outright**, not merely in
   combination with urgency. WHO's list — "unknown, fatal, epidemic" — maps
   cleanly onto "collapse", "crisis", "coming".
3. **Two registers is the right architecture, and WHO validates it.** A
   pronounceable public label plus a precise technical identifier, with the
   technical one explicitly *not* deprecated. Narrative Radar's ID / claim name /
   hook title is a three-register version of the same idea.
4. **A rename is a dated, dual-running transition with a published reason** — not
   a silent edit. Twelve months of both names is WHO's answer.
5. **Names that name a group get weaponised against that group.** This is the
   whole reason the 2015 document exists, and it is the strongest argument in
   this brief against naming a narrative after the people who believe it.

---

## 6. Conspiracy theory and extremism research

This is the field with the **least formal standardisation and the sharpest
disagreement**. There is no ATU, no ICP, no WHO document. What exists is a set of
editorial guidance documents, an academic argument about terminology, and one
vigorous empirical dispute.

### How the names actually arose — and why that is a problem

Almost every well-known name in this space is an **endonym**: coined by the
movement, then adopted wholesale by researchers and journalists.

- **Great Replacement** — from Renaud Camus's *Le Grand Remplacement* (2011). The
  researchers use the propagandist's book title. Mattias Ekman's study of how the
  claim crossed into the mainstream is published as "The great replacement:
  Strategic mainstreaming of far-right conspiracy claims," *Convergence* 28(4),
  2022, pp. 1127–1143 — the title carries the endonym, with the classifier
  bolted on.
- **QAnon** — from the anonymous poster's own handle plus "anon".
- **Pizzagate** — a coinage from within the campaign.

The working convention, unwritten but near-universal in the literature, is
**endonym + classifier**: "the Great Replacement *conspiracy theory*", "the
QAnon *movement*". Wikipedia's article titles encode it. It is a compromise: the
searchable name is preserved, and the frame is attached to it — which is
structurally identical to SYSTEM.md's attributed claim name ("*The 'housing crash
is coming next year' story*").

### The classifier itself is contested

Butter and Knight's *Routledge Handbook of Conspiracy Theories* (2020) treats the
status of the term as an open question: "conspiracy theory" carries pejorative
connotations and has been used "by elites to mark out particular beliefs as
beyond the pale of rational political discourse." Some scholars prefer
*conspiracy narrative* or *conspiracy belief*. And the classifier is not always
accurate: Mark Sedgwick has argued the Great Replacement does not meet the
criterion of a hidden conspiring group at all. **The classifier can be wrong in
both directions — too pejorative for the believer, too generous to the claim.**

### The one published guidance document: Phillips, *The Oxygen of Amplification*

Whitney Phillips, Data & Society Research Institute, May 2018. Interview-based;
recommendations "shaped by interviewees themselves". The naming-relevant rules:

**A three-part newsworthiness test before you cover anything:**

- **Tipping Point** — "has the story extended beyond the interests of the community being discussed? … whether a particular meme has been broadly shared by anyone outside the core group of participants."
- **Social Benefit** — "will the story have a positive social benefit, open up a new conversation, or add weight or exemplars to an existing conversation?"
- **Potential Harms** — "will the story produce harm … or could an audience use the story to cause harm (attacking sources, imitating crimes)?"

For **objectively false information** specifically, add: is there a public-health
takeaway from the debunking, is there a political or social action point, and "is
the risk of entrenching/rewarding the falsehood in some stories … worth
dislodging the falsehood in others." If every answer is no, "then the story isn't
worth reporting at that time."

**Precision over mass nouns:**

> "To the extent possible, stories should specify the number of participants in a particular online attack/campaign, rather than using vague mass nouns (i.e., trolls did this, the alt-right did that) … When describing media manipulation campaigns of any kind, stories and their headlines should employ the most precise language possible."

**Retire a label once it becomes a cloak:**

> "Given how nebulous the term has become, and how easily it is used to cloak hateful behaviors, 'troll' should be used sparingly in stories and headlines, if at all."

**And the rule that directly contradicts IFLA ICP 2.3:**

> "Stories should avoid deferring to manipulators' chosen language, explanations, or justifications … They may say it's 'just trolling,' but stories should describe the behaviors, and their impact on targeted communities, as accurately and as free of euphemism as possible. Just as importantly, **stories should not employ the aggressors' insider lingo to describe specific actions or targets**."

Also: "minimize the inclusion of euphemistic dog whistles", and "reporting should
avoid framing bad actors as the center of the narrative."

### Strategic silence versus strategic amplification

Joan Donovan and danah boyd, "Stop the Presses? Moving From Strategic Silence to
Strategic Amplification in a Networked Media Ecosystem," *American Behavioral
Scientist* (online September 2019; in the 2021 issue), DOI
10.1177/0002764219878229. **Strategic silence** is defined in the associated
Media Manipulation Casebook as "the use of editorial discretion for the public
good. For example, journalistic or editorial standards to not report on
suicide." Their argument is that silence alone no longer works in a networked
ecosystem, and that newsrooms and platforms need **strategic amplification** —
deliberate, designed decisions about what to spread and how — instead.

### The empirical dispute: do not name them

Adam Lankford and Eric Madfis, "Don't Name Them, Don't Show Them, But Report
Everything Else: A Pragmatic Proposal for Denying Mass Killers the Attention They
Seek and Deterring Future Offenders," *American Behavioral Scientist*
62(2), 2018, DOI 10.1177/0002764217730854. The proposal: withhold names and
photos of mass shooters, report everything else in as much detail as desired. It
was backed by an October 2017 open letter signed by 149 scholars and law-
enforcement professionals.

**It is genuinely contested.** The counter-arguments, from journalists and from
within the field:

- Withholding a name creates its own distortion and invites speculation. CBC's
  director of journalism standards: "It is not our role to filter or purposefully
  withhold information of this nature."
- Accountability reporting requires names — Jaclyn Schildkraut, a proponent of
  reformed coverage, has praised the detailed Uvalde accountability work.
- Even No Notoriety's own position is narrower than the slogan: it "means not
  gratuitously [naming], or giving them prominent placement", not never naming.

### Retiring a term that got weaponised: "fake news"

Claire Wardle and Hossein Derakhshan, *Information Disorder: Toward an
Interdisciplinary Framework for Research and Policy Making* (Council of Europe,
2017), refused the term "fake news" on two grounds: it is "woefully inadequate to
effectively capture the complexity of the phenomenon of information pollution",
and it was being used by politicians "to describe news organizations they don't
like." They replaced it with a three-way distinction — **mis**information (false,
no harm intended), **dis**information (false, harm intended), **mal**information
(true, weaponised).

Note the pattern, third occurrence in this brief: **a term with overwhelming
common usage was retired because it had been captured** — LCSH's *illegal
aliens*, Phillips's *troll*, Wardle's *fake news*. Common usage is a starting
point, not a defence.

### What transfers to naming a narrative

1. **Run the tipping-point test before a narrative gets a public name at all.**
   Has it left the community that produced it? Phillips's three criteria are
   directly implementable as admission fields alongside SYSTEM.md's grip profile.
2. **Endonym + classifier is the working convention, and it matches what
   Narrative Radar already does.** "The '*X*' story" is the classifier. Keep it,
   and keep it in the same typographic position every time.
3. **Numbers instead of mass nouns.** "43 channels say…" beats "creators say…".
   SYSTEM.md's `split` and `scale` shapes are the Phillips rule already
   implemented; make it a constraint rather than a preference.
4. **Do not adopt insider lingo into the authorised name.** Record it as a
   variant (4XX), search on it, never promote it. This is where Narrative Radar
   must depart from library practice — see the disagreement below.
5. **Budget for retiring a name.** Three of the fields here have had to retire a
   dominant term. Build the mechanism before you need it.
6. **Naming a *person* and naming a *claim* are different decisions with
   different evidence bases.** The don't-name-them literature is about
   perpetrators, and it is contested even there. Do not import it wholesale as a
   reason not to name claims.

---

## Comparison across the six fields

| | **Neutrality** | **Common usage vs precision** | **Mutation over time** | **Contested / pejorative terms** | **Identifier stability** |
|---|---|---|---|---|---|
| **Library authority control** (Cutter; ICP 2016; Z39.19; LCSH H 180) | Explicit written rule. Z39.19 §6.6.1: "Neutral terms should be selected". H 180: "Avoid assigning headings that label topics or express personal value judgments" | **Usage wins**, with limits. Cutter: "the usage … not of the cataloger but of the public". Tie-break 169c prefers the least ambiguous term | History notes (§6.2.3); USE references old→new; retired terms kept "for retrieval purposes only" with the date shown | Changed, slowly, through a public proposal process. *Illegal aliens* → *Noncitizens* took 7 years and a congressional fight. Rule that decided it: **name the act, not the person** | Very high. Retired headings survive as former-heading pointers; deletion is a last resort because it destroys access |
| **Folklore** (ATU; Motif-Index; Brunvand) | Descriptive, not evaluative — but 2024 ATU concedes "unavoidable post-colonial echoes" and corrected gender bias in descriptions | Precision wins. Type descriptions "completely rewritten and made more precise"; vocabulary standardised (ape/monkey, ass→donkey) | **Its specialist subject.** Type is "flexible … not a constant unit of measure". Oikotypes folded into a parent type as an "oikotypical substratum" rather than split off | Handled by rewriting the description, not the number. "obscene" replaced with explicit content; misogynist framings corrected | **Highest of any field.** Numbers unchanged for ~100 years; "there was no need to reinvent the wheel." Moves logged as mappings (AaTh 1587 → ATU 927D). Titles change freely; former titles retained |
| **Rumour / urban legend** (Allport & Postman; Snopes) | Claim written as a neutral third-person synopsis, never as an assertion | Both. Canonical short name (*The Hook*) for usage; verbatim dated variants for precision | Leveling / sharpening / assimilation is the model of mutation. **The label is the part that does *not* mutate** | Retired ratings marked "(retired)" with replacement explained and the prior page archived | Medium. Stable URL slugs; Brunvand numbers (BRUN 02000) where a formal index exists. No universal registry |
| **Fact-checking** (ClaimReview; IFCN; Debunking Handbook) | Enforced structurally: the rating may not appear in `claimReviewed`. Fairness of wording is **not** covered by any standard | Precision, under a hard length cap: "less than 75 characters" | Weak. ClaimReview has no versioning for a claim that evolves; each check is a new record. IFCN requires a published corrections policy | Handled by house style, not by the schema. IFCN requires equal treatment "regardless of who made the claim" | Low. The `url` is the identifier; there is no claim-level ID shared across fact-checkers |
| **Epidemiology** (WHO 2015 / 2021 / 2022) | **The strictest.** Places, people, animals, occupations and fear words all banned from the name | **Split deliberately into two registers.** Public label optimised for saying and remembering; Pango/GISAID scientific name retained unchanged for precision | Rename with a **dated dual-running transition** — mpox and monkeypox ran together for one year | Renamed on documented evidence of harm, by a convened expert group, with the reason published | High on the technical layer (lineage names never retired), deliberately mutable on the public layer |
| **Conspiracy / extremism research** (Phillips; Donovan & boyd; Wardle) | Contested at the root: the classifier "conspiracy theory" is itself argued to be pejorative | **Rejects common usage where it is the movement's own.** "stories should not employ the aggressors' insider lingo"; use "the most precise language possible"; numbers not mass nouns | Terms are retired when captured: "troll" (Phillips 2018), "fake news" (Wardle & Derakhshan 2017) | No standard body, no process. Retirement happens by argument and adoption | **Lowest.** No registry, no IDs. Names are endonyms that stuck, stabilised only by Wikipedia titles and citation habit |

### Where the fields genuinely disagree

**1. Whose words go in the authorised name.** This is the real fault line.

- **IFLA ICP 2016 §2.3 (Representation):** "Controlled forms of names … should be based on the way an entity describes itself."
- **Phillips 2018:** "stories should not employ the aggressors' insider lingo to describe specific actions or targets."

These cannot both be followed. Cataloguing assumes the named entity is not an
adversary; manipulation research assumes it is. A narrative-tracking product sits
between the two cases — most narratives are sincerely held, some are engineered.
**The resolution is layered, and both fields already permit it:** the endonym is
recorded as a variant and used for search (Z39.19 §6.6.4.2, "shrinks USE
psychiatrists"); the authorised name is the neutral description of the act. That
is the LCSH *illegal aliens* resolution, applied generally.

**2. Do you freeze the number or the name?** ATU freezes the number and lets the
title drift. WHO freezes the scientific lineage and lets the public label drift.
ClaimReview freezes neither. Library practice freezes both but allows supersession
with pointers. **Three of the four say: freeze exactly one layer, and let the
public-facing layer move.**

**3. Does naming the claim spread it?** The Debunking Handbook 2020 says the
familiarity backfire has not survived replication and one repetition attached to a
refutation "has been found to be safe in many circumstances". Phillips and the
strategic-silence line say coverage itself is the harm. These are answering
different questions — belief updating in an individual reader versus reach and
incentive at population scale — and both can be true. The tipping-point test is
the practical reconciliation: **once the story has left its origin community, the
amplification cost of naming it has already been paid by someone else.**

**4. Is a count publishable?** ATU refuses to publish variant counts across
catalogues with different inclusion rules. Phillips demands counts instead of mass
nouns. The difference is whether the inclusion rule is published: **ATU's
objection is to counts without a stated criterion, not to counts.** SYSTEM.md's
`title_basis` requirement already satisfies Uther's objection and Phillips's
demand at the same time.

### The five rules all six fields agree on

1. The public name and the stable identifier are different objects.
2. Every rejected or superseded wording is recorded, never deleted.
3. Every change is dated, with a reason, and visible to the reader.
4. A name states the situation; the verdict lives in a separate field.
5. A name that has been captured or that names a group is a liability, whatever
   its usage share.

---

## Sources

**Library and archival authority control**
- Charles A. Cutter, *Rules for a Dictionary Catalog*, 4th ed., 1904 — full text: https://archive.org/details/rulesforadictio06cuttgoog (rules 161, 166–171, "Objects", p. 12)
- IFLA, *Statement of International Cataloguing Principles (ICP) 2016* — https://www.ifla.org/files/assets/cataloguing/icp/icp_2016-en.pdf (§2.1–2.13)
- ANSI/NISO Z39.19-2005 (R2010), *Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies* — https://www.anzsi.org/wp-content/uploads/2019/05/z39-19-2005r2010.pdf (§5.3.5, 6.2.2–6.2.3, 6.6, 11.3)
- LC *Subject Headings Manual* H 180 — https://www.loc.gov/aba/publications/FreeSHM/H0180.pdf (403 from this environment; quoted via https://www2.tulane.edu/~techserv/lcsh%20introd.html and https://acrl.ala.org/anss/index.php/publications/cataloging-qa/what-kinds-of-subject-headings-are-used-for-false-information-how-do-library-of-congress-subject-headings-describe-fallacies/)
- MARC 21 Format for Authority Data, field 670 "Source Data Found"; 4XX See From Tracings — https://www.itsmarc.com/crs/mergedprojects/helpauth/helpauth/idh_670_auth.htm
- LC, *Library of Congress to Cancel the Subject Heading "Illegal Aliens"* (12 November 2021) — https://www.loc.gov/catdir/cpso/illegal-aliens-decision.pdf (403 here; reported at https://americanlibrariesmagazine.org/blogs/the-scoop/library-of-congress-changes-illegal-aliens-subject-heading/)

**Folklore**
- Hans-Jörg Uther, "Introduction to the Revised and Supplemented Edition", *The Types of International Folktales*, FFC 284–286 (2024 edition of the 2004 ATU) — https://www.folklorefellows.fi/wp-content/uploads/FFC-284-286-Uther-2024-Introductions.pdf
- Stith Thompson, *Motif-Index of Folk-Literature* (1955–58) — https://archive.org/details/Thompson2016MotifIndex
- Greg Kelley, review of Brunvand, *Encyclopedia of Urban Legends*, updated and expanded ed., *Journal of Folklore Research Reviews* — https://scholarworks.iu.edu/journals/index.php/jfrr/article/view/38934 (BRUN numbers)
- Volksverhalenbank van de Lage Landen, catalogue prefixes (ATU, BRUN, VDK, SIN*, TM) — https://www.verhalenbank.nl/zoekhulp

**Rumour and urban legend**
- Gordon W. Allport and Leo Postman, "An Analysis of Rumor", *Public Opinion Quarterly* 10(4), Winter 1946–47, 501–517 — https://www.romolocapuano.com/wp-content/uploads/2018/10/ALLPORT_POSTMAN_AN-ANALYSIS-OF-RUMOR.pdf; book: *The Psychology of Rumor*, Holt, 1947 — https://archive.org/details/psychology_of_rumor
- Snopes, *Fact Check Ratings* (page updated 7 May 2026) — https://www.snopes.com/fact-check-ratings/
- Snopes, "The Hook" (Barbara Mikkelson, 2 December 1998) — https://www.snopes.com/fact-check/the-hook/

**Fact-checking**
- schema.org, `ClaimReview` — https://schema.org/ClaimReview
- Google Search Central, *Fact Check (ClaimReview) structured data* — https://developers.google.com/search/docs/appearance/structured-data/factcheck
- IFCN, *The commitments of the Code of Principles* — https://ifcncodeofprinciples.poynter.org/the-commitments
- Lewandowsky, Cook, Ecker et al., *The Debunking Handbook 2020* — https://skepticalscience.com/docs/DebunkingHandbook2020.pdf

**Epidemiology**
- WHO, *Best Practices for the Naming of New Human Infectious Diseases*, WHO/HSE/FOS/15.1, May 2015 — https://www.who.int/publications/i/item/WHO-HSE-FOS-15.1; announcement: https://www.who.int/news/item/08-05-2015-who-issues-best-practices-for-naming-new-human-infectious-diseases
- WHO, *WHO announces simple, easy-to-say labels for SARS-CoV-2 Variants of Interest and Concern*, 31 May 2021 — https://www.who.int/news/item/31-05-2021-who-announces-simple-easy-to-say-labels-for-sars-cov-2-variants-of-interest-and-concern
- WHO, *Monkeypox: experts give virus variants new names*, 12 August 2022 — https://www.who.int/news/item/12-08-2022-monkeypox--experts-give-virus-variants-new-names
- WHO, *WHO recommends new name for monkeypox disease*, 28 November 2022 — https://www.who.int/news/item/28-11-2022-who-recommends-new-name-for-monkeypox-disease

**Conspiracy and extremism research**
- Whitney Phillips, *The Oxygen of Amplification: Better Practices for Reporting on Extremists, Antagonists, and Manipulators Online*, Data & Society, May 2018 — https://datasociety.net/wp-content/uploads/2018/05/Phillips_Oxygen_Exec_Summary_V3.pdf
- Joan Donovan and danah boyd, "Stop the Presses? Moving From Strategic Silence to Strategic Amplification in a Networked Media Ecosystem", *American Behavioral Scientist*, DOI 10.1177/0002764219878229 — https://journals.sagepub.com/doi/abs/10.1177/0002764219878229; definition at https://mediamanipulation.org/definitions/strategic-silence/
- Adam Lankford and Eric Madfis, "Don't Name Them, Don't Show Them, But Report Everything Else", *American Behavioral Scientist* 62(2), 2018, DOI 10.1177/0002764217730854 — https://journals.sagepub.com/doi/abs/10.1177/0002764217730854
- Claire Wardle and Hossein Derakhshan, *Information Disorder: Toward an Interdisciplinary Framework for Research and Policy Making*, Council of Europe, 2017 — https://rm.coe.int/leaflet-information-disorder-en/168079cece
- Michael Butter and Peter Knight (eds.), *Routledge Handbook of Conspiracy Theories*, 2020 — https://www.routledge.com/Routledge-Handbook-of-Conspiracy-Theories/Butter-Knight/p/book/9781032173986
- Mattias Ekman, "The great replacement: Strategic mainstreaming of far-right conspiracy claims", *Convergence* 28(4), 2022, 1127–1143 — https://journals.sagepub.com/doi/10.1177/13548565221091983
- Media Manipulation Casebook definitions and code book — https://mediamanipulation.org/definitions/
