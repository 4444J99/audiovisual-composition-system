"""One-shot Textport readback. No node edits, cooking, saving, or media reads.

Run inside the already-open TouchDesigner session, using the command provided
with this file. Findings stay in this workspace's ignored .agents directory.
"""


def inspect_session(td):
    import json
    import os
    from datetime import datetime, timezone
    from pathlib import Path

    workspace = Path("/Users/4jp/Workspace/audiovisual-composition-system")
    expected = workspace / "audiovisual-sampler-01.toe"
    actual = Path(td.project.folder) / td.project.name
    if actual.resolve() != expected.resolve():
        raise RuntimeError("Inspection refused: the open project is not " + str(expected))

    root = td.op("/")
    dirty_before = root.dirty
    excluded = {"/sys", "/ui", "/local"}
    roots = [node for node in root.children if node.path not in excluded]
    nodes, pending = [], list(roots)
    while pending:
        node = pending.pop()
        nodes.append(node)
        if node.isCOMP:
            pending.extend(node.children)

    report = {
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "project": {"path": str(actual), "version": str(td.app.version),
                    "build": str(td.app.build), "dirty_before": dirty_before},
        "scope": {"roots": [node.path for node in roots],
                  "excluded_system_roots": sorted(excluded),
                  "node_count": len(nodes)},
        "networks": [{"path": node.path, "type": node.OPType,
                      "children": len(node.children)} for node in nodes if node.isCOMP],
        "sources": [], "audio_routing": [], "missing_media": [],
        "errors": [], "inspection_issues": [],
        "playback": "Not tested; a read-only snapshot does not prove playback.",
    }

    def parameters(node, names):
        values = {}
        for name in names:
            par = getattr(node.par, name, None)
            if par is None:
                continue
            # Reading constant values avoids executing user expressions or exports.
            if str(par.mode).split(".")[-1].upper() != "CONSTANT":
                values[name] = {"mode": str(par.mode), "status": "not evaluated"}
                report["inspection_issues"].append(
                    {"path": node.path, "parameter": name,
                     "reason": "Dynamic parameter left unevaluated to preserve session."})
                continue
            values[name] = par.val
        return values

    for node in sorted(nodes, key=lambda item: item.path):
        kind = node.OPType
        source = (node.isTOP and (not node.inputs or kind == "moviefileinTOP"))
        audio = node.isCHOP
        if source or audio:
            names = ("file", "play", "playmode", "speed", "active", "volume",
                     "device", "driver", "outputs", "moviefileintop", "chops")
            values = parameters(node, names)
            entry = {"path": node.path, "type": kind, "parameters": values,
                     "inputs": [item.path for item in node.inputs],
                     "outputs": [item.path for item in node.outputs]}
            if source:
                report["sources"].append(entry)
            if audio:
                report["audio_routing"].append(entry)
            # Only check file-source paths, never output targets or media contents.
            if kind in {"moviefileinTOP", "audiofileinCHOP", "audioplayCHOP"}:
                media = values.get("file")
                if isinstance(media, str) and media:
                    expanded = td.tdu.expandPath(media)
                    if "://" in expanded:
                        entry["media"] = {"path": expanded, "status": "URL not accessed"}
                    else:
                        path = Path(expanded).expanduser()
                        if not path.is_absolute():
                            path = Path(td.project.folder) / path
                        exists = path.exists()
                        entry["media"] = {"path": str(path), "exists": exists}
                        if not exists:
                            report["missing_media"].append(
                                {"node": node.path, "path": str(path)})
                elif media == "":
                    entry["media"] = {"status": "No file assigned"}
        for method in ("errors", "warnings", "scriptErrors"):
            message = getattr(node, method)(recurse=False)
            if message:
                report["errors"].append(
                    {"path": node.path, "kind": method, "message": message})

    report["project"]["dirty_after"] = root.dirty
    report["status"] = "complete" if not report["inspection_issues"] else "partial"
    destination = workspace / ".agents" / "touchdesigner-inspection"
    destination.mkdir(mode=0o700, parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = destination / ("session-" + stamp + ".json")
    fd = os.open(str(output), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    print("TouchDesigner session inspection written to " + str(output))


inspect_session(__import__("td"))
