# Commit Changes

Generate and execute a Conventional Commits compliant commit.

**Important**: Only run this command when the user explicitly asks to commit.

---

## Steps

### 1. Check Staged Changes

```bash
git status
git diff --cached --stat
```

If no staged changes, prompt user:

> "No staged changes. Run `git add <files>` first, or would you like me to stage specific files?"

### 2. Analyze Changes

```bash
git diff --cached
```

Understand:

- What files changed
- What type of change (feature, fix, docs, etc.)
- The scope of changes

### 3. Determine Commit Type

| Type       | When to Use                             |
| ---------- | --------------------------------------- |
| `feat`     | New feature or functionality            |
| `fix`      | Bug fix                                 |
| `docs`     | Documentation only changes              |
| `style`    | Formatting, whitespace (no code change) |
| `refactor` | Code restructuring (no feature/fix)     |
| `perf`     | Performance improvement                 |
| `test`     | Adding or updating tests                |
| `chore`    | Maintenance, dependencies, config       |
| `ci`       | CI/CD changes                           |
| `build`    | Build system changes                    |

### 4. Generate Commit Message

Format:

```
<type>: <short description>

[optional body - what and why]

Co-Authored-By: Claude <noreply@anthropic.com>
```

Rules:

- Type: lowercase, from the list above
- Description: lowercase, imperative mood, no period at end
- Max 100 characters for first line
- Body: wrap at 72 characters

### 5. Show Preview and Confirm

Display the proposed commit:

```
Proposed commit:
────────────────────────────────────
<type>: <description>

<body if any>

Co-Authored-By: Claude <noreply@anthropic.com>
────────────────────────────────────

Files to commit:
- <file list>
```

Ask: "Proceed with this commit? (Or suggest changes)"

### 6. Execute Commit

Only after user confirms:

```bash
git commit -m "$(cat <<'EOF'
<type>: <description>

<body if any>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 7. Verify Success

```bash
git log -1 --oneline
```

---

## Examples

### Documentation change

```
docs: add api reference section
```

### New feature

```
feat: add user authentication flow

Implement login/logout functionality with session management.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Bug fix

```
fix: resolve broken navigation link

The quickstart link was pointing to a non-existent page.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Multiple file types

```
chore: update dependencies and config

- Upgrade husky to v9
- Add prettier configuration
- Update lint-staged rules

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Forbidden

- **Never** commit without user confirmation
- **Never** use `git add .` or `git add -A` without explicit approval
- **Never** amend commits unless explicitly asked
- **Never** force push
