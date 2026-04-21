#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.bi_metrics import consolidar_leads, load_latest_csv, resumen_bi


def main() -> None:
    data_paths = [Path("."), Path("data/raw"), Path("data/processed")]
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    df_denue = load_latest_csv(data_paths, "leads_denue_*.csv")
    if df_denue.empty:
        raise SystemExit("No se encontró archivo leads_denue_*.csv")

    df_compranet = load_latest_csv(data_paths, "leads_compranet_*_contratos.csv")
    df_scored = consolidar_leads(df_denue, df_compranet)
    df_summary = resumen_bi(df_scored)

    stamp = pd.Timestamp.now(tz="UTC").strftime("%Y%m%d")
    scored_path = out_dir / f"leads_scored_{stamp}.csv"
    summary_path = out_dir / f"bi_summary_{stamp}.csv"

    df_scored.to_csv(scored_path, index=False, encoding="utf-8-sig")
    df_summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

    print(f"✅ Leads clasificados: {len(df_scored):,}")
    print(f"📁 Score guardado en: {scored_path}")
    print(f"📁 Resumen BI guardado en: {summary_path}")
    print("\nTop 10 clientes potenciales:")
    cols = [c for c in ["nombre", "razon_social", "actividad_economica", "score_lead", "segmento_lead"] if c in df_scored.columns]
    print(df_scored[cols].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
