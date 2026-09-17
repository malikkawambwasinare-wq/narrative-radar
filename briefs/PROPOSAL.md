# The collection engine — proposal

The full proposal, with budgets and the build plan, is a living document:
https://claude.ai/code/artifact/d4fa579f-9c01-4d25-8dc8-f6d32f7ce67d

What it settles, in one paragraph. The paste is the front door; the library exists
to make the answer behind a paste good, and it stays bounded, because YouTube's
30-day refresh rule taxes every stored title forever. Growth is demand-shaped: a
pasted link that lands in a narrative we hold is a hit, a link that does not names
a channel real people watch and we do not collect, and that channel is queued.
One number runs it, the paste hit rate, and above roughly three quarters further
collection is vanity.

The rules the code follows live beside it:

- [The narrative system](narratives/SYSTEM.md) — what a narrative is, how it is named and graded
- [The extraction pipeline](collection-engine/PIPELINE.md) — claim, then narrative, then shelf
- [Which channels matter](collection-engine/CHANNELS.md) — the ledger's tiers and tests
- [The audit application](collection-engine/AUDIT.md) — draft answers for YouTube
