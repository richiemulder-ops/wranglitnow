# CRM — Index

The people, organizations and meetings you deal with. One note per entity, linked
by `[[wikilink]]` from everywhere else. Nothing is duplicated — a person's phone
number lives on their note and nowhere else.

This index is a hub, not a database. As your CRM grows, the team keeps it current:
Penn adds entries when a new person or organization first appears, and Larry checks
it during the Librarian pass at session close.

## Folders

| Folder | What goes in it | Template |
|---|---|---|
| `People/` | One note per human you interact with | [[Team Knowledge/Templates/person]] |
| `Organizations/` | One note per company, client, supplier or body | [[Team Knowledge/Templates/organization]] |
| `Meetings/` | One note per meeting, call or interview | written by [[WS-007-file-a-meeting-and-extract-actions]] |

## Rules

- **Start from the template.** Every note in `People/` and `Organizations/` begins
  from the matching file in `Team Knowledge/Templates/`. Structured data goes in
  YAML frontmatter; narrative goes in the body. The field schemas are defined in
  [[GL-002-frontmatter-conventions]].
- **Naming is kebab-case.** `jane-smith.md`, `acme-corp.md`. Where two people share
  a name, disambiguate with the organization: `jane-smith-acme.md`. See
  [[GL-001-file-naming-conventions]].
- **Link, never copy.** If a person works at an organization, their note links to
  the organization note. The employer is not written twice.
- **Meetings are filed, not summarized.** Dropping a transcript or saying "file this
  meeting" runs [[WS-007-file-a-meeting-and-extract-actions]], which writes the
  meeting note, stubs any new people or organizations, and creates one note in
  `Actions/` per action item.

## People

<!-- Penn appends one line per person: [[filename]] — role, organization, context -->

_No entries yet._

## Organizations

<!-- Penn appends one line per organization: [[filename]] — what they are, your relationship -->

_No entries yet._

## Meetings

<!-- WS-007 appends one line per meeting: [[YYYY-MM-DD-slug]] — who, what it covered -->

_No entries yet._
