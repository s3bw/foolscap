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
    """Classifies each commit into the type of change, if commit isn't
    classified it is added to 'Unknown'.

    :param list[str] log: a log of all the commits
    :return: classified changes.
    :rtype: dict
    """
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
    """Creates the groupings of classified changes.

    :param dict changes: Classified changes.
    :param str|dict prefixs: Changes to group into template.
    :param str template: The template to present the changes in.
    :return: Presentable grouped changes.
    :rtype: str
    """
    if isinstance(prefixs, list):
        chnge = []
        for prefix in prefixs:
            chnge.append(changes.pop(prefix))
        section = '\n'.join(chnge)
    else:
        section = '\n'.join(changes.pop(prefixs))
    return template.format(section)


def patch_notes(changes):
    """Passes grouped changes into presentable templates.

    :param dict changes: Containing the classified changes.
    :return: the final patch note.
    :rtype: str
    """
    whole_note = ""
    if "FEA" in changes or "ENH" in changes:
        whole_note += sub_section(changes, ["FEA", "ENH"], FEATURES)
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

