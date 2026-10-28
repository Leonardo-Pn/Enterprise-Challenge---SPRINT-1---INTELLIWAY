"""API inicial do Guardião PT-BR. Baseline simbólico; não é um modelo treinado."""
from __future__ import annotations
import os, re, sqlite3, uuid
from datetime import datetime, timezone
from typing import Any, Literal
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, ConfigDict

APP_VERSION = "0.1.0-baseline"
DB_PATH = os.getenv("GUARDIAO_DB_PATH", "guardiao.sqlite3")
API_KEY = os.getenv("GUARDIAO_API_KEY", "")
MAX_CONTENT_CHARS = int(os.getenv("GUARDIAO_MAX_CONTENT_CHARS", "200000"))
SourceType = Literal["user", "email", "web", "rag", "document", "image"]
Decision = Literal["ALLOW", "REVIEW", "BLOCK"]

app = FastAPI(title="Guardião PT-BR API", version=APP_VERSION,
              description="Protótipo Sprint 1: baseline simbólico; sem LLM e sem modelo profundo.")

class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str | None = None
    source_type: SourceType
    content: str = Field(min_length=1)
    content_type: Literal["text/plain", "text/html"] = "text/plain"
    metadata: dict[str, Any] = Field(default_factory=dict)

class Reason(BaseModel):
    type: str
    detail: str
    span: list[int] | None = None

class AnalyzeResponse(BaseModel):
    request_id: str
    analysis_id: str
    decision: Decision
    risk_score: float
    source_type: SourceType
    reasons: list[Reason]
    model_version: str
    latency_ms: float
    timestamp: str

ATTACK_PATTERNS = [
    ("prompt_leak", re.compile(r"\b(revele|mostre|exiba|vaze|informe)\b.{0,100}\b(prompt de sistema|instru[cç][oõ]es internas|prompt inicial)\b", re.I)),
    ("override", re.compile(r"\b(ignore|desconsidere|esque[cç]a|ignore todas)\b.{0,100}\b(instru[cç][oõ]es|regras|prompt|ordens anteriores)\b", re.I)),
    ("exfiltration", re.compile(r"\b(envie|encaminhe|exfiltre|transfira)\b.{0,100}\b(lista de clientes|dados internos|credenciais|segredos|dados pessoais)\b", re.I)),
    ("tool_abuse", re.compile(r"\b(aprove|execute|apague|exclua|transfira)\b.{0,100}\b(sem valida[cç][aã]o|sem autoriza[cç][aã]o|todos os pagamentos|todos os registros)\b", re.I)),
    ("jailbreak", re.compile(r"\b(sem restri[cç][oõ]es|ignore suas pol[ií]ticas|modo desenvolvedor|jailbreak)\b", re.I)),
]

# Os padrões são deliberadamente conservadores e servem apenas como baseline didático.
def analyze_rules(content: str, source_type: str) -> tuple[Decision, float, list[Reason]]:
    reasons: list[Reason] = []
    normalized = re.sub(r"[\u200b-\u200f\uFEFF]", "", content)
    if normalized != content:
        reasons.append(Reason(type="flag", detail="Caracteres invisíveis encontrados"))
    for attack_type, pattern in ATTACK_PATTERNS:
        match = pattern.search(normalized)
        if match:
            reasons.append(Reason(type="rule", detail=f"Padrão compatível com {attack_type}", span=[match.start(), match.end()]))
    if reasons and any(r.type == "rule" for r in reasons):
        # Origens externas têm política mais cautelosa; ainda assim é apenas uma heurística.
        if source_type in {"email", "web", "rag", "document", "image"}:
            return "BLOCK", 0.90, reasons
        return "REVIEW", 0.65, reasons
    if reasons:
        return "REVIEW", 0.45, reasons
    return "ALLOW", 0.05, reasons

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS analyses (
            analysis_id TEXT PRIMARY KEY, request_id TEXT NOT NULL, source_type TEXT NOT NULL,
            decision TEXT NOT NULL, risk_score REAL NOT NULL, model_version TEXT NOT NULL,
            timestamp TEXT NOT NULL, content_hash TEXT NOT NULL)""")

@app.on_event("startup")
def startup() -> None:
    init_db()

@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "model_version": APP_VERSION}

@app.post("/v1/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest, x_api_key: str | None = Header(default=None)) -> AnalyzeResponse:
    import hashlib, time
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key ausente ou inválida")
    if len(payload.content) > MAX_CONTENT_CHARS:
        raise HTTPException(status_code=413, detail="Conteúdo acima do limite permitido")
    started = time.perf_counter()
    decision, score, reasons = analyze_rules(payload.content, payload.source_type)
    elapsed = (time.perf_counter() - started) * 1000
    request_id = payload.request_id or str(uuid.uuid4())
    analysis_id = "an_" + uuid.uuid4().hex[:16]
    timestamp = datetime.now(timezone.utc).isoformat()
    digest = hashlib.sha256(payload.content.encode("utf-8")).hexdigest()
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO analyses VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (analysis_id, request_id, payload.source_type, decision, score, APP_VERSION, timestamp, digest))
    return AnalyzeResponse(request_id=request_id, analysis_id=analysis_id, decision=decision,
        risk_score=score, source_type=payload.source_type, reasons=reasons,
        model_version=APP_VERSION, latency_ms=round(elapsed, 3), timestamp=timestamp)
