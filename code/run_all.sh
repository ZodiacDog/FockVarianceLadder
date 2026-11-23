#!/usr/bin/env bash
# Regenerate everything: results -> figures -> documents -> PDFs.
# The protocol builder edits a copy of the v1.0 protocol docx, which is not
# included in this repository. That step is skipped when the source is absent.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-python3}
$PY fvl_verify.py
$PY regen_figures.py
$PY build_paper.py
$PY build_supplement.py
shopt -s nullglob
cands=(../protocol_v1_source.docx ../../9df80a77*.docx)
shopt -u nullglob
if ((${#cands[@]})) && [[ -f "${cands[0]}" ]]; then
  $PY build_protocol.py
else
  echo "Skipping protocol rebuild (v1.0 source docx not present in this tree)."
fi
if command -v soffice >/dev/null; then
  soffice --headless --convert-to pdf --outdir ../pdf ../docs/*.docx >/dev/null
fi
echo "done"
