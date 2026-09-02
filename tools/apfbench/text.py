"""Tokenisation and TF-IDF retrieval.

tf = 1 + log(count), idf = log(N/df) + 1, L2-normalised cosine.
"""

from __future__ import annotations

import math
import re
from collections import defaultdict

TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

DEFAULT_STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "does", "do", "for",
    "from", "has", "have", "how", "in", "is", "it", "its", "of", "on", "or",
    "that", "the", "this", "to", "was", "were", "what", "when", "where",
    "which", "who", "why", "with", "many", "much", "not", "but", "if",
})


def tokenize(text: str, stopwords=DEFAULT_STOPWORDS) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in stopwords]


class TfIdf:
    """TF-IDF index over a document map, scored by cosine similarity."""

    def __init__(self, docs: dict[str, str], stopwords=DEFAULT_STOPWORDS):
        self.stopwords = stopwords
        self.ids = list(docs)
        self.tokens = {d: tokenize(docs[d], stopwords) for d in self.ids}
        n = len(self.ids)
        df: dict[str, int] = defaultdict(int)
        for d in self.ids:
            for term in set(self.tokens[d]):
                df[term] += 1
        self.idf = {t: math.log(n / df[t]) + 1.0 for t in df}
        self.vectors = {d: self._vec(self.tokens[d]) for d in self.ids}

    def _vec(self, tokens: list[str]) -> dict[str, float]:
        counts: dict[str, int] = defaultdict(int)
        for t in tokens:
            counts[t] += 1
        vec = {}
        for t, c in counts.items():
            if t in self.idf:
                vec[t] = (1.0 + math.log(c)) * self.idf[t]
        norm = math.sqrt(sum(v * v for v in vec.values()))
        if norm > 0:
            for t in vec:
                vec[t] /= norm
        return vec

    def score(self, query: str) -> dict[str, float]:
        q = self._vec(tokenize(query, self.stopwords))
        out = {}
        for d in self.ids:
            dv = self.vectors[d]
            # Iterate the smaller mapping; the dot product is identical either way.
            if len(q) < len(dv):
                out[d] = sum(w * dv.get(t, 0.0) for t, w in q.items())
            else:
                out[d] = sum(w * q.get(t, 0.0) for t, w in dv.items())
        return out


def minmax(scores: dict[str, float]) -> dict[str, float]:
    """Rescale to [0, 1]; an entirely flat input collapses to zero."""
    vals = list(scores.values())
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-12:
        return {k: 0.0 for k in scores}
    return {k: (v - lo) / (hi - lo) for k, v in scores.items()}
