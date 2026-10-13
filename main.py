"""ReconAI read-only reconciliation API.
Deterministic matching only; no AI models or account modification.
"""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from app.loader import DataQualityError, build_report

ROOT = Path(__file__).resolve().parent
DATA_DIR = Path(
    os.environ.get("RECONAI_DATA_DIR", str(ROOT / "data"))
)

app = FastAPI(
    title="ReconAI — Reconciliation API",
    version="0.1.0",
    description=(
        "Read-only ledger-versus-settlement reconciliation. "
        "Matching decisions use deterministic Python rules."
    ),
)


def get_report():
    """Build the reconciliation report and handle data errors."""
    try:
        report, _ = build_report(DATA_DIR)
        return report
    except DataQualityError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to read reconciliation input files.",
        ) from exc


@app.get("/health")
def health():
    """Return source quality and reconciliation health."""
    report = get_report()

    totals = report.get("control_totals", {})
    reconciled_values = [
        value
        for key, value in totals.items()
        if key.endswith("_reconciled")
    ]

    is_reconciled = (
        bool(reconciled_values)
        and all(value is True for value in reconciled_values)
    )

    return {
        "status": (
            "healthy"
            if report.get("status") == "PASS" and is_reconciled
            else "degraded"
        ),
        "source_rows": report.get("source_rows", {}),
        "valid_rows": report.get("valid_rows", {}),
        "invalid_rows": report.get("invalid_rows", {}),
        "reconciled": is_reconciled,
    }


@app.get("/data-quality")
def data_quality():
    """Return source validation results and control totals."""
    return get_report()


@app.get("/reconciliation")
def reconciliation():
    """Return the deterministic reconciliation report."""
    report = get_report()

    return {
        "status": report.get("status"),
        "control_totals": report.get("control_totals", {}),
        "exceptions": report.get("exceptions", []),
        "approval_required": True,
        "approved_automatically": False,
    }