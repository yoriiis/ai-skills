"""Validate skill directories: YAML frontmatter, references, and orphan files."""

import os
import re
import sys
import yaml

def validate_skill(skill_dir):
    """
    Validates the technical integrity of a specific skill.
    Checks YAML metadata, reference links, and identifies orphan files.
    Returns True if no Blocking errors were found.
    """
    skill_file = os.path.join(skill_dir, "SKILL.md")
    skill_name = os.path.basename(skill_dir)
    is_valid = True

    if not os.path.exists(skill_file):
        print(f"❌ {skill_name}: SKILL.md missing")
        return False

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. YAML Frontmatter Validation (Required for skills.sh compatibility)
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        print(f"❌ {skill_name}: Missing YAML frontmatter")
        is_valid = False
    else:
        try:
            data = yaml.safe_load(match.group(1))
            required_keys = ["name", "tags", "description"]
            for key in required_keys:
                if key not in data or not data[key]:
                    print(f"❌ {skill_name}: Missing or empty metadata '{key}'")
                    is_valid = False
        except yaml.YAMLError as exc:
            print(f"❌ {skill_name}: YAML syntax error: {exc}")
            is_valid = False

    # 2. Reference File Validation (Mapping)
    # We continue even if frontmatter failed to catch all reference errors
    referenced_files = set(re.findall(r"`?\./references/([\w-]+\.md)`?", content))
    missing_files = []

    for filename in referenced_files:
        ref_path = os.path.join(skill_dir, "references", filename)
        if not os.path.exists(ref_path):
            missing_files.append(filename)

    if missing_files:
        print(f"❌ {skill_name}: References not found: {', '.join(missing_files)}")
        is_valid = False

    # 3. Orphan Files Detection (Repository Hygiene)
    # Warnings do not trigger is_valid = False
    ref_dir = os.path.join(skill_dir, "references")
    if os.path.exists(ref_dir):
        on_disk_files = {f for f in os.listdir(ref_dir) if f.endswith(".md")}
        orphans = on_disk_files - referenced_files
        if orphans:
            print(f"⚠️  {skill_name}: Orphan files (unused): {', '.join(orphans)}")

    if is_valid:
        print(f"✅ {skill_name}: Validated ({len(referenced_files)} unique references)")

    return is_valid


if __name__ == "__main__":
    BASE_DIR = "skills"

    if not os.path.exists(BASE_DIR):
        print(f"❌ Base directory '{BASE_DIR}' not found")
        sys.exit(1)

    all_valid = True
    # Scan subdirectories and ensure we run through ALL of them
    for entry in os.scandir(BASE_DIR):
        if entry.is_dir():
            # Calling the function first ensures it executes even if all_valid is False
            skill_result = validate_skill(entry.path)
            if not skill_result:
                all_valid = False

    if all_valid:
        print("\n🚀 All skills are valid and ready for the Agent Skills ecosystem!")
    else:
        print("\n❌ Validation failed. Please fix the errors listed above.")
        sys.exit(1)