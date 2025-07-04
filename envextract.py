"""

python envextract.py requirements_mini_import.txt requirements_lock.txt requirements_mini.txt

"""
import sys

import sys
import re

def normalize_name(name):
    """将包名统一为小写，并将 - 和 _ 视为等价"""
    return re.sub(r"[-_]+", "-", name.lower())

def load_packages(filename):
    """读取 requirements 文件，返回标准化后的包名集合"""
    packages = set()
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # package_name = line.split("==")[0].strip()
            package_name = line.split("==")[0].split(">=")[0].split("<=")[0].strip()

            if package_name:
                packages.add(normalize_name(package_name))
    return packages

def main():
    if len(sys.argv) != 4:
        print("Usage: python envextract.py <requirements_new.txt> <requirements_lock.txt> <output.txt>")
        sys.exit(1)

    input_req = sys.argv[1]
    full_list = sys.argv[2]
    output_file = sys.argv[3]

    target_packages = load_packages(input_req)
    normalized_target = {name: name for name in target_packages}

    print(f"\n🔍 Looking for these packages:")
    for package in sorted(target_packages):
        print(f" - {package}")

    matched = []
    not_found = set(target_packages)

    with open(full_list, "r") as f:
        lines = f.readlines()

    total_lines = len(lines)
    print(f"\n📊 Processing {total_lines} lines from lock file...")

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        package_name = normalize_name(line.split("==")[0])

        if package_name in normalized_target:
            matched.append(line)
            not_found.discard(package_name)

        if (i + 1) % 100 == 0:
            print(f" → Processed {i + 1}/{total_lines} lines...")

    print(f"✅ Finished processing. Total matched: {len(matched)} packages.")

    with open(output_file, "w") as f:
        f.write("\n".join(matched) + "\n")

    print(f"\n📦 Wrote {len(matched)} packages to {output_file}")
    for line in matched:
        print(f" + {line}")

    if not_found:
        print(f"\n❌ These packages were not found in lock file:")
        for package in sorted(not_found):
            print(f" - {package}")
    else:
        print("\n👍 All specified packages were found!")

if __name__ == "__main__":
    main()