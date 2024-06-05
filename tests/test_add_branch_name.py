import pytest
from unittest.mock import Mock, patch

import prepare_commit_msg_hooks.add_branch_name as bn



@pytest.fixture
def mock_repo_class(monkeypatch):
    def _mock_repo_class():
        Repo = Mock()
        Repo.head = Mock()
        Repo.head.ref = Mock()
        Repo.head.ref.name = "branch-name"
        return Repo
    monkeypatch.setattr(bn.git, "Repo", _mock_repo_class)

def test_get_branch_name(mock_repo_class):
    assert bn.get_branch_name() == "branch-name"


@pytest.mark.parametrize("branch, pattern, expected_output", [
    ("AB-123", "[A-Z]{2,3}-[0-9]+", True),
    ("ab-123", "[A-Z]{2,3}-[0-9]+", False),
    ("aAB-123b", "[A-Z]{2,3}-[0-9]+", False),
    ("main", "[A-Z]{2,3}-[0-9]+", False)
])
def test_check_if_branch_match_pattern(branch, pattern, expected_output):
    assert bn.check_if_branch_match_pattern(branch, pattern) == expected_output


@pytest.mark.parametrize("text, prefix, expected_output", [
    ("commit mssg", "AB-123", "AB-123 commit mssg"),
    ("AB-123 commit mssg", "AB-123", "AB-123 commit mssg"),
    ("ab-123 commit mssg", "AB-123", "AB-123 ab-123 commit mssg"),
    ("commit mssg AB-123", "AB-123", "AB-123 commit mssg AB-123"),
])
def test_add_prefix(text, prefix, expected_output):
    assert bn.add_prefix(text, prefix) == expected_output


@pytest.mark.parametrize("text, suffix, expected_output", [
    ("commit mssg\n", "AB-123", "commit mssg AB-123\n"),
    ("commit mssg AB-123\n", "AB-123", "commit mssg AB-123\n"),
    ("commit mssg ab-123\n", "AB-123", "commit mssg ab-123 AB-123\n"),
    ("AB-123 commit mssg\n", "AB-123", "AB-123 commit mssg AB-123\n")
])
def test_add_suffix(text, suffix, expected_output):
    assert bn.add_suffix(text, suffix) == expected_output

#def test_add_branch_name():
#    assert bn.add_branch_name
#
#def test_main():
#    assert bn.main
#