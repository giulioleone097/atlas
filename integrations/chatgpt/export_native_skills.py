#!/usr/bin/env python3
"""Export Atlas and Spotter as independently uploadable native skills."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile


EXPORT_MARKER = b"generated; do not edit\n"


def has_export_marker(path: Path) -> bool:
    """Return whether a regular marker belongs to this exporter."""

    try:
        return path.is_file() and not path.is_symlink() and path.read_bytes() == EXPORT_MARKER
    except OSError:
        return False


def bundle_files(bundle: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path in sorted(bundle.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"export contains a symlink: {path}")
        if path.is_file():
            files[path.relative_to(bundle).as_posix()] = path.read_bytes()
    return files


def archive_files(archive: Path) -> dict[str, bytes]:
    with ZipFile(archive) as zip_file:
        names = [entry.filename for entry in zip_file.infolist() if not entry.is_dir()]
        if len(names) != len(set(names)):
            raise ValueError(f"archive contains duplicate paths: {archive}")
        return {name: zip_file.read(name) for name in names}


def has_export_marker_in_archive(archive: Path) -> bool:
    try:
        return archive_files(archive).get(".chatgpt-skill-export") == EXPORT_MARKER
    except (BadZipFile, OSError, ValueError):
        return False


def plugin_metadata(name: str, source: Path) -> dict[str, str]:
    manifest = source / ".codex-plugin" / "plugin.json"
    if not manifest.is_file() or safe_relative(manifest, source) is None:
        raise ValueError(f"plugin manifest is missing: {manifest}")
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid plugin manifest: {manifest}") from error
    interface = data.get("interface", {})
    if data.get("name") != name or not all(isinstance(data.get(key), str) and data[key] for key in ("name", "version", "description")):
        raise ValueError(f"plugin manifest has incomplete metadata: {manifest}")
    icon = interface.get("composerIcon") or interface.get("logo")
    if not all(isinstance(interface.get(key), str) and interface[key] for key in ("displayName", "shortDescription")) or not isinstance(icon, str):
        raise ValueError(f"plugin manifest has incomplete interface metadata: {manifest}")
    icon_relative = Path(icon)
    icon_path = source / icon_relative
    if icon_relative.is_absolute() or not icon_path.is_file() or safe_relative(icon_path, source) is None:
        raise ValueError(f"plugin manifest icon is unsafe or missing: {icon_path}")
    prompt = interface.get("defaultPrompt", f"Use ${name} for this request.")
    if isinstance(prompt, list):
        prompt = prompt[0] if prompt and isinstance(prompt[0], str) else f"Use ${name} for this request."
    return {
        "display_name": interface["displayName"],
        "short_description": interface["shortDescription"],
        "description": data["description"],
        "icon": safe_relative(icon_path, source).as_posix(),
        "color": interface.get("brandColor", "#2563EB"),
        "default_prompt": prompt,
        "version": data["version"],
    }


def bundle_entry(name: str, workflows: dict[str, str], metadata: dict[str, str]) -> str:
    trigger = {
        "atlas": "software brainstorming through verified implementation, code review, debugging, or measured optimization",
        "spotter": "personal brainstorming through practical preparation, portable knowledge, daily planning, priorities, KPI or time review",
    }.get(name, metadata["description"])
    procedures = "\n".join(
        f"- `{workflow}` — {description} Read `references/package/skills/{workflow}/PROCEDURE.md`."
        for workflow, description in workflows.items()
    )
    version_note = f"Source package: {name}; version: {metadata['version']}.\n\n" if metadata["version"] else ""
    description = f"Use when the user needs {trigger}. Routes the request to the matching maintained procedure."
    return f"""---
name: {json.dumps(name)}
description: {json.dumps(description)}
---

{version_note}Read `references/package/core/{name.upper()}.md` first. It is the canonical doctrine
for this bundle and user and host instructions still outrank it.

Choose the one procedure that best matches the request, then read only the references
that procedure names. Whenever an internal procedure invokes another skill, read the
matching bundled procedure below and carry its arguments forward in this chat.
Bundled procedures do not register separate commands, agents, hooks or connectors.

Available procedures:
{procedures}

Use `references/package/` as the bundle root. Paths in the exported procedures already
resolve there. Helper scripts are reference material only: run one only when the host
can execute it and its required capability is available. When a required local tool,
connector, scheduled run, native agent, or lifecycle hook is unavailable, report that
specific gap and continue any independent read-only or preparation work. Do not claim
that this upload installs those capabilities.
"""


def safe_relative(path: Path, root: Path) -> Path | None:
    try:
        relative = path.relative_to(root)
        current = root
        for part in relative.parts:
            current /= part
            if current.is_symlink():
                return None
        path.resolve(strict=True).relative_to(root.resolve())
        return relative
    except (FileNotFoundError, ValueError):
        return None


def skill_descriptions(source: Path) -> dict[str, str]:
    descriptions = {}
    for path in sorted(source.glob("skills/*/SKILL.md")):
        if safe_relative(path, source) is None:
            raise ValueError(f"unsafe skill entry: {path}")
        header = path.read_text(encoding="utf-8").split("---", 2)[1]
        match = re.search(r"^description:\s*(.+)$", header, re.MULTILINE)
        if not match or match[1].strip() in {"|", ">", "|-", ">-"}:
            raise ValueError(f"expected canonical single-line description: {path}")
        descriptions[path.parent.name] = match[1].strip().strip("\"'")
    return descriptions


def rewrite_markdown(text: str, skill: str | None, source: Path) -> str:
    """Map plugin-relative instruction paths into the exported package tree."""
    text = text.replace("<plugin root>/", "references/package/")
    text = text.replace("<plugin root>", "references/package")
    # Some canonical prose names a sibling directly rather than through a placeholder.
    # Keep those references valid after the source tree moves under references/package.
    text = re.sub(
        r"(?<![\w/])skills/([a-z-]+)/(?:SKILL|PROCEDURE)\.md",
        r"references/package/skills/\1/PROCEDURE.md",
        text,
    )
    text = re.sub(
        r"(?<![\w/])skills/([a-z-]+)/references/([\w.-]+\.md)",
        r"references/package/skills/\1/references/\2",
        text,
    )
    if skill:
        text = text.replace(
            "<this skill>/", f"references/package/skills/{skill}/"
        )
        text = text.replace("<this skill>", f"references/package/skills/{skill}")
        # Procedure bodies formerly lived directly in skills/<skill>/.
        text = re.sub(
            r"(?<![\w/])references/([\w.-]+\.md)",
            rf"references/package/skills/{skill}/references/\1",
            text,
        )
        def rewrite_script(match: re.Match[str]) -> str:
            filename = match.group(1)
            root = "references/package" if (source / "scripts" / filename).is_file() else f"references/package/skills/{skill}"
            return f"{root}/scripts/{filename}"

        text = re.sub(r"(?<![\w/])scripts/((?:[\w.-]+/)*[\w.-]+\.(?:py|sh))", rewrite_script, text)
    text = text.replace("/SKILL.md", "/PROCEDURE.md")
    text = re.sub(
        r"Skill tool `[^`:]+:([a-z-]+)` / `[^`:]+:([a-z-]+)`, `\$[a-z-]+` / `\$[a-z-]+` on Codex",
        r"read `references/package/skills/\1/PROCEDURE.md` or `references/package/skills/\2/PROCEDURE.md` in this chat",
        text,
    )
    return re.sub(
        r"Skill tool `[^`:]+:([a-z-]+)`, `\$[a-z-]+` on Codex",
        r"read `references/package/skills/\1/PROCEDURE.md` in this chat",
        text,
    )


def referenced_root_helpers(source: Path, name: str) -> set[Path]:
    helpers: set[Path] = set()
    for document in list((source / "skills").rglob("*.md")) + [source / "core" / f"{name.upper()}.md"]:
        if not document.is_file() or safe_relative(document, source) is None:
            continue
        for filename in re.findall(r"scripts/((?:[\w.-]+/)*[\w.-]+\.(?:py|sh))", document.read_text(encoding="utf-8")):
            relative = Path(filename)
            candidate = source / "scripts" / relative
            if candidate.is_file() and safe_relative(candidate, source) is not None:
                helpers.add(relative)
    return helpers


def wiki_runtime_files(source: Path) -> tuple[Path, ...]:
    """Return the minimal runtime closure required by scripts/wiki.sh."""

    relative_paths = (
        Path("runtime/spotter_wiki/__init__.py"),
        Path("runtime/spotter_wiki/__main__.py"),
        Path("runtime/spotter_wiki/store.py"),
        Path("runtime/LICENSE.llm-wiki-kit"),
    )
    files = tuple(source / relative for relative in relative_paths)
    for path in files:
        if not path.is_file() or safe_relative(path, source) is None:
            raise ValueError(f"Spotter wiki helper requires a safe runtime file: {path}")
    return files


def export_package(name: str, source: Path, output: Path) -> Path:
    if not source.is_dir():
        raise ValueError(f"source directory is missing: {source}")
    core = source / "core" / f"{name.upper()}.md"
    if not core.is_file() or safe_relative(core, source) is None:
        raise ValueError(f"canonical core is missing: {core}")

    bundle = output / name
    marker = bundle / ".chatgpt-skill-export"
    if bundle.is_symlink() or (bundle.exists() and not has_export_marker(marker)):
        raise ValueError(f"refusing to replace unowned output directory: {bundle}")
    archive = output / f"{name}.zip"
    if archive.is_symlink():
        raise ValueError(f"refusing to replace symlink archive: {archive}")
    if archive.exists():
        try:
            with ZipFile(archive) as previous:
                owned = previous.read(".chatgpt-skill-export") == EXPORT_MARKER
        except (BadZipFile, KeyError):
            owned = False
        if not owned:
            raise ValueError(f"refusing to replace unowned archive: {archive}")
    if bundle.exists():
        shutil.rmtree(bundle)
    package = bundle / "references" / "package"
    (package / "core").mkdir(parents=True)
    (package / "core" / core.name).write_text(
        rewrite_markdown(core.read_text(), None, source), encoding="utf-8"
    )

    metadata = plugin_metadata(name, source)
    workflows = skill_descriptions(source)
    (bundle / "SKILL.md").write_text(bundle_entry(name, workflows, metadata), encoding="utf-8")
    (bundle / ".chatgpt-skill-export").write_bytes(EXPORT_MARKER)
    (bundle / "agents").mkdir(parents=True)
    (bundle / "agents" / "openai.yaml").write_text(
        f"# Source: {name} {metadata['version']}\n"
        "interface:\n"
        f"  display_name: {json.dumps(metadata['display_name'])}\n"
        f"  short_description: {json.dumps(metadata['short_description'])}\n"
        "  icon_small: \"./assets/icon.png\"\n"
        "  icon_large: \"./assets/icon.png\"\n"
        f"  brand_color: {json.dumps(metadata['color'])}\n"
        f"  default_prompt: {json.dumps(metadata['default_prompt'])}\n"
        "policy:\n"
        "  allow_implicit_invocation: true\n",
        encoding="utf-8",
    )

    for source_file in sorted((source / "skills").rglob("*")):
        if not source_file.is_file() or source_file.is_symlink():
            continue
        relative = safe_relative(source_file, source)
        if relative is None or relative.parts[0] != "skills":
            continue
        is_document = source_file.suffix == ".md"
        is_helper = source_file.suffix in {".py", ".sh"} and "scripts" in relative.parts
        if not (is_document or is_helper):
            continue
        destination = package / relative
        if destination.name == "SKILL.md":
            destination = destination.with_name("PROCEDURE.md")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if is_document:
            text = rewrite_markdown(source_file.read_text(encoding="utf-8"), relative.parts[1], source)
            # Markdown links resolve from the document, unlike instruction root paths.
            text = re.sub(
                r"(?<=\]\()(references/package/[^)#]+)(#[^)]*)?(?=\))",
                lambda match: Path(os.path.relpath(bundle / match[1], destination.parent)).as_posix() + (match[2] or ""),
                text,
            )
            destination.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(source_file, destination)

    root_helpers = referenced_root_helpers(source, name)
    for helper in root_helpers:
        source_file = source / "scripts" / helper
        if source_file.is_file() and safe_relative(source_file, source) is not None:
            destination = package / "scripts" / helper
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination)

    if name == "jobs-engine-seeker":
        for source_file in sorted((source / "scripts" / "jaf").rglob("*.py")):
            if source_file.is_symlink() or safe_relative(source_file, source) is None:
                raise ValueError(f"unsafe Jobs runtime helper: {source_file}")
            destination = package / source_file.relative_to(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination)

    if name == "spotter" and Path("wiki.sh") in root_helpers:
        for source_file in wiki_runtime_files(source):
            destination = package / source_file.relative_to(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination)

    icon = source / metadata["icon"]
    if icon.is_file() and safe_relative(icon, source) is not None:
        destination = bundle / "assets" / "icon.png"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(icon, destination)

    with ZipFile(archive, "w", ZIP_DEFLATED) as zip_file:
        for file in sorted(bundle.rglob("*")):
            if file.is_file():
                zip_file.write(file, file.relative_to(bundle))
    return bundle


def check_bundle(bundle: Path, source: Path) -> list[str]:
    errors: list[str] = []
    archive = bundle.parent / f"{bundle.name}.zip"
    if bundle.is_symlink():
        return [f"{bundle}: exported directory must not be a symlink"]
    skills = list(bundle.rglob("SKILL.md"))
    if skills != [bundle / "SKILL.md"]:
        errors.append(f"{bundle}: expected exactly one root SKILL.md, found {len(skills)}")
    package = bundle / "references" / "package"
    if not has_export_marker(bundle / ".chatgpt-skill-export"):
        errors.append(f"{bundle}: missing or invalid generated-output marker")
    if not (bundle / "agents" / "openai.yaml").is_file():
        errors.append(f"{bundle}: missing native UI sidecar")
    if not (bundle / "assets" / "icon.png").is_file():
        errors.append(f"{bundle}: missing native icon")
    for procedure in source.glob("skills/*/SKILL.md"):
        exported = package / procedure.relative_to(source)
        exported = exported.with_name("PROCEDURE.md")
        if not exported.is_file():
            errors.append(f"{bundle}: missing procedure {exported.relative_to(bundle)}")
    for document in package.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        if "<plugin root>" in text or "<this skill>" in text or "/SKILL.md" in text:
            errors.append(f"{bundle}: unresolved exported path in {document.relative_to(bundle)}")
        if "Skill tool" in text:
            errors.append(f"{bundle}: unresolved native skill invocation in {document.relative_to(bundle)}")
        if re.search(r"(?<!references/package/)skills/[a-z-]+/(?:PROCEDURE\.md|references/)", text):
            errors.append(f"{bundle}: raw plugin path in {document.relative_to(bundle)}")
        for target in set(re.findall(r"references/package/[\w./-]+\.(?:md|py|sh)", text)):
            if not (bundle / target).is_file():
                errors.append(f"{bundle}: broken reference {target} in {document.relative_to(bundle)}")
        for target in re.findall(r"\]\(([^)#]+\.(?:md|py|sh))(?:#[^)]+)?\)", text):
            if "://" not in target:
                resolved = (document.parent / target).resolve()
                if not resolved.is_relative_to(bundle.resolve()) or not resolved.is_file():
                    errors.append(f"{bundle}: broken relative reference {target} in {document.relative_to(bundle)}")
    for helper in referenced_root_helpers(source, bundle.name):
        if not (package / "scripts" / helper).is_file():
            errors.append(f"{bundle}: missing referenced root helper scripts/{helper}")
    wiki_helper = package / "scripts" / "wiki.sh"
    if wiki_helper.is_file():
        if bundle.name != "spotter":
            errors.append(f"{bundle}: wiki.sh is only supported by the Spotter runtime")
        else:
            runtime_files = wiki_runtime_files(source)
            expected_runtime = {
                source_file.relative_to(source).as_posix() for source_file in runtime_files
            }
            actual_runtime = {
                file.relative_to(package).as_posix()
                for file in (package / "runtime").rglob("*")
                if file.is_file()
            }
            for source_file in runtime_files:
                exported = package / source_file.relative_to(source)
                if not exported.is_file():
                    errors.append(f"{bundle}: missing wiki helper dependency {exported.relative_to(bundle)}")
            for unexpected in sorted(actual_runtime - expected_runtime):
                errors.append(f"{bundle}: unexpected wiki runtime artifact {unexpected}")
    if archive.is_symlink() or not archive.is_file():
        errors.append(f"{bundle}: missing generated archive {archive.name}")
    elif not has_export_marker_in_archive(archive):
        errors.append(f"{bundle}: archive is not owned by this exporter")
    else:
        try:
            if archive_files(archive) != bundle_files(bundle):
                errors.append(f"{bundle}: archive content differs from exported directory")
        except (BadZipFile, OSError, ValueError) as error:
            errors.append(f"{bundle}: cannot validate archive: {error}")
    try:
        with tempfile.TemporaryDirectory() as directory:
            expected = export_package(bundle.name, source, Path(directory))
            if bundle_files(bundle) != bundle_files(expected):
                errors.append(f"{bundle}: exported content differs from current source")
    except (OSError, ValueError) as error:
        errors.append(f"{bundle}: cannot validate current source: {error}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas-root", required=True, type=Path)
    parser.add_argument("--spotter-root", required=True, type=Path)
    parser.add_argument("--plugin", action="append", default=[], metavar="NAME=PATH", help="export an additional plugin from its canonical root")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--check", action="store_true", help="validate existing exports")
    args = parser.parse_args()
    output = args.output.resolve()
    source_roots = {"atlas": args.atlas_root.resolve(), "spotter": args.spotter_root.resolve()}
    for value in args.plugin:
        name, separator, path = value.partition("=")
        if not separator or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", name) or not path or name in source_roots:
            parser.error("--plugin must be NAME=PATH with a new plugin name")
        source_roots[name] = Path(path).resolve()

    if not args.check:
        output.mkdir(parents=True, exist_ok=True)
        for name, source in source_roots.items():
            export_package(name, source, output)

    errors = []
    for name, source in source_roots.items():
        errors.extend(check_bundle(output / name, source))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"exports: {', '.join(source_roots)}; one root SKILL.md each; source procedures and references closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
