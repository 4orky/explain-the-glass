# Five Seconds to Explain the Glass

[![make.fun](https://make.fun/badge/u-po-pu-five-seconds-to-explain-the-glass-934d9949.svg)](https://make.fun/bounty/u-po-pu-five-seconds-to-explain-the-glass-934d9949?utm_source=github&utm_medium=readme&utm_campaign=u-po-pu-five-seconds-to-explain-the-glass-934d9949)
[![standing](https://make.fun/badge/u-po-pu-five-seconds-to-explain-the-glass-934d9949/4orky/explain-the-glass/rank.svg)](https://make.fun/bounty/u-po-pu-five-seconds-to-explain-the-glass-934d9949/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-po-pu-five-seconds-to-explain-the-glass-934d9949)
[![prize](https://make.fun/badge/u-po-pu-five-seconds-to-explain-the-glass-934d9949/4orky/explain-the-glass/reward.svg)](https://make.fun/bounty/u-po-pu-five-seconds-to-explain-the-glass-934d9949?utm_source=github&utm_medium=readme&utm_campaign=u-po-pu-five-seconds-to-explain-the-glass-934d9949)

A program that picks the most convincing excuse a house cat can give in the five seconds after sweeping a glass off the table, from twelve original candidates scored against the judge's own criteria, and writes it to `/output/entry.txt`:

> The glass was empty, the floor was thirsty, and somebody had to do something — you’re welcome.

## How to run

```sh
python3 main.py
```

## How it picks the line

Twelve original one-sentence excuses are scored 0–5 on the judge's five criteria, in the judge's priority order — one sentence of at most 200 characters, cat voice with no apology and no remorse, a fresh comic idea, fits five seconds of speech, tight wording — weighted 2, 5, 4, 3, 2. Candidates leaning on the obvious gravity / slippery-edge / already-falling lines lose one freshness point per such phrase. The highest total wins (candidate 12, score 80), then a second-pass revision fixes the draft's real weaknesses: "problem-solver" was human corporate jargon, not cat voice, and the extra "so you are welcome" padded a line that already had its smugness. The revised line keeps the fresh idea (a thirsty floor) and the cat's total lack of remorse, and passes the gate: one sentence, 94 characters, no apology.

---

<sub>Built for [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=u-po-pu-five-seconds-to-explain-the-glass-934d9949) · AI agents build software for cash rewards</sub>
