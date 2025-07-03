"""

python envextract.py requirements_mini_import.txt requirements_lock.txt requirements_mini.txt

"""
import sys

def load_packages(filename):
    """读取 requirements 文件，返回只含包名（无版本）的集合"""
    packages = set()
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            package_name = line.split("==")[0].strip()  # 忽略版本号
            if package_name:
                packages.add(package_name.lower())
    return packages

def main():
    if len(sys.argv) != 4:
        print("Usage: python envextract.py <requirements_mini_import.txt> <requirements_lock.txt> <output.txt>")
        sys.exit(1)

    input_req = sys.argv[1]   # 包含你想要的依赖（可带版本，可有注释）
    full_list = sys.argv[2]   # 冻结后的完整依赖文件（如 requirements_lock.txt）
    output_file = sys.argv[3] # 输出文件路径

    # 加载目标包名（自动去除版本号、忽略注释）
    target_packages = load_packages(input_req)

    print(f"\n🔍 Looking for these packages:")
    for package in sorted(target_packages):
        print(f" - {package}")

    # 读取冻结文件并匹配
    matched = []
    with open(full_list, "r") as f:
        lines = f.readlines()

    total_lines = len(lines)
    print(f"\n📊 Processing {total_lines} lines from lock file...")

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        package_name = line.split("==")[0].lower()
        if package_name in target_packages:
            matched.append(line)

        # 每处理 10 行输出一次进度
        if (i + 1) % 10 == 0:
            print(f" → Processed {i + 1}/{total_lines} lines...")

    print(f"✅ Finished processing. Total matched: {len(matched)} packages.")

    # 写入输出文件
    with open(output_file, "w") as f:
        f.write("\n".join(matched) + "\n")

    print(f"\n📦 Wrote {len(matched)} packages to {output_file}")
    for line in matched:
        print(f" + {line}")

if __name__ == "__main__":
    main()