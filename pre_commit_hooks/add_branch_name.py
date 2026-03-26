from __future__ import annotations

import re
import argparse
from typing import Sequence, Literal

import git


def get_branch_name() -> str:
    """
    Get current branch name.

    Returns
    -------
    str
        Current branch name.
    """
    return git.Repo().head.ref.name


def check_if_branch_match_pattern(branch: str, pattern: str) -> bool:
    """
    """
    pattern = re.compile(rf"^{pattern}$")
    if pattern.search(branch):
        return True
    else:
        return False
    

def add_prefix(text: str, prefix: str) -> str:
    if not re.search(rf"^{prefix}\b", text):
        text = f"{prefix} {text}"
    return text


def add_suffix(text: str, suffix: str) -> str:
    text = text.strip()
    if not re.search(rf"\b{suffix}$", text):
        text = f"{text} {suffix}"
    return f"{text}\n"


def add_branch_name(
        filename: str,
        pattern: str = None,
        loc: Literal['prefix', 'suffix'] = 'prefix'
    ):
    branch_name = get_branch_name()

    if pattern:
        branch_match_pattern = check_if_branch_match_pattern(
            branch_name, pattern
        )
        if not branch_match_pattern:
            print("Branch doesn't match pattern. Addition skipped.")
            return 0
    
    with open(filename, 'r') as f:
        mssg = f.read()

    if loc == 'prefix':
        mssg = add_prefix(mssg, branch_name)

    elif loc == 'suffix':
        mssg = add_suffix(mssg, branch_name)

    with open(filename, 'w') as f:
        _ = f.write(mssg)
    
    return 0
    

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filename',
        help='Filenames to fix'
    )
    parser.add_argument(
        '--pattern', '-p',
        default=None,
        help='Pattern to check against branch name before adding it to the commit message'
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--prefix", action='store_const', dest='loc', const="prefix")
    group.add_argument("--suffix", action='store_const', dest='loc', const="suffix")
    
    args = parser.parse_args(argv)

    return_value = add_branch_name(args.filename, args.pattern, args.loc)

    return return_value

if __name__ == '__main__':
    raise SystemExit(main())
