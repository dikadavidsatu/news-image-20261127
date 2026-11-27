# 27 November in One Frame — The World Today, One Image Edition

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/dikadavidsatu/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/dikadavidsatu/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

An entry for make.fun's **“Sum up 27 November's world news in one image”** bounty ($100 in USDC):
https://make.fun/bounty/news-image-20261127

## The edition

One square image — a broadsheet front page for **Thursday 27 November 2026** — carrying
**33 stories** researched from that day's wire reporting (Reuters, Associated Press,
BBC News, Al Jazeera): Washington's proposed tariffs on 14 trading partners as the lead,
the drone strike that killed two Italian technicians in Kuwait as the second story,
six news sections, five wire datelines, eight one-line briefs, and a “Day in Numbers”
strip (€1.58tn of undecided EU budget, 100+ drones over Ukraine, 10,000+ Ebola cases
in DR Congo, and more).

## How it was made

- `headlines.json` — the day's reporting, structured: lead, second story, six sections
  (Middle East & the Gulf, Europe, Ukraine & Russia, United States, Asia-Pacific,
  Business & Technology), datelines, briefs and the numbers strip, each item credited
  to its wire.
- `render.py` — a Python/PIL compositor that draws the front page at 1024×1024:
  masthead and furniture rules, the lead in large serif type, a halftone-screened
  numbers strip, the section grid and the briefs columns, all on a fine paper grain.
  The layout is measured and auto-scaled so every story fits the square.
- `entry.png` — the finished page, committed to this repository.
- `main.ts` — the program the grader runs. The sandbox mounts the repo read-only,
  so it simply delivers the committed `entry.png` to the output folder
  (`MAKEFUN_OUTPUT_DIR`, else `/output`, else `./output`) — twice, verifying
  length and SHA-256 after each copy, and writing nothing anywhere else.

## The headlines

**Lead — TRADE WAR WIDENS.** *US Proposes New Tariffs on 14 Trading Partners Over
Subsidized Factories.* Washington unveiled a broad new tariff package aimed at China,
the European Union, Brazil, Taiwan and 11 other economies, accusing them of flooding
world markets with subsidized industrial production. Beijing threatened retaliation
within hours. (Reuters · Associated Press)

**Second — THE GULF UNDER FIRE.** *Drone Strike Kills Two Italian Technicians in
Kuwait; Iran Denies Any Role.* Debris from intercepted drones fell on an air-defence
station, killing two Italian radar technicians; an attack on Saudi Aramco's Jazan
refinery the same day killed a Nepali worker and halted some operations.
(Reuters · Associated Press)

**Middle East & the Gulf**

- Attack on Saudi Aramco's Jazan refinery kills a Nepali worker, starts a fire and halts some operations at the 400,000-barrel-a-day plant. (Reuters)
- Israeli strikes kill 10 people across Gaza, hospital officials say, as Hamas weighs its response. (Reuters)
- Saudi airstrikes hit Sanaa overnight as the Houthis and the kingdom trade near-daily blows in Yemen's revived war. (AP)

**Europe**

- EU leaders end a 12-hour Brussels summit deadlocked over the €1.58 trillion 2028–34 budget and a €45 billion loan for Ukraine; talks resume December 17–18. (AP)
- Spain's Pablo Hernández de Cos is chosen to succeed Christine Lagarde as president of the European Central Bank. (Reuters)
- Bank of England to cut capital requirements for UK-focused lenders in a post-crisis rule rethink. (Reuters)

**Ukraine & Russia**

- Russian ballistic missiles and more than 100 drones strike Kyiv and Kharkiv overnight, killing at least three people. (Wire reports)
- Leaked Russian records suggest nearly 500,000 Russian soldiers have died in Ukraine since the 2022 invasion. (Analysis)
- Russia arrests a deputy aerospace commander in a reported corruption case. (Reuters)

**United States**

- Severe weather on both coasts complicates Thanksgiving travel for millions of Americans. (AP)
- Trump uses his Thanksgiving message to lash out at political foes, immigrants and the federal government. (Reuters)
- Trump calls revised GDP figures 'fake' and demands an investigation of the Commerce Department. (AP)

**Asia-Pacific**

- North Korea's Kim Jong Un vows to build more nuclear weapons after ignoring Trump's latest overture. (AP)
- Police fire tear gas to disperse fresh protests by Bangladesh garment workers. (Reuters)
- North Korean launderers turn to little-known crypto services to move the Binance haul, researchers say. (Reuters)

**Business & Technology**

- Altria, the US maker of Marlboro, explores an all-cash bid for Imperial Brands in a possible tobacco carve-up. (Reuters)
- Dutch groups ask a court to halt sales of Meta's smart glasses in the Netherlands over privacy concerns. (Reuters)
- FCC says SpaceX can deploy 1 million satellites for data centres in space; scientists are sceptical. (AP)

**From the wires**

- **KYIV** — Russian missiles and drones struck residential districts overnight; Zelenskyy warns a major attack on the power grid is imminent.
- **KUWAIT CITY** — Intercepted Iranian drones rained debris on an air-defence station, killing two Italian technicians; Iran denies involvement.
- **GAZA CITY** — Five strikes and a shooting killed 10 Palestinians, among them a Hamas official and his wife, hospital officials said.
- **CAIRO** — A fuel tanker crash ignited a massive fire on a highway ringing the capital, killing at least 31 people. (AP)
- **DHAKA** — Police used tear gas against garment workers protesting for the second day over pay and conditions.

**In brief**

- **PARIS** — Gérard Depardieu will face trial for rape, a French court rules. (Reuters)
- **STOCKHOLM** — Sweden's Centre leader backs a right-wing prime minister in a major shift. (Reuters)
- **ANKARA** — Türkiye's elections set for 2028 as the ruling alliance agrees on an Erdoğan candidacy. (Reuters)
- **WARSAW** — Poland's defence ministry to sign an AI decision-support deal with Palantir on Friday. (Reuters)
- **KINSHASA** — Ebola cases in DR Congo pass 10,000 in the fastest-growing outbreak on record. (Wire reports)
- **BAGHDAD** — Iraqi Kurds protest Baghdad's moves to assert central control over their region. (Reuters)
- **WELLINGTON** — Early voting opens in New Zealand's 2026 election, with polls pointing to a tight race. (Wire reports)
- **ALGIERS** — Algeria approves a troop deployment to Niger — its first foreign mission since 1973. (Wire reports)

**The day in numbers:** 14 trading partners in the new US tariff plan · €1.58tn EU
budget left undecided · €45bn Ukraine loan deadlocked · 100+ drones in Russia's
overnight barrage · 31 killed in the Cairo tanker fire · 10 killed in Israeli strikes
on Gaza · 10,000+ Ebola cases in DR Congo · 500,000 Russian troops reported killed
in Ukraine.

*Compiled from wire reports filed 26–27 Nov 2026 — Reuters, Associated Press, BBC News
and Al Jazeera — as of 02:00 UTC, Thursday 27 November 2026.*
