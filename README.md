# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/anirhfx/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/anirhfx/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Sum up 21 November's world news in one image: a program that draws a
newspaper front page for Saturday 21 November 2026 — Trump telling Europe
to stop funding Ukraine after his Putin summit, COP31 running into
Saturday overtime in Antalya, the AI-led market rout (worst week since
2020), Russian missiles hitting Kyiv and Kryvyi Rih and breaching Polish
airspace, Trump weighing new Iran strikes as tankers hit mines at Hormuz,
and the day's other headlines — as a single deterministic 1024×1024 PNG.

## Run it

```sh
python3 main.py
```

Writes `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
Pure Python standard library: no network, no fonts, no third-party
packages. The rasterizer, the 5×7 bitmap font and the PNG encoder are all
in `main.py`, so two runs write byte-identical output.

## What's in the picture

- **Lead story:** Trump tells Europe to stop funding Ukraine after his
  summit with Putin; Xi backs a ceasefire pact and nuclear-safety talks.
- **COP31, Antalya:** talks run into Saturday overtime — EU says "no deal
  or a good deal"; the draft drops fossil-fuel language and a $120bn
  finance target.
- **Markets:** worst week since 2020 — S&P 500 −3.7%, Nikkei −5.1%,
  Nasdaq −5.3%; Nvidia falls 14% as the SEC examines its books.
- **War:** Russian missiles hit Kyiv and Kryvyi Rih (2 killed, 60 hurt);
  missiles and a drone cross into Polish airspace.
- **The Gulf:** Trump weighs new strikes on Iran; Tehran says it fired on
  a US F-16; two tankers hit mines near Hormuz.
- **Also today:** Sinaloa violence after the "El Chapo Isidro" capture,
  mosquitoes cutting dengue by 69% in Brazil, BepiColombo reaching
  Mercury, the EU–UK landmark deal, UN talks on limiting AI weapons,
  Somalia expelling the UAE envoy, and France's police-shootings law.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
