import filecmp
import os
from pathlib import Path
from difflib import Differ


def highlight_line_diff(file1, file2):
    """
    Return a list of strings showing line-by-line comparison of two files.
    Lines starting with '- ' indicate content unique to file1,
    '+ ' indicate content unique to file2,
    '? ' shows location of a difference within the line.
    """
    with open(file1, 'r', encoding='utf-8', errors='replace') as f1, \
            open(file2, 'r', encoding='utf-8', errors='replace') as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

    differ = Differ()
    diff_result = list(differ.compare(f1_lines, f2_lines))
    return diff_result


def compare_directories(dir1: str, dir2: str):
    """
    Compare the contents of two directories recursively, listing mismatched files,
    as well as files and directories that are only in one of the two directories.
    Also shows line differences for mismatched files.
    """
    d1_path = Path(dir1)
    d2_path = Path(dir2)

    comparison = filecmp.dircmp(d1_path, d2_path)

    results = {
        'matches': [],
        'mismatches': [],
        'left_only': comparison.left_only,
        'right_only': comparison.right_only,
        'line_diffs': {}
    }

    common_files = comparison.common_files
    match_list, mismatch_list, _ = filecmp.cmpfiles(d1_path, d2_path, common_files, shallow=False)
    results['matches'].extend(match_list)

    # For mismatched files, highlight differences line-by-line
    for mm_file in mismatch_list:
        file1_path = d1_path / mm_file
        file2_path = d2_path / mm_file
        diff = highlight_line_diff(file1_path, file2_path)
        results['mismatches'].append(mm_file)
        results['line_diffs'][mm_file] = diff

    # Recurse into subdirectories
    for subdir in comparison.common_dirs:
        sub_results = compare_directories(d1_path / subdir, d2_path / subdir)
        for m in sub_results['matches']:
            results['matches'].append(f"{subdir}/{m}")
        for mm in sub_results['mismatches']:
            results['mismatches'].append(f"{subdir}/{mm}")
        for l in sub_results['left_only']:
            results['left_only'].append(f"{subdir}/{l}")
        for r in sub_results['right_only']:
            results['right_only'].append(f"{subdir}/{r}")
        # Merge line_diffs from subdirectories
        for file_name, diff_content in sub_results['line_diffs'].items():
            results['line_diffs'][f"{subdir}/{file_name}"] = diff_content

    return results


if __name__ == "__main__":
    # Example usage
    directory1 = r"D:\MyDrive2\pythonprojects\decks\src\test_gen_image"
    directory2 = r"D:\MyDrive2\pythonprojects\decks\src\test_gen_image2"

    comparison_results = compare_directories(directory1, directory2)

    print("Files that match:", comparison_results['matches'])
    print("Files that differ:", comparison_results['mismatches'])
    print("Only in first directory:", comparison_results['left_only'])
    print("Only in second directory:", comparison_results['right_only'])

    # Display line-by-line differences for each mismatched file
    for filename, diffs in comparison_results['line_diffs'].items():
        print(f"\nDifferences in {filename}:")
        for line in diffs:
            print(line, end='')