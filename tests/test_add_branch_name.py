from unittest.mock import Mock, patch, mock_open

import pytest

import prepare_commit_msg_hooks.add_branch_name as bn


@pytest.fixture
def mock_repo_class(monkeypatch, branch_name):
    def _mock_repo_class():
        Repo = Mock()
        Repo.head = Mock()
        Repo.head.ref = Mock()
        Repo.head.ref.name = branch_name
        return Repo
    monkeypatch.setattr(bn.git, "Repo", _mock_repo_class)

@pytest.mark.parametrize("branch_name", [
    ("main"), ("AB-123")
])
def test_get_branch_name(mock_repo_class, branch_name):
    assert bn.get_branch_name() == branch_name


@pytest.mark.parametrize("branch, expected_output", [
    ("AB-123", True), ("ab-123", False), ("aAB-123b", False), ("main", False)
])
def test_check_if_branch_match_pattern(branch, expected_output):
    assert bn.check_if_branch_match_pattern(branch, "[A-Z]{2,3}-[0-9]+") == expected_output


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


@pytest.mark.parametrize("branch_name, loc", [
    ("main", "prefix"), ("main", "suffix")
])
def test_add_branch_name_without_pattern(
    capsys, mock_repo_class, branch_name, loc
):
    return_value = bn.add_branch_name("filename", "[a-c]{2}-[0-9]+", loc)
    captured = capsys.readouterr()
    assert captured.out == "Branch doesn't match pattern. Addition skipped.\n"
    assert return_value == 0


@patch("builtins.open", new_callable=mock_open, read_data="commit mssg")
@pytest.mark.parametrize("branch_name, pattern, loc", [
    ("main", None, "prefix"),
    ("main", None, "suffix"),
    ("ab-123", "[a-c]{2}-[0-9]+", "prefix"),
    ("ab-123", "[a-c]{2}-[0-9]+", "suffix"),
])
def test_add_branch_name_with_pattern(
    capsys, mock_repo_class, branch_name, pattern, loc
):
    return_value = bn.add_branch_name("filename", pattern, loc)
    assert return_value == 0


#def test_main():
#    assert bn.main()
