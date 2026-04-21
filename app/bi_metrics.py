from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


ESTRATO_SCORE = {
    "0 a 5 personas": 5,
    "6 a 10 personas": 10,
    "11 a 30 personas": 20,
    "31 a 50 personas": 35,
    "51 a 100 personas": 50,
    "101 a 250 personas": 75,
    "251 y más personas": 100,
}


@dataclass
class LeadScoringConfig:
    peso_contacto: float = 0.30
    peso_tamanio: float = 0.20
    peso_sector: float = 0.15
    peso_contratos: float = 0.20
    peso_monto: float = 0.15


def _normalize_series(s: pd.Series) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce").fillna(0)
    mx = s.max()
    if mx <= 0:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return s / mx


def calcular_metricas_denue(df_denue: pd.DataFrame) -> pd.DataFrame:
    out = df_denue.copy()

    telefono = out.get("telefono", pd.Series("", index=out.index)).fillna("").astype(str)
    correo = out.get("correo_e", pd.Series("", index=out.index)).fillna("").astype(str)
    web = out.get("sitio_internet", pd.Series("", index=out.index)).fillna("").astype(str)

    out["tiene_telefono"] = telefono.str.len().gt(6)
    out["tiene_email"] = correo.str.contains("@", na=False)
    out["tiene_web"] = web.str.len().gt(5)

    out["score_contacto"] = (
        out["tiene_telefono"].astype(int) * 60
        + out["tiene_email"].astype(int) * 30
        + out["tiene_web"].astype(int) * 10
    )

    estrato = out.get("estrato", pd.Series("", index=out.index)).fillna("")
    out["score_tamanio"] = estrato.map(ESTRATO_SCORE).fillna(0)

    sectores_prioritarios = {
        "Comercio al por mayor": 100,
        "Servicios de consultoría": 95,
        "Servicios de diseño de sistemas de cómputo": 95,
        "Fabricación": 85,
        "Corporativos": 90,
        "Telecomunicaciones": 90,
        "Servicios financieros": 95,
    }

    actividad = out.get("actividad_economica", pd.Series("", index=out.index)).fillna("")
    out["score_sector"] = 30
    for key, points in sectores_prioritarios.items():
        mask = actividad.str.contains(key, case=False, na=False)
        out.loc[mask, "score_sector"] = points

    return out


def consolidar_leads(
    df_denue: pd.DataFrame,
    df_compranet: pd.DataFrame | None = None,
    config: LeadScoringConfig | None = None,
) -> pd.DataFrame:
    config = config or LeadScoringConfig()

    denue = calcular_metricas_denue(df_denue)

    if df_compranet is None or df_compranet.empty:
        denue["num_contratos"] = 0
        denue["monto_total"] = 0.0
    else:
        cnet = df_compranet.copy()
        cnet["razon_social"] = cnet.get("razon_social", "").fillna("").astype(str)
        cnet["monto_contrato"] = pd.to_numeric(cnet.get("monto_contrato", 0), errors="coerce").fillna(0)
        agg = (
            cnet.groupby("razon_social", dropna=False)
            .agg(num_contratos=("razon_social", "count"), monto_total=("monto_contrato", "sum"))
            .reset_index()
        )

        denue["_key"] = denue.get("razon_social", denue.get("nombre", "")).fillna("").astype(str).str.upper().str.replace(r"[^A-Z0-9 ]", "", regex=True)
        agg["_key"] = agg["razon_social"].str.upper().str.replace(r"[^A-Z0-9 ]", "", regex=True)

        denue = denue.merge(agg[["_key", "num_contratos", "monto_total"]], on="_key", how="left")
        denue = denue.drop(columns=["_key"], errors="ignore")
        denue["num_contratos"] = denue["num_contratos"].fillna(0)
        denue["monto_total"] = denue["monto_total"].fillna(0)

    denue["n_contratos_norm"] = _normalize_series(denue["num_contratos"]) * 100
    denue["monto_norm"] = _normalize_series(denue["monto_total"]) * 100

    denue["score_lead"] = (
        denue["score_contacto"] * config.peso_contacto
        + denue["score_tamanio"] * config.peso_tamanio
        + denue["score_sector"] * config.peso_sector
        + denue["n_contratos_norm"] * config.peso_contratos
        + denue["monto_norm"] * config.peso_monto
    ).round(2)

    denue["segmento_lead"] = pd.cut(
        denue["score_lead"],
        bins=[-0.1, 35, 60, 80, 100],
        labels=["Bajo", "Medio", "Alto", "Prioritario"],
    )

    return denue.sort_values("score_lead", ascending=False)


def resumen_bi(df_scored: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "metric": [
                "total_empresas",
                "con_telefono",
                "con_email",
                "score_promedio",
                "prioritarios",
            ],
            "valor": [
                len(df_scored),
                int(df_scored.get("tiene_telefono", pd.Series(dtype=bool)).sum()),
                int(df_scored.get("tiene_email", pd.Series(dtype=bool)).sum()),
                float(df_scored["score_lead"].mean()) if not df_scored.empty else 0.0,
                int((df_scored["segmento_lead"] == "Prioritario").sum()),
            ],
        }
    )


def load_latest_csv(paths: Iterable[Path], pattern: str) -> pd.DataFrame:
    files: list[Path] = []
    for path in paths:
        files.extend(sorted(path.glob(pattern)))
    if not files:
        return pd.DataFrame()
    latest = max(files, key=lambda p: p.stat().st_mtime)
    return pd.read_csv(latest, low_memory=False)
