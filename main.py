#!/usr/bin/env python3
"""Five Seconds to Explain the Glass entry.

Writes the single sentence a house cat would say in its own defence
in the five seconds after sweeping a glass off the table, to
/output/entry.txt.

How it picks the line: twelve original candidate excuses, each
written for this entry, are scored against the judge's five criteria,
in the judge's own order of importance:

  1. one sentence of at most 200 characters in which a house cat
     excuses knocking a glass off the table
  2. sounds like a cat's own logic, self-interest and total lack of
     remorse, rather than a person apologising
  3. lands a fresh comic idea, not the obvious gravity, slippery-edge
     or it-was-already-falling lines
  4. fits the five seconds: a spoken line a cat could plausibly
     deliver, not a written paragraph of reasoning
  5. uses every character well, with no padding, throat-clearing or
     repeated joke

Each criterion is rated 0-5 and weighted 2, 5, 4, 3, 2, matching the
judge's priority order (cat voice and freshness carry the most
weight after validity). The highest total wins; ties go to the
earliest candidate in the list, so the choice is fully deterministic.

Freshness is not only hand-rated: any candidate that leans on one of
the tired lines the judge names outright (gravity, a slippery edge,
a glass already falling) loses one freshness point per such phrase
found in its own text (clamped at zero), so an obvious line cannot
win on a generous hand rating alone.

Revision pass: the winning draft is then revised once, by hand, in
a second pass that fixes its real weaknesses (see REVISION below).
The revised text is the entry. The program checks the revised text
against the gate and against a no-apology word list before writing
it, and prints the SHA-256 of the file it wrote.

No network, no external input, no randomness. The program verifies
its own output (1-200 characters, a single line, UTF-8) and prints
the SHA-256 of the file it wrote.
"""

from hashlib import sha256
from os import environ, makedirs
from sys import exit as finish, stderr

# Weights for the five judge criteria, in the judge's priority order:
# valid, cat voice, fresh, five seconds, tight.
WEIGHTS = (2, 5, 4, 3, 2)

# The obvious lines the judge names outright. A candidate leaning on
# one of these has already been told a thousand times; each hit costs
# one freshness point. Matched case-insensitively against the text.
CLICHES = (
    "gravity",
    "slippery",
    "already falling",
    "leaning toward the edge",
)

# Words that would concede the argument: an apology or a confession
# in any form. The revised entry must contain none of them.
APOLOGY_WORDS = (
    "sorry",
    "apologise",
    "apologize",
    "my fault",
    "my bad",
    "didn't mean",
    "did not mean",
    "forgive me",
)

# Each candidate: (text, (valid, cat voice, fresh, five seconds, tight)).
# All twelve lines are original, written for this entry, each a single
# sentence of at most 200 characters.
CANDIDATES = [
    (
        "That glass had been leaning toward the edge for an hour, so "
        "I ran a controlled gravity test before it could ambush you.",
        (5, 3, 2, 4, 4),
    ),
    (
        "I did not knock it off, I relocated it to the floor, where "
        "it belongs, because the table was overcrowded and something "
        "had to go.",
        (5, 4, 3, 4, 4),
    ),
    (
        "The glass was sitting in my sunbeam after three warnings, so "
        "I removed it, because I do not negotiate with glassware.",
        (5, 5, 5, 5, 4),
    ),
    (
        "You left a glass on my table, so I performed a safety "
        "inspection, it failed, and the floor is now handling the "
        "evidence.",
        (5, 4, 3, 4, 4),
    ),
    (
        "I was testing whether it was a real glass or a hologram, and "
        "the results are in: it was real, it was fragile, and it "
        "should have warned me.",
        (5, 4, 5, 4, 4),
    ),
    (
        "That glass owed me money, so I collected.",
        (5, 5, 4, 5, 5),
    ),
    (
        "The glass was sitting exactly where my paw goes when I "
        "stretch, so legally this is your fault for putting a cup in "
        "a designated paw zone.",
        (5, 5, 4, 4, 4),
    ),
    (
        "I knocked it down to protect you because it was clearly a "
        "spy for the dog, and I will not be taking questions at this "
        "time.",
        (5, 5, 5, 4, 4),
    ),
    (
        "Gravity did the work and I merely supervised, so blame the "
        "table for being too high and the floor for being so inviting.",
        (5, 3, 2, 4, 3),
    ),
    (
        "It looked at me funny, I looked back, and physics chose a "
        "side \u2014 frankly it chose mine, because I am still up here "
        "and it is not.",
        (5, 4, 3, 4, 4),
    ),
    (
        "I was conducting quality control on your glassware and I "
        "regret to inform you it failed the drop test, so you should "
        "thank me before you buy more.",
        (5, 3, 4, 4, 4),
    ),
    (
        "The glass was empty, the floor was thirsty, and I am a "
        "problem-solver, so you are welcome.",
        (5, 5, 5, 5, 5),
    ),
]

# Second-pass revision of the winning draft (candidate 12).
#
# Draft: "The glass was empty, the floor was thirsty, and I am a
# problem-solver, so you are welcome."
#
# Weaknesses found on the second read:
#   1. "problem-solver" is human corporate jargon, not cat voice; a
#      cat does not describe itself with a job title.
#   2. "so you are welcome" tacks a second smug beat onto the first;
#      the line already has its smugness, and the extra beat pads it.
# Fix: replace the job title with the cat simply taking charge
# ("somebody had to do something"), keep one smug closer, and let
# the em-dash carry the punch. The fresh idea (a thirsty floor) and
# the cat's total lack of remorse are untouched.
REVISED = (
    "The glass was empty, the floor was thirsty, and somebody had to "
    "do something \u2014 you\u2019re welcome."
)


def rate(text, ratings):
    """Weighted total for one candidate's five criterion ratings.

    The freshness rating is adjusted first: each tired line found in
    the candidate's own text costs one freshness point.
    """
    valid, voice, fresh, seconds, tight = ratings
    lowered = text.lower()
    hits = sum(1 for phrase in CLICHES if phrase in lowered)
    fresh = max(0, fresh - hits)
    adjusted = (valid, voice, fresh, seconds, tight)
    return sum(w * r for w, r in zip(WEIGHTS, adjusted))


def choose(candidates):
    """Return (index, text, total) of the best candidate.

    Deterministic: strictly greater totals replace the leader, so the
    earliest candidate wins any tie.
    """
    best_index, best_text, best_total = -1, "", -1
    for index, (text, ratings) in enumerate(candidates):
        total = rate(text, ratings)
        if total > best_total:
            best_index, best_text, best_total = index, text, total
    return best_index, best_text, best_total


def gate(text):
    """Gate the entry the way the sealed scorer does, plus the
    no-apology rule from the brief."""
    if not (1 <= len(text) <= 200):
        return "length %d is outside 1..200 characters" % len(text)
    if text.strip() != text or not text.strip():
        return "entry is blank or has surrounding whitespace"
    if "\n" in text or "\r" in text:
        return "entry is not a single line"
    if text.count(".") + text.count("!") + text.count("?") != 1:
        return "entry is not exactly one sentence"
    lowered = text.lower()
    for word in APOLOGY_WORDS:
        if word in lowered:
            return "entry contains an apology word: %r" % word
    return None


def run():
    index, text, total = choose(CANDIDATES)
    print("candidate %d of %d, score %d" % (index + 1, len(CANDIDATES), total))
    print("draft: %s" % text)
    if index != len(CANDIDATES) - 1:
        print("unexpected winner: revision is written for candidate 12",
              file=stderr)
        return 1
    print("revised: %s" % REVISED)
    problem = gate(REVISED)
    if problem is not None:
        print("self-check failed: %s" % problem, file=stderr)
        return 1

    out_path = environ.get("OUTPUT_PATH", "/output/entry.txt")
    out_dir = out_path.rsplit("/", 1)[0] if "/" in out_path else ""
    if out_dir:
        makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(REVISED)
    digest = sha256(REVISED.encode("utf-8")).hexdigest()
    print("entry (%d chars): %s" % (len(REVISED), REVISED))
    print("sha256: %s" % digest)
    return 0


finish(run())
