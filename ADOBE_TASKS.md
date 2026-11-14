# Adobe tasks (Mahak): end to end

Goal: win **"Best Use of Adobe"** by making Adobe part of the product, not just the slides.
The story: *"Content Credentials prove who made it. Hallucinot proves what it says is true."*
**Hard deadline: 3:00 PM submission. Aim to have everything done by 2:15.**

## 0. Setup (10 min)
```bash
git clone https://github.com/harsh-neubird/hallucinot && cd hallucinot
echo "<Drex key from Harsh>" > .nace_key
python3 server.py
```
Open http://localhost:8787 in Chrome (or use the public link Harsh shares).
**Ask the Adobe EDU folks at the venue:** what do they judge on (use inside the product? classroom impact? which tools)?

## 1. Student poster in Adobe Express (20 min) ⭐ most important
Make a school poster titled **"The Cell"** (any template, make it look good). Use exactly these lines:

- By Jamie, Bio 101
- Mitochondria produce most of the cell's ATP. ✅ correct
- Mitochondria are only found in plant cells. ❌ wrong on purpose
- DNA is shaped like a triple helix. ❌ wrong on purpose
- Humans have 48 chromosomes in each body cell. ❌ wrong on purpose
- Plant cells have a cell wall made of cellulose. ✅ correct
- Ribosomes build proteins. ✅ correct

**Export as PDF** (Share → Download → PDF). An image (PNG/JPG) won't work, because the text has to stay readable.
**Test:** in the app, open **📄 Check a document**, set Knowledge to **🎓 Classroom**, drop the PDF, then click **Check every claim**.
Expected: 🦖 3 hallucinations and ✅ 3 checked out. If anything comes out different, screenshot it and send it to Harsh.

## 2. Sales one-pager in Adobe Express (15 min)
A marketing flyer for **"Quokka Analytics: Growth plan"** with these lines:
- $48,000 per year, billed annually. ✅
- 99.99% uptime guarantee. ❌ (the contract says 99.9%)
- Single sign-on (SSO) included on every plan. ❌ (Enterprise only)
- 10% service credit if we miss our uptime target. ✅
- Your data is kept for 13 months. ✅

Export it as PDF, then test with Knowledge set to **🏢 Company**. Expected: 🦖 2 hallucinations and ✅ 3 checked out.

## 3. Fact-Rex mascot in Adobe Firefly (25 min)
Generate **4 images** of the same cute cartoon T-Rex (consistent style, square, transparent or plain background):

| File name | Firefly prompt idea | Used when |
|---|---|---|
| `rex-stomp.png` | cartoon T-Rex angrily stomping on a piece of paper with a red X, sticker style | 🦖 hallucination caught |
| `rex-approve.png` | same cartoon T-Rex giving a thumbs up with a green check mark, sticker style | ✅ checks out |
| `rex-confused.png` | same cartoon T-Rex scratching its head with a yellow question mark, sticker style | 🟡 no source |
| `rex-sleep.png` | same cartoon T-Rex napping peacefully, sticker style | 🤫 stayed quiet |

Put them in `ui/img/` and push (or send them to Harsh), and he'll wire them into the cards.
Optional: a **logo**, a T-Rex holding a magnifying glass, with the word "Hallucinot".

## 4. Pitch slides in Adobe Express (30 min)
Six slides max. Use the Firefly T-Rex art.
1. **Hook:** "Humans hallucinate. AIs hallucinate. Hallucinot catches both."
2. **Problem:** wrong facts in meetings, sales emails, chatbots, and student work (ChatGPT makes things up).
3. **How it works:** knowledge (docs, GitHub, course notes) → Drex decides: speak? which source? true or false? → card with receipts.
4. **Classroom:** a screenshot of the student poster check (3 🦖 caught), with the line "Teaches students to cite, helps teachers grade."
5. **Numbers:** Drex vs Claude Opus: same accuracy (47/50), 6× faster (0.38 s vs 2.2 s), 500× cheaper.
6. **Close:** "Content Credentials prove who made it. Hallucinot proves it's true." Plus the team names.

## 5. Backup demo video (30 min, after Harsh's live demo works)
- Screen-record a good run: the live meeting, then the poster check, then the sales flyer check.
- Edit it in **Adobe Express** (trim it, add captions, 2 minutes max).
- Clean the audio with **Adobe Podcast "Enhance Speech"** (free, podcast.adobe.com).
- Keep it on the laptop desktop in case the venue Wi-Fi fails.

## 6. Stretch: only if the Adobe folks say it's quick
Ask whether an **Adobe Express add-on** could run the check inside Express. If they say it's easy, tell Harsh before 1:30.

## Checklist
- [ ] Asked Adobe judges what they score
- [ ] Student poster PDF works (3 🦖 / 3 ✅)
- [ ] Sales flyer PDF works (2 🦖 / 3 ✅)
- [ ] 4 Firefly T-Rex images in `ui/img/`
- [ ] Slides done
- [ ] Backup video saved
