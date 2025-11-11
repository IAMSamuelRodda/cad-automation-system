# Contributing to CAD Automation System

> **Purpose**: Workflow guide, progress tracking, and planning new features
> **Lifecycle**: Stable (update when workflow processes change)

> **Before submitting code**: See `DEVELOPMENT.md` for pre-commit checklist, CI/CD expectations, and test organization.

## Getting Started: Local Development

**🚀 Quick Start**

```bash
cd ~/repos/cad-automation-system
python3 -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**What it sets up:**
- Python 3.11+ virtual environment
- build123d, ezdxf, OpenCascade dependencies
- FastAPI, Pydantic, SQLAlchemy (future milestones)
- pytest, pytest-cov for testing

**Result:** Virtual environment activated at ~/repos/cad-automation-system/.venv, ready to code!

**Full setup details:** See [`DEVELOPMENT.md`](./DEVELOPMENT.md) for complete environment configuration.

---

## Definition of Done

### For Feature Development

**Required:**
- [ ] Feature implemented and tested locally
- [ ] Unit tests written and passing (≥80% coverage)
- [ ] Integration tests written (if multi-component)
- [ ] Documentation updated (ARCHITECTURE.md, CLAUDE.md if patterns change)
- [ ] PR created with issue reference
- [ ] CI/CD pipeline passing (when implemented)

### For Bug Fixes

**⚠️ CRITICAL REQUIREMENT**: All bug fixes MUST include automated tests that verify the fix.

**Required:**
- [ ] Root cause identified and documented in issue
- [ ] Fix implemented
- [ ] Test written that reproduces the bug (fails before fix, passes after)
- [ ] Regression test added to test suite
- [ ] Issue updated with investigation notes

### For Template Development

**Required:**
- [ ] Pydantic parameter schema defined
- [ ] generate_3d() implemented with build123d
- [ ] generate_2d() implemented with ezdxf + AS 1100 layout
- [ ] export_step() and export_dxf() tested
- [ ] Unit tests verify parametric generation
- [ ] Manual verification of STEP/DXF output

### For AS 1100 Validator Development

**Required:**
- [ ] Validator extends BaseValidator
- [ ] validate() method returns ValidationResult
- [ ] Weight registered in compliance rubric
- [ ] Unit tests with AS 1100 compliant examples
- [ ] Unit tests with non-compliant examples
- [ ] Reference to AS 1100.101/201 standard section

---

## Progress Tracking

This project uses **GitHub Issues + GitHub Projects v2** for progress tracking.

### Issue Hierarchy

```
Milestone (timeboxed release group)
  ↓
Epic (large feature/initiative)
  ├─ Feature (user-facing functionality)
  │   └─ Task (implementation work)
  └─ Feature
      └─ Task
```

**Milestones:**
1. **v1.0 MVP** (Weeks 1-4): Template-based CAD engine, basic AS 1100 validation, CLI
2. **v1.1 AI-Assisted** (Weeks 5-10): LLM integration, web UI, expanded templates
3. **v2.0 Production** (Weeks 11-18): AI generation, human review workflow, cloud deployment

### Quick Reference

```bash
# View current progress
gh issue list --repo IAMSamuelRodda/cad-automation-system --state open

# View specific epic/feature with sub-issues
gh issue view <issue-number> --repo IAMSamuelRodda/cad-automation-system

# Mark work in progress
gh issue edit <issue-number> --add-label "status: in-progress" --repo IAMSamuelRodda/cad-automation-system
```

---

## Working on Features/Tasks

### Starting Work

```bash
# 1. Create branch from main
git checkout main
git pull origin main
git checkout -b feature/<feature-name>

# 2. Update issue status
gh issue edit <issue-number> --add-label "status: in-progress" --repo IAMSamuelRodda/cad-automation-system

# 3. Add comment
gh issue comment <issue-number> --body "Starting work on this feature" --repo IAMSamuelRodda/cad-automation-system
```

### Completing Work

```bash
# 1. Create commit with issue reference
git commit -m "feat: <description>

Implements Feature #<N>: <feature name>

<extended description>

Relates to #<epic-number>

🤖 Generated with [Claude Code](https://claude.com/claude-code)"

# 2. Push and create PR
git push -u origin feature/<feature-name>
gh pr create --repo IAMSamuelRodda/cad-automation-system --title "<title>" --body "<description>"

# 3. Update issue status when merged
gh issue close <issue-number> --comment "Feature complete" --repo IAMSamuelRodda/cad-automation-system
```

### Marking as Blocked

```bash
# Add blocked label and link to blocker
gh issue edit <issue-number> --add-label "status: blocked" --repo IAMSamuelRodda/cad-automation-system
gh issue comment <issue-number> --body "🚫 Blocked by #<blocker>: <reason>" --repo IAMSamuelRodda/cad-automation-system

# When unblocked
gh issue edit <issue-number> --remove-label "status: blocked" --add-label "status: in-progress" --repo IAMSamuelRodda/cad-automation-system
gh issue comment <issue-number> --body "✅ Unblocked: <resolution>" --repo IAMSamuelRodda/cad-automation-system
```

---

## Git Workflow

This project uses a **simple main-branch** workflow for MVP.

**Quick Reference:**
```bash
# Create feature branch from main
git checkout main && git pull origin main
git checkout -b feature/<name>

# Commit with issue reference
git commit -m "feat: <description>

Closes #<issue-number>"

# Create PR
gh pr create --repo IAMSamuelRodda/cad-automation-system --title "<title>" --body "<description>"
```

**See [`DEVELOPMENT.md`](./DEVELOPMENT.md)** for complete git workflow, CI/CD expectations, and troubleshooting.

---

## Best Practices

### 1. Always Check Current State First

```bash
# See what's being worked on
gh issue list --repo IAMSamuelRodda/cad-automation-system --state open --label "status: in-progress"

# View specific item's progress
gh issue view <issue-number> --repo IAMSamuelRodda/cad-automation-system
```

### 2. Update Status When Starting Work

```bash
# Mark in-progress
gh issue edit <issue-number> --add-label "status: in-progress" --repo IAMSamuelRodda/cad-automation-system
```

### 3. Comment on Progress

```bash
# Add detailed progress comments
gh issue comment <issue-number> --body "Completed <milestone>:
- <detail 1>
- <detail 2>

Next: <next step>" --repo IAMSamuelRodda/cad-automation-system
```

### 4. Link Commits to Issues

```bash
# Reference issue in commit messages
git commit -m "feat: <description>

<details>

Relates to #<issue-number>

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

---

## Planning New Features

### BLUEPRINT.yaml Lifecycle

**BLUEPRINT.yaml** is a planning tool for initial project structure, NOT a living reference document.

**When to Use:**
- Initial project planning (done)
- Major scope changes requiring re-planning

**When NOT to Use:**
- ❌ Tracking daily progress (use GitHub Issues instead)
- ❌ Updating task status (use issue labels instead)
- ❌ Adding minor tasks (create GitHub issue directly)

### Lifecycle Flow

```
1. Plan Feature → Write BLUEPRINT.yaml structure (done at project start)
2. Generate Issues → Create GitHub issues/milestones from BLUEPRINT
3. Archive → BLUEPRINT becomes historical reference
4. Track Progress → Use GitHub Issues/Projects, NOT BLUEPRINT.yaml
```

**When plans change:** See CLAUDE.md § Blueprint Change Management

---

## Project Links

- **GitHub Repository**: https://github.com/IAMSamuelRodda/cad-automation-system
- **Project Board**: https://github.com/IAMSamuelRodda/cad-automation-system/projects
- **Issues**: https://github.com/IAMSamuelRodda/cad-automation-system/issues

---

## Example Workflow

### Starting a New Feature

```bash
# 1. Check current state
gh issue list --repo IAMSamuelRodda/cad-automation-system --state open

# 2. View feature details
gh issue view <feature-number> --repo IAMSamuelRodda/cad-automation-system

# 3. Start work
gh issue edit <feature-number> --add-label "status: in-progress" --repo IAMSamuelRodda/cad-automation-system

# 4. Create branch
git checkout main && git pull origin main
git checkout -b feature/<name>

# 5. Do the work
# ... implement feature ...

# 6. Commit with issue reference
git commit -m "feat: implement <feature>

Implements Feature #<N>: <name>

<details>

Relates to #<epic>

🤖 Generated with [Claude Code](https://claude.com/claude-code)"

# 7. Push and create PR
git push -u origin feature/<name>
gh pr create --repo IAMSamuelRodda/cad-automation-system

# 8. When feature complete (after merge)
gh issue close <feature-number> --comment "Feature complete" --repo IAMSamuelRodda/cad-automation-system
```

---

## Troubleshooting

### GitHub CLI Not Authenticated

```bash
gh auth login
# Follow prompts to authenticate with GitHub
```

### Can't See Sub-Issues

Sub-issues are linked but may not display in all GitHub interfaces. Use:
```bash
gh issue view <parent-issue-number> --repo IAMSamuelRodda/cad-automation-system
# Look for "Sub-issues" section
```

---

## Need Help?

### Documentation
- Review `specs/BLUEPRINT.yaml` for technical specifications
- Check `ARCHITECTURE.md` for system architecture
- View git history: `git log --oneline --graph`

### Progress Tracking
- View all issues: `gh issue list --repo IAMSamuelRodda/cad-automation-system`
- View project board: Visit https://github.com/IAMSamuelRodda/cad-automation-system/projects

---

**Last Updated**: 2025-11-11
