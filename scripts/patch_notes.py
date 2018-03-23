import sys
import subprocess


FEATURES = """
\tNew Features:
\t=============
{}
"""
FIXS = """
\tBug Fixs:
\t=========
{}
"""
TESTS = """
\tMore Tests:
\t===========
{}
"""
MISC = """
\t{}
\t{}
{}
"""
OTHER = """
\tOther:
\t======
{}
"""


def version_diff(from_version, to_version="HEAD"):
    output = subprocess.check_output([
        "git",
        "log",
        "--pretty=format:%s",
        "{}..{}".format(from_version, to_version),
        ])
    return str(output)[2:].split("\\n")


def classify(log):
    groups = {}
    for commit in log:
        try:
            grp, detail = commit.split(': ')
        except ValueError:
            grp, detail = 'UNK', commit
        if grp not in groups:
            groups[grp] = []
        groups[grp].append("\t- " + detail)
    return groups


def sub_section(changes, prefixs, template):
    section = '\n'.join(changes.pop(prefixs))
    return template.format(section)


def patch_notes(changes):
    whole_note = ""
    if "FEA" in changes:
        whole_note += sub_section(changes, "FEA", FEATURES)
    if "FIX" in changes:
        whole_note += sub_section(changes, "FIX", FIXS)
    if "TST" in changes:
        whole_note += sub_section(changes, "TST", TESTS)
    for key, values in changes.items():
        if key != "UNK":
            whole_note += MISC.format(
                key, '='*len(key),
                '\n'.join(values))
    if "UNK" in changes:
        whole_note += sub_section(changes, "UNK", OTHER)
    return whole_note


if __name__ == "__main__":
    version = sys.argv[1]
    to_version = "HEAD"
    n = "now"
    if len(sys.argv) > 2:
        to_version = sys.argv[2]
        n = to_version

    print("\nThis is what's happened since version {v} and {n}.".format(v=version, n=n))
    change_log = version_diff(version, to_version)
    changes = classify(change_log)
    print(patch_notes(changes))

