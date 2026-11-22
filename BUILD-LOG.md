# BUILD LOG — news-image-20261121

## What was built
- `main.py` — pure Python 3 standard-library program (no network, no fonts,
  no third-party packages). Draws a newspaper front page for Saturday
  21 November 2026 as a 1024×1024 PNG: hand-written Canvas rasterizer,
  5×7 bitmap font, PNG encoder (zlib level 9, filter-0 rows, no timestamps)
  and small editorial illustrations (US/China/Russia flags, slashed AID
  coin, overtime clock, falling market chart, missile burst, Hormuz tanker
  and mine) all in the one file. Every file in this repo was written with
  the file tools in this session; nothing was copied in from outside the
  repo (the kit was only read for its RULES.txt).
- `LICENSE` — MIT, Ani Rohani (SPDX-License-Identifier: MIT).
- `README.md` — with the three make.fun badges for this bounty.
- `.makefun/owner.json` — owner anirhfx (no wallet address added).
- `.gitignore` — out/, __pycache__/.

## News research (2026-11-22 ~05:30 WIB, web search)
Stories verified across same-day briefs and wires (One Turn daily brief,
Reuters via KTWB, NYT, Telegraph, BBC via Broadcast Prism, AP):
1. Trump tells European leaders to withhold funding from Ukraine after
   his summit with Putin; Xi backs a ceasefire pact and nuclear-safety
   negotiations; Europe calls for a winter ceasefire and postwar troops.
2. COP31 Antalya runs into Saturday overtime; EU "good deal or no deal";
   draft drops fossil-fuel language and a $120bn adaptation finance
   target; talks 21+ hours over time.
3. Markets: worst week since 2020 — S&P 500 -3.7%, Nikkei -5.1%,
   Nasdaq -5.3%; Nvidia -14% as the SEC examines its books; Anthropic
   -8.5% a day after its record $81bn debut.
4. Russian missiles hit Kyiv and Kryvyi Rih (2 killed, 60 hurt in
   Zelensky's home city); missiles and a drone cross into Polish airspace.
5. Trump weighs new strikes on Iran; Tehran says it fired on a US F-16
   in the Gulf; two oil tankers hit mines near the Strait of Hormuz.
6. Also today: Sinaloa violence after the "El Chapo Isidro" capture;
   mosquitoes cut dengue cases 69% in a Brazil trial; BepiColombo reaches
   Mercury orbit after eight years; EU–UK landmark post-Brexit deal; UN
   talks agree to keep working on rules to limit AI weapons; Somalia
   expels the UAE envoy; France passes its police-shootings law.

## Tests (2026-11-22 ~05:35 WIB)
- Ran twice with different MAKEFUN_OUTPUT_DIR: `cmp` identical,
  sha256 `25794027614392c55ba0736bd3a67a5baa93504ce5c3cd09903c5dd847bbca4a`.
- Size: 26,284 bytes (limit 1 MiB). Dimensions: 1024×1024 RGB (limit
  1024×1024). Verified with Pillow; IHDR (1024, 1024, 8, 2, 0, 0, 0).
- Grader-style run `python3 -P -s main.py` with default `/output`:
  wrote `/output/entry.png`, exit 0, same sha256.
- Visual check: rendered image viewed; fixed one real bug (lowercase
  letters rendered blank because the font is uppercase-only — `text()`
  now uppercases input) and re-tested identical. No text overflows
  remain; all six footer items fit above the bottom rule.
- `python3 -m py_compile main.py`: OK.

## Not done (out of scope for this task)
- No submission, no GitHub repo created, no push, no login, no wallet
  touched, no money spent. The repo is local-only; the parent agent
  handles submission.
