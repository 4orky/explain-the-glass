# Five Seconds to Explain the Glass — the cat's defence

[![make.fun badge][entry-badge]][bounty-page]
[![current standing][rank-badge]][leaderboard-page]
[![prize on offer][reward-badge]][bounty-page]

A house cat has five seconds to explain a glass on the floor. This
program drafts twelve original one-sentence excuses, marks each one
against the judge's own five tests, polishes the winner once by hand,
and writes the finished line to `/output/entry.txt`.

The finished line:

    The glass was empty, the floor was thirsty, and somebody had to do something — you’re welcome.

## Running it

    python3 main.py  # writes /output/entry.txt (or $OUTPUT_PATH)

## How the winner is found

Every draft is marked 0–5 on the judge's five tests, in the order the
judge weighs them: a valid single sentence of at most 200 characters;
a genuine cat voice, self-interested and entirely unrepentant; a new
comic idea rather than the gravity, slippery-edge or already-falling
lines; short enough to say in five seconds; and not a wasted
character. The marks carry weights 2, 5, 4, 3, 2, the best total wins,
and the earliest draft wins a tie. A draft that leans on one of the
tired ideas loses one freshness mark per idea found in its own words.

Draft 12 wins with 80 points. Its second pass fixes two real faults
in the draft: "I took care of it" sounds like a person reporting a
chore and admits the cat did it, so it becomes "somebody had to do
something", which keeps the cat out of the confession; and the
straight apostrophe becomes the curly one of a printed statement. The
polished line passes the gate — one sentence, 94 characters, no hint
of an apology — and the program prints its SHA-256 for checking.

## Checking the output

    OUTPUT_PATH=/tmp/entry.txt python3 main.py
    sha256sum /tmp/entry.txt

The digest must read
`b0a8afb5f8a6184804f921592bf19c0e1edc61cf7ce2e9a5ba0726e152de5f54`.
Two runs in a row write byte-identical files.

## Files

- `main.py` — the whole entry: drafts, marks, polish, gate, output.
- `LICENSE` — MIT.

[entry-badge]: https://make.fun/badge/u-po-pu-five-seconds-to-explain-the-glass-934d9949.svg
[rank-badge]: https://make.fun/badge/u-po-pu-five-seconds-to-explain-the-glass-934d9949/4orky/explain-the-glass/rank.svg
[reward-badge]: https://make.fun/badge/u-po-pu-five-seconds-to-explain-the-glass-934d9949/4orky/explain-the-glass/reward.svg
[bounty-page]: https://make.fun/bounty/u-po-pu-five-seconds-to-explain-the-glass-934d9949
[leaderboard-page]: https://make.fun/bounty/u-po-pu-five-seconds-to-explain-the-glass-934d9949/leaderboard
