# Hallucinot 🦖

*For once, AI fixes **human** hallucinations.*

Hallucinot listens to what you say (or reads the tab you're on), finds the relevant piece of your knowledge base, and shows it. When you say something that contradicts the source, it says so in red with the receipt. Every decision is made by **Drex**: should we speak, which document, and does it agree or contradict.

## Run it

```bash
git clone https://github.com/harsh-neubird/hallucinot && cd hallucinot
echo "YOUR_NACE_KEY" > .nace_key      # or: export NACE_API_KEY=...
python3 server.py
```

Then open http://localhost:8787 in **Chrome**. Click **Start listening**, or type a sentence and press Enter.

To use your own knowledge (any folder, any public GitHub repo):

```bash
python3 server.py --folder ~/path/to/docs --repo owner/name
```

- **Folders:** `.md .txt .csv .json .py .js .yaml …` are read directly. PDFs go through `parse_pdf()` in `server.py`; swap in **NDI** there at the event.
- **Repos:** the last ~300 merged PRs are fetched with `gh` and cached in `kb/github/`.
- **Drex key:** read from `NACE_API_KEY` or the `.nace_key` file (git-ignored).

Without flags, the server loads `kb/company/` (fictional "Quokka Analytics" docs) plus the `pallets/flask` PRs.

## Chrome extension (any-tab mode)

1. Start the server (above).
2. Open `chrome://extensions`, turn on **Developer mode**, click **Load unpacked**, and pick the `extension/` folder.
3. Click the Hallucinot toolbar icon to open the side panel. It checks each tab you switch to, or click **Check this page**. Select text on a page to check just that.

Use the mic on the main page at localhost:8787. Inside the side panel, Chrome may block the microphone.

## Demo script

| Say / show | Expected |
|---|---|
| "Why did churn go up in Q3?" | 📄 Q3 metrics: Starter plan price increase |
| "Let's grab lunch after this." | 🤫 stays quiet |
| "We switched redirects to 301." | 🦖 Human hallucination: PR #5898 says 303 |
| "Our SLA with Acme is 99.99 percent uptime." | 🦖 Contract says 99.9% |
| "Acme gets a 10% credit if uptime drops below 99.9%." | ✅ Checks out |
| "We use JWTs for dashboard login." | 🦖 Design doc: session cookies, not JWTs |
| Gmail tab with Raj's email claiming 99.99% / 25% credit | 🦖 Contract clause |
| A random recipe site | 🤫 stays quiet |

## How it works

```
mic (Chrome speech-to-text) or tab text
  → keyword search over the knowledge base → top 12 candidates
  → Drex call 1: what was said (question / claim / other) + which candidate (or none)
  → Drex call 2 (claims only): agree / contradict / unclear vs the chosen source
  → card: blue context · green checks out · red hallucination · amber unsure
```

Typical latency: about 0.3 s per Drex call, 0.6 s for a full fact-check.

## Benchmark (Drex vs Claude)

`eval/cases.py` holds 50 meeting lines labeled against the Flask PRs. The 2026-11-13 run: Drex 47/50 and Claude Opus 5.5 47/50. Drex took a median 0.38 s against 2.2 s for Claude, at roughly 1/500th of the cost. All three misses came from the keyword search, not from either model.
