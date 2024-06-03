import pytest

import prepare_commit_msg_hooks.add_branch_name as bn


def test_get_branch_name():
    assert bn.get_branch_name

def test_check_if_branch_match_pattern():
    assert bn.check_if_branch_match_pattern

def test_add_prefix():
    assert bn.check_if_branch_match_pattern

def test_add_suffix():
    assert bn.add_suffix

def test_add_branch_name():
    assert bn.add_branch_name

def test_main():
    assert bn.main
