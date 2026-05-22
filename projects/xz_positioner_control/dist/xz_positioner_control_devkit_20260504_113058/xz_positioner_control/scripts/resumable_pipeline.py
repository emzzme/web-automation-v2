from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from xz_control_ui.icd import parse_icd, save_icd_snapshot


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run_step(step: str, root: Path, icd_path: Path | None) -> str:
    if step == "validate_workspace":
        (root / "state").mkdir(exist_ok=True)
        return "workspace_ok"

    if step == "parse_icd_if_present":
        if icd_path and icd_path.exists():
            bundle = parse_icd(icd_path)
            save_icd_snapshot(bundle, root / "state" / "icd_snapshot.json")
            return f"icd_parsed:{len(bundle.found_tokens)}_tokens"
        return "icd_skipped"

    if step == "generate_connection_map":
        src = root / "config" / "activation.json"
        dst = root / "state" / "active_connections.json"
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        return "connection_map_ready"

    if step == "generate_or_update_code":
        return "code_stage_external_claude"

    if step == "run_local_checks":
        return "checks_placeholder"

    if step == "build_exe":
        return "build_stage_ready"

    return "unknown_step"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--icd", default="")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    icd_path = Path(args.icd).resolve() if args.icd else None

    pipeline = _load_json(root / "config" / "claude_pipeline.json")["pipeline"]
    state_path = root / "state" / "pipeline_state.json"

    if state_path.exists():
        state = _load_json(state_path)
    else:
        state = {"completed": [], "events": []}

    for step in pipeline:
        if step in state["completed"]:
            continue
        result = run_step(step, root, icd_path)
        state["completed"].append(step)
        state["events"].append(
            {"step": step, "result": result, "at": datetime.now(UTC).isoformat()}
        )
        _save_json(state_path, state)

        # Token yenilenmesi veya oturum kesilmesi durumunda bu dosya sayesinde devam edilir.

    print("Pipeline completed.")


if __name__ == "__main__":
    main()
