Prepare Commit Message Hooks
============================

Some hooks for prepare your commit message using `pre-commit`.
See also: https://github.com/pre-commit/pre-commit

### Using prepare-commit-msg-hooks with pre-commit

Create a `.prepate-commit-msg-config.yaml` and add:

```
-   repo: https://github.com/macfernandez/prepare-commit-msg-hooks
    rev: v1.0.0  # Use the ref you want to point at
    hooks:
    -   id: add-branch-name
```

### Available hooks

#### `add-branch-name`

Add the branch name to you commit message.

- `--pattern` - Check if branch match the passed pattern before adding it. If it doesn't match, it's not added either.
- `--prefix` - Wether to add the branch name as prefix (default).
- `--suffix` - Wether to add the branch name as suffix. Mutually exclusive with `--prefix`.

**Usage example**

```
-   repo: https://github.com/macfernandez/prepare-commit-msg-hooks
    rev: v1.0.0  # Use the ref you want to point at
    hooks:
    -   id: add-branch-name
        args: [--prefix, --pattern="[A-Z]{2}-[0-9]+"]
```