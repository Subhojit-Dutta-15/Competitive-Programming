import os
import re
from urllib.parse import quote

# Map folder names in your repo to the Display Names in the README
PLATFORMS = {
    "Leetcode": "LeetCode",
    "HackerRank": "HackerRank",
}


def natural_sort_key(item):
    """Sorts filenames naturally (e.g., 2_prob.py comes before 10_prob.py)."""
    filename = item[0]
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r"(\d+)", filename)
    ]


def format_title(filename):
    """Removes .py and leading numbers/separators (e.g., '0001_two-sum.py' -> 'Two Sum')."""
    name = os.path.splitext(filename)[0]
    name = re.sub(r"^\d+[-_\s]*", "", name)
    return re.sub(r"[-_]+", " ", name).strip().title()


def get_problem_number(filename):
    """Extracts leading digits as the problem number, or returns '-'."""
    match = re.match(r"^(\d+)", filename)
    return str(int(match.group(1))) if match else "-"


def scan_platform_files(base_folder):
    """Recursively scans a platform folder for .py files and tracks subfolders as topics."""
    found_files = []
    if not os.path.exists(base_folder):
        return found_files

    for root, _, files in os.walk(base_folder):
        for f in files:
            if f.endswith(".py") and not f.startswith("__"):
                rel_dir = os.path.relpath(root, base_folder)
                topic = "-" if rel_dir == "." else rel_dir.replace(os.sep, " / ").title()
                full_rel_path = os.path.join(root, f).replace(os.sep, "/")
                found_files.append((f, topic, full_rel_path))

    return sorted(found_files, key=natural_sort_key)


def generate_readme():
    stats = {}
    sections = []

    for folder, display_name in PLATFORMS.items():
        files = scan_platform_files(folder)
        stats[display_name] = len(files)

        section_lines = [f"## 🧩 {display_name} Solutions\n"]
        if not files:
            section_lines.append("*No solutions uploaded yet.*\n")
        else:
            section_lines.append("| # | Problem | Category / Folder | Solution |")
            section_lines.append("| :---: | :--- | :---: | :---: |")
            for filename, topic, filepath in files:
                num = get_problem_number(filename)
                title = format_title(filename)
                encoded_link = f"./{quote(filepath)}"
                section_lines.append(f"| {num} | {title} | {topic} | [Python]({encoded_link}) |")
            section_lines.append("")

        sections.append("\n".join(section_lines))

    total_solved = sum(stats.values())

    readme_content = [
        "# Competitive Programming & DSA Solutions 🚀\n",
        "An auto-updating repository tracking my Data Structures and Algorithms practice across **LeetCode** and **HackerRank** using **Python 3**.\n",
        "> 🤖 *This README is automatically updated via GitHub Actions whenever new solutions are pushed.*\n",
        "---\n",
        "## 📊 Live Progress Tracker\n",
        "| Platform | Solved |",
        "| :--- | :---: |",
    ]

    for display_name, count in stats.items():
        readme_content.append(f"| **{display_name}** | {count} |")

    readme_content.append(f"| **Total** | **{total_solved}** |\n")
    readme_content.append("---\n")
    readme_content.extend(sections)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(readme_content))


if __name__ == "__main__":
    generate_readme()