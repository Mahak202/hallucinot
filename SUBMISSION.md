# Submission draft (review before 2:50)

Fill the form at nace.ai/drexathon/submit with this. Adjust the wording to match the form's fields.

**Project name:** Hallucinot

**One-liner:** For once, AI fixes *human* hallucinations: a team of Drex agents fact-checks every sentence of a meeting, document or chatbot answer against your company's real sources, in under a second.

**Track:** Swarm Intelligence (multi-agent). It also covers Apex Predator, with Drex vs Claude Opus benchmark numbers.

**Team:** Harsh, Mahak

**Repo:** https://github.com/harsh-neubird/hallucinot (make it public before submitting)

**Demo:** live at the ngrok link while the laptop is on; backup video in the presentation

**What it does:**
- **Live meetings:** mic → speech-to-text → a Drex router plus parallel agents on every sentence: Fact checker, Suggest, Policy guards (auto-created from rules found in your documents), Action items, Leak guard, Decision recorder, and custom agents written in plain English. When agents disagree, a third Drex call arbitrates (negotiation).
- **Learns with no clicks:** remembers decisions announced in the meeting, warns when a later statement contradicts them ("this changed today, the doc may be outdated"), and learns from self-corrections.
- **Check any document:** chatbot answers, emails, sales flyers, student posters. Each claim is marked hallucination / checks out / no source, with **Fix** (the correct sentence, picked from the source) and **Cite** (references).
- **Chrome extension:** checks the tab you're on.
- **After the meeting:** a recap goes to Slack with a hand-off to @Intern for the action items.

**How we used Nace:**
- **Drex:** every decision. The router, each agent, verdicts (agree / contradict / unclear), fix selection, negotiation, decision and correction detection. Typically 0.3–0.6 s per decision.
- **NDI (Perception API):** parses uploaded PDFs, images (OCR, for example Adobe Express exports), Word and PowerPoint into the knowledge base; rules found in them become new agents.
- **Intern:** the meeting recap and action items are handed to @Intern in Slack for follow-up.
- **Partners:** Adobe Express / Firefly (classroom poster, slides, mascot); DeepInfra as the "System 2" recap writer (template fallback if unavailable).

**Benchmark (Track 1 evidence):** 50 meeting lines against 300 real pallets/flask PRs: Drex 47/50 vs Claude Opus 5.5 47/50. Median 0.38 s vs 2.2 s, about 500× cheaper per decision. All misses came from the keyword search step, not the model. When the right source wasn't among the candidates, Drex mostly answered "none"; Claude picked a wrong PR.

**Honest limits:** demo data is fictional (Quokka Analytics, Bio 101 notes) plus a public repo. Retrieval is keyword-based. Learning happens in memory per session.
