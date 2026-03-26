Pre Commit Hooks
============================

Some hooks for preparing your commit message using `pre-commit`.

See also: https://github.com/pre-commit/pre-commit

### Using pre-commit-hooks with pre-commit

Create a `.pre-commit-config.yaml` and add:

```
-   repo: https://github.com/macfernandez/pre-commit-hooks
    rev: v1.0.0  # Use the ref you want to point at
    hooks:
    -   id: add-branch-name
```

### Available hooks

#### `add-branch-name`

Add the branch name to your commit message.

- `--pattern`: Check if branch match the passed pattern before adding it. If it doesn't match, it's not added either.
- `--prefix`: Whether to add the branch name as prefix (default).
- `--suffix`: Whether to add the branch name as suffix. Mutually exclusive with `--prefix`.

**Usage example**

```
-   repo: https://github.com/macfernandez/pre-commit-hooks
    rev: v1.0.0  # Use the ref you want to point at
    hooks:
    -   id: add-branch-name
        args: [--prefix, --pattern="[A-Z]{2}-[0-9]+"]
```
