"""Narrative Radar — one definition of the words that carry a claim.

Shared by every stage, so "what is a claim word" and "what is rhetoric" cannot
drift apart between discovery and filing. A term earns its place in a
narrative's vocabulary only if it names a SUBJECT: not a stopword, not a claim
marker, not a sales formula. Without this test a corpus teaches the matcher its
own turns of phrase — "about to pop" learned from housing then files a bitcoin
video under housing.
"""
import re

CLAIM_MARK = re.compile(r"""\b(
 will|won'?t|going\ to|about\ to|coming|next\ year|by\ 20\d\d|soon|imminent|
 is|are|isn'?t|aren'?t|was|were|has|have|
 causes?|caused|cause|drives?|proves?|proven|shows?|means?|explains?|
 crash(?:es|ing)?|collaps(?:e|es|ing)|boom|bubble|burst|end(?:s|ing|ed)?|dead|dying|over|
 bans?|banned|wins?|beats?|replac(?:e|es|ing)|kills?|saves?|fix(?:es)?|
 should|must|why|truth|really|actually|myth|lie|scam|hoax
)\b""", re.X | re.I)


RHETORIC = set("""truth truths shocking shock brutal harsh dark ugly hidden secret real reality actually
really literally insane crazy wild unbelievable believe know knows knowing learn learned tell tells telling
told say says said reveal reveals revealed revealing explain explains explained explaining expert experts
economist economists doctor doctors analyst analysts guru warns warning nobody everyone everybody someone
thing things something anything everything stuff way ways here there they you your his her our their
biggest bigger huge massive major minor small tiny crazy important must need needs needed want wants
come comes coming came get gets getting got make makes making made take takes taking took give gives
happen happens happening happened work works working worked try tries trying let lets good bad worse
worst better best right wrong sure certain maybe perhaps probably possibly obviously clearly simply just
one two three next last first final new old full part update guide tips tricks hack hacks step steps
watch watching look looking see seeing seen saw start starts starting stop stops stopped keep keeps
it's here's what's that's there's don't doesn't isn't won't can't didn't you're we're they're i'm let's
well enough far away back out off again still yet ever never always sometimes soon later ahead behind
save saves saving saved buy buys buying bought sell sells selling sold use uses using used doing does
much many more less least own free easy hard simple quick fast slow big long short low high""".split())



def has_content(term):
    """True when the term names something, once claim verbs and rhetoric are removed."""
    return any(w for w in term.split()
               if w not in RHETORIC and not CLAIM_MARK.fullmatch(w))
