# Hallucinot: team plan (living doc, edit and push freely)

**Event:** Nace AI Drexathon × Adobe EDU · Sat Nov 14 · build 11:00 → **hard submit 3:00 PM** · finalist demos 3:15 (5 min)
**Pitch:** *Humans hallucinate. AIs hallucinate. Hallucinot catches both, with receipts.* Drex decides on every sentence: speak? which source? true or false?
**Live link:** https://quench-humped-excluding.ngrok-free.dev (runs from Harsh's laptop) · **Repo:** https://github.com/harsh-neubird/hallucinot

Status key: ⬜ todo · 🟨 in progress · ✅ done · ❌ dropped
Add notes or questions under **Updates log** at the bottom (newest first).

---

## ⏰ Check-ins
| Time | What should be true |
|---|---|
| 1:00 | Fix + Cite built · poster PDF tested · NDI info in hand |
| 2:15 | Slides + backup video done · mascots wired in |
| 2:30 | Full rehearsal (timer, 5 min) |
| 2:50 | **Submit** (don't wait for 3:00) |

## 🧑‍💻 Harsh: main demo and Nace judges
| # | Task | Status | Notes |
|---|---|---|---|
| H1 | Ask organizers: is code written before 11:00 OK? | ⬜ | |
| H2 | Ask Nace team how to use **NDI** (endpoint, input, output); paste the answer in the log | ⬜ | |
| H3 | Test mic in real Chrome at localhost:8787 | ⬜ | |
| H4 | Load the extension (`chrome://extensions` → Load unpacked → `extension/`) and test on Gmail/GitHub | ⬜ | |
| H5 | Decide: install c2patool for the "Certify" stamp (yes/no) | ⬜ | |
| H6 | Rehearse the live meeting demo (README demo script) | ⬜ | |
| H7 | Final run-through and submit | ⬜ | |

## 🎨 Mahak: everything Adobe (details in [ADOBE_TASKS.md](ADOBE_TASKS.md))
| # | Task | Status | Notes |
|---|---|---|---|
| M1 | Ask Adobe EDU folks what they judge on; paste the answer in the log | ⬜ | |
| M2 | Student poster "The Cell" in Adobe Express (3 planted mistakes) → PDF → test in app (expect 3 🦖 / 3 ✅) | ⬜ | |
| M3 | Sales flyer in Adobe Express (2 planted mistakes) → PDF → test (expect 2 🦖 / 3 ✅) | ⬜ | |
| M4 | 4 Firefly T-Rex stickers → `ui/img/` (rex-stomp, rex-approve, rex-confused, rex-sleep) | ⬜ | |
| M5 | 6 slides in Adobe Express | ⬜ | |
| M6 | Backup demo video (Express edit + Adobe Podcast audio cleanup) | ⬜ | |

## 🤖 Claude (via Harsh): building
| # | Task | Status | Notes |
|---|---|---|---|
| C1 | **Fix:** each 🦖 shows the correct sentence from the source, with a copy button | ✅ | Drex picks the sentence from the source; nothing is generated |
| C2 | **Cite:** ✅ claims get citations plus a References list | ✅ | "Copy fixed version + citations" button |
| C3 | **Certify:** Content Credentials stamp, verifiable on Adobe's site (needs H5 = yes) | ⬜ | |
| C4 | Wire the T-Rex images into the cards (needs M4) | ⬜ | |
| C5 | Plug in NDI for PDFs (needs H2) | ⬜ | |

## ✅ Already done
- Live mode: mic or typing → Drex decides → 📄 context / ✅ checks out / 🦖 hallucination / 🤫 stays quiet (about 0.3 s per decision)
- **Check a document:** paste text or drop a PDF, every claim checked in about 1 s (poster 3/3 🦖, chatbot answer and customer email caught)
- Workspaces: 🏢 Company (Quokka docs + 298 Flask PRs) and 🎓 Classroom (Bio 101 notes)
- Chrome extension (any-tab side panel), public link with a spend cap, private repo
- Benchmark: Drex 47/50 vs Claude Opus 47/50, 0.38 s vs 2.2 s, about 500× cheaper

## 🎬 Demo order (5 min)
1. Hook (20 s): "Humans hallucinate. AIs hallucinate."
2. Live meeting (1.5 min): question → card · small talk → quiet · 3 wrong claims → 🦖
3. Drex catches Claude (40 s): chatbot answer sample → 🦖
4. Adobe loop (60 s): Mahak's Express poster → 🦖 → Fix → Cite → (Certify)
5. Numbers (40 s) · Close (20 s): "Content Credentials prove who made it. Hallucinot proves it's true."

## ❓ Open questions
- What do the Adobe judges score? (M1)
- How does NDI work? (H2)
- Is pre-11:00 code allowed? (H1)

---

## 📝 Updates log (newest first)
- **11:35 Claude:** Fix + Cite done. Poster: 3 wrong lines replaced with the correct sentences from the notes, plus a References list. Live red cards now show the correct line too. `git pull` to get it.
- **11:20 Harsh:** Plan created. Mahak has repo access. Drex key sent privately (never commit it).
