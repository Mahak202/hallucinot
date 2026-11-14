"""Hallucinot: live knowledge cards + fact-checking, decided by Drex.

Run:  python3 server.py [--folder PATH ...] [--repo owner/name ...] [--port 8787]
Open: http://localhost:8787
"""
import argparse, collections, concurrent.futures, json, math, os, re, shutil, subprocess, sys, time, urllib.request
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
DREX_URL = "https://console.nace.ai/v1/systemone"
TEXT_EXT = {".md", ".txt", ".csv", ".json", ".rst", ".py", ".js", ".ts", ".go", ".yaml", ".yml", ".html"}

# ---------------------------------------------------------------- knowledge base
CHUNKS = []  # {id, source, title, text, url, date, kind}


def add_chunk(source, title, text, url="", date="", kind="doc"):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < 20:
        return
    CHUNKS.append({"id": f"c{len(CHUNKS)}", "source": source, "title": title.strip()[:120],
                   "text": text[:1200], "url": url, "date": date, "kind": kind})


def parse_pdf(path):
    """PDF -> text. Replace with NDI at the event (Nace's document parser)."""
    if shutil.which("pdftotext"):
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    return ""


def load_folder(folder):
    n0 = len(CHUNKS)
    for dirpath, _, files in os.walk(folder):
        for f in sorted(files):
            path = os.path.join(dirpath, f)
            ext = os.path.splitext(f)[1].lower()
            rel = os.path.relpath(path, folder)
            if ext == ".pdf":
                text = parse_pdf(path)
            elif ext in TEXT_EXT:
                text = open(path, errors="ignore").read()
            else:
                continue
            if not text.strip():
                continue
            doc_title = (re.search(r"^#\s+(.+)$", text, re.M) or [None, rel])[1]
            # split markdown by headings, else by blank-line paragraphs ~800 chars
            parts = re.split(r"\n(?=#{2,3}\s)", text)
            if len(parts) == 1:
                paras, buf, parts = re.split(r"\n\s*\n", text), "", []
                for p in paras:
                    if len(buf) + len(p) > 800 and buf:
                        parts.append(buf); buf = ""
                    buf += "\n" + p
                if buf: parts.append(buf)
            for p in parts:
                h = re.match(r"#{1,3}\s+(.+)", p.strip())
                section = h.group(1) if h else ""
                body = re.sub(r"^#{1,3}\s+.+\n?", "", p.strip())
                title = f"{doc_title} — {section}" if section and section != doc_title else doc_title
                add_chunk(rel, title, body, url="file://" + path, kind="file")
    print(f"  folder {folder}: {len(CHUNKS)-n0} chunks")


def load_repo(repo, limit=300):
    cache = os.path.join(ROOT, "kb", "github", repo.replace("/", "__") + ".jsonl")
    if not os.path.exists(cache):
        print(f"  fetching merged PRs for {repo} via gh ...")
        out = subprocess.run(["gh", "api", "-X", "GET", f"repos/{repo}/pulls", "-f", "state=closed",
                              "-f", "per_page=100", "--paginate", "--jq",
                              '.[] | select(.merged_at!=null) | {n:.number,t:.title,b:((.body//"")[:600]),m:.merged_at[:10],u:.user.login}'],
                             capture_output=True, text=True)
        lines = out.stdout.strip().splitlines()[:limit]
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        open(cache, "w").write("\n".join(lines) + "\n")
    load_pr_file(cache, repo)


def load_pr_file(path, repo):
    n0 = len(CHUNKS)
    for line in open(path):
        if not line.strip():
            continue
        p = json.loads(line)
        if p["t"].lower().startswith(("bump", "[pre-commit", "merge branch", "release", "build(deps")):
            continue
        add_chunk(f"{repo} PR #{p['n']}", f"PR #{p['n']}: {p['t']}", f"{p['t']}. {p['b']}",
                  url=f"https://github.com/{repo}/pull/{p['n']}", date=p.get("m", ""), kind="pr")
    print(f"  repo {repo}: {len(CHUNKS)-n0} PRs")


# ---------------------------------------------------------------- search (BM25)
STOP = set("the and for this that with now did was still does are can why what someone anyone instead hey our "
           "we thing like right didnt where when there any yet get you your have has had they them their its "
           "it's from but not about into just been will would could should how who which then than also".split())
STOP |= set("yeah yes okay ok um uh so well actually really guys everyone".split())


def _stem(w):
    for suf in ("ing", "ed", "es", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf) and not w.endswith("ss"):
            return w[: -len(suf)]
    return w


tok = lambda s: [_stem(w.strip(".")) for w in re.findall(r"[a-z0-9_.%$]+", s.lower())
                 if len(w.strip(".")) > 1 and w.strip(".") not in STOP]
INDEX = {}


def build_index():
    docs = [tok(c["title"] + " " + c["title"] + " " + c["text"]) for c in CHUNKS]
    df = collections.Counter(w for d in docs for w in set(d))
    INDEX.update(docs=[collections.Counter(d) for d in docs], lens=[len(d) for d in docs], df=df,
                 N=len(docs), avg=sum(map(len, docs)) / max(1, len(docs)))


def search(q, k=12):
    I = INDEX; qs = set(tok(q)); scored = []
    for i, c in enumerate(I["docs"]):
        s = 0.0
        for w in qs:
            if w in c:
                idf = math.log(1 + (I["N"] - I["df"][w] + .5) / (I["df"][w] + .5))
                s += idf * c[w] * 2.2 / (c[w] + 1.2 * (.25 + .75 * I["lens"][i] / I["avg"]))
        if s > 0:
            scored.append((s, i))
    return [CHUNKS[i] for s, i in sorted(scored, reverse=True)[:k]]


# ---------------------------------------------------------------- Drex
KEY = os.environ.get("NACE_API_KEY") or open(os.path.join(ROOT, ".nace_key")).read().strip()


def drex(state, questions):
    body = json.dumps({"model": "drex-latest", "state": state, "questions": questions}).encode()
    req = urllib.request.Request(DREX_URL, data=body, headers={"Authorization": "Bearer " + KEY,
                                                               "Content-Type": "application/json"})
    t = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=30))
    r["_ms"] = round((time.time() - t) * 1000)
    return r


def cand_label(c):
    d = f" ({c['date']})" if c["date"] else ""
    return f"{c['title']}{d}: {c['text'][:220]}"


VERDICT = {"type": "choice",
           "instructions": "Compare the statement with the source. Does the source support it, contradict it, or not say?",
           "criteria": {"agree": "The source supports the statement",
                        "contradict": "The source says something different from the statement",
                        "unclear": "The source does not say either way"}}


def analyze(text, mode="speech", previous=""):
    t0 = time.time()
    text = text.strip()
    if not text:
        return {"show": False}
    query = text if mode == "speech" else text[:4000]
    cands = search(query + " " + previous[-200:] if mode == "speech" else query)
    if not cands:
        return {"show": False, "reason": "no candidates", "total_ms": round((time.time() - t0) * 1000)}
    crit = {c["id"]: cand_label(c) for c in cands}
    crit["none"] = "None of these documents is about it"
    if mode == "speech":
        state = {"earlier_in_conversation": previous[-400:], "speaker_just_said": text}
        qs = {"kind": {"type": "choice",
                       "instructions": "What did the speaker just do?",
                       "criteria": {"question": "Asked a question about the company, customers, numbers, code or past decisions",
                                    "claim": "Stated a fact about the company, customers, numbers, code or past decisions",
                                    "other": "Small talk, logistics, opinions, or anything else"}},
              "doc": {"type": "choice", "instructions": "Which document covers the same topic as what the speaker just said, even if the document disagrees with the speaker? Pick none only if no document is on that topic.",
                      "criteria": crit}}
    else:
        state = {"page_the_user_is_reading": text[:6000]}
        qs = {"useful": {"type": "noul", "instructions": "Would one of the company's internal documents help the user with this page right now?"},
              "doc": {"type": "choice", "instructions": "Which document is most relevant to this page? Pick none if none of them is.",
                      "criteria": crit}}
    r1 = drex(state, qs)
    a = r1["answers"]
    doc_id, doc_conf = a["doc"]["choice"], a["doc"].get("confidence", 0)
    kind = a["kind"]["choice"] if mode == "speech" else ("page" if a["useful"]["noul"] > 0.5 else "other")
    out = {"mode": mode, "text": text[:300], "kind": kind,
           "kind_conf": round(a["kind"].get("confidence", 0), 2) if mode == "speech" else round(a["useful"]["noul"], 2),
           "doc_conf": round(doc_conf, 2), "drex_ms": [r1["_ms"]], "drex_eval_ms": [r1.get("evaluation_time_ms")],
           "candidates": len(cands)}
    show = kind != "other" and doc_id != "none" and doc_conf >= 0.4
    out["show"] = show
    if not show:
        out["total_ms"] = round((time.time() - t0) * 1000)
        return out
    doc = next(c for c in cands if c["id"] == doc_id)
    out["doc"] = doc
    out["verdict"] = None
    if kind in ("claim", "page"):
        statement = text if mode == "speech" else text[:3000]
        r2 = drex({"statement": statement, "source": f"{doc['title']}: {doc['text']}"}, {"v": VERDICT})
        v = r2["answers"]["v"]
        out["verdict"], out["verdict_conf"] = v["choice"], round(v.get("confidence", 0), 2)
        out["drex_ms"].append(r2["_ms"]); out["drex_eval_ms"].append(r2.get("evaluation_time_ms"))
        if mode == "page" and v["choice"] != "contradict":
            out["verdict"] = None  # on pages, only speak up for contradictions; otherwise just show context
    out["total_ms"] = round((time.time() - t0) * 1000)
    return out


# ---------------------------------------------------------------- HTTP
STATS = {"decisions": 0, "cards": 0, "ms": []}
# guardrails for when the app is exposed publicly (e.g. via ngrok): caps Drex spend
RATE = collections.defaultdict(list)
PER_IP_PER_MIN = int(os.environ.get("HALLUCINOT_PER_IP_PER_MIN", 30))
MAX_DECISIONS = int(os.environ.get("HALLUCINOT_MAX_DECISIONS", 3000))


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self._send(204, b"")

    def do_GET(self):
        if self.path.startswith("/api/kb"):
            by = collections.Counter(c["kind"] for c in CHUNKS)
            return self._send(200, {"chunks": len(CHUNKS), "by_kind": by,
                                    "sources": sorted({c["source"].split(" PR #")[0] for c in CHUNKS})[:50], "stats": STATS})
        path = self.path.split("?")[0]
        f = os.path.join(ROOT, "ui", "index.html" if path in ("/", "") else path.lstrip("/"))
        if os.path.isfile(f) and os.path.realpath(f).startswith(os.path.join(ROOT, "ui")):
            ctype = {"html": "text/html", "js": "text/javascript", "css": "text/css", "png": "image/png",
                     "svg": "image/svg+xml"}.get(f.rsplit(".", 1)[-1], "application/octet-stream")
            return self._send(200, open(f, "rb").read(), ctype)
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/analyze":
            return self._send(404, {"error": "not found"})
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()
        now = time.time()
        hits = [t for t in RATE[ip] if now - t < 60]
        RATE[ip] = hits + [now]
        if len(hits) >= PER_IP_PER_MIN or STATS["decisions"] >= MAX_DECISIONS:
            return self._send(429, {"error": "Slow down: demo rate limit reached"})
        try:
            res = analyze(body.get("text", ""), body.get("mode", "speech"), body.get("previous", ""))
        except Exception as e:  # keep the demo alive
            return self._send(500, {"error": str(e)})
        STATS["decisions"] += 1; STATS["cards"] += bool(res.get("show"))
        if res.get("drex_ms"): STATS["ms"] = (STATS["ms"] + res["drex_ms"])[-200:]
        self._send(200, res)

    def do_HEAD(self):
        self._send(200, b"", "text/html")

    def log_message(self, fmt, *args):
        if args and "/api/analyze" in str(args[0]):
            sys.stderr.write("%s\n" % (fmt % args))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", action="append", help="folder of files to index (repeatable)")
    ap.add_argument("--repo", action="append", help="GitHub repo owner/name to index PRs from (repeatable)")
    ap.add_argument("--port", type=int, default=8787)
    args = ap.parse_args()
    print("Building knowledge base:")
    for f in args.folder or [os.path.join(ROOT, "kb", "company")]:
        load_folder(os.path.expanduser(f))
    repos = args.repo or []
    if not repos and os.path.exists(os.path.join(ROOT, "kb", "github", "flask_prs.jsonl")):
        load_pr_file(os.path.join(ROOT, "kb", "github", "flask_prs.jsonl"), "pallets/flask")
    for r in repos:
        load_repo(r)
    build_index()
    print(f"Ready: {len(CHUNKS)} chunks. Open http://localhost:{args.port}")
    ThreadingHTTPServer(("127.0.0.1", args.port), H).serve_forever()
