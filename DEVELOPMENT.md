# Development Workflow

> **Purpose**: Git workflow, CI/CD pipelines, and pre-commit checklist
> **Lifecycle**: Stable (update when branching strategy or CI/CD processes change)

---

## 🌿 Git Branching Strategy

This project uses a **simple main-branch** model for MVP (single developer).

### Branch Overview

| Branch | Purpose | Deployments | Auto-Merge | Approval Required |
|--------|---------|-------------|-----------|-------------------|
| `main` | Stable code | None (CLI-only MVP) | No | No (single dev) |
| `feature/*` | Feature development | None | No | No (single dev) |

### Development Flow

```bash
# 1. Always branch from main
git checkout main
git pull origin main
git checkout -b feature/<feature-name>

# 2. Work on feature with frequent commits
git add .
git commit -m "feat: <description> (Relates to #<issue>)"

# 3. Push and create PR (optional for single dev)
git push -u origin feature/<feature-name>
gh pr create --repo IAMSamuelRodda/cad-automation-system

# 4. Merge to main when complete
git checkout main
git merge feature/<feature-name>
git push origin main
```

### PR Merge Strategy

**RULE**: Use `--squash` for feature branches (clean history).

**Why**: Keeps main branch history clean with one commit per feature.

**How to Merge**:
```bash
# Merge feature branch with squash
git checkout main
git merge --squash feature/<feature-name>
git commit -m "feat: <feature description> (Closes #<issue>)"
git push origin main

# Do NOT use:
git merge feature/<feature-name>  # ❌ Creates merge commit
```

---

## 🔍 Pre-Commit Checklist (CRITICAL)

**Before EVERY commit**, complete this checklist:

```bash
# 1. Run linting (when configured)
# ruff check . --fix  # TODO: Add in Milestone 1

# 2. Format code (when configured)
# black src/ tests/  # TODO: Add in Milestone 1

# 3. Run unit tests
pytest tests/

# 4. Run with coverage (optional)
pytest --cov=src/cad_automation tests/

# 5. Review staged changes
git status
git diff --staged

# 6. Verify commit message includes issue reference
#    Use: "Closes #N", "Relates to #N", "Fixes #N"
```

**Why**: Prevents bugs from reaching main branch. CI will enforce these checks in Milestone 1.

---

## 🚀 CI/CD Workflow Expectations

CI/CD will be implemented in **Milestone 1 (Week 2)** with GitHub Actions.

### Planned Workflows

| Workflow | Triggers | Checks | Pass Criteria | Duration |
|----------|----------|--------|---------------|----------|
| **Test** | Push to any branch | pytest + coverage | 100% tests pass, ≥80% coverage | ~2 min |
| **Lint** | Push to any branch | ruff, black | No linting errors | ~30 sec |
| **Build** | PR to main | Package build test | Build succeeds | ~1 min |

### Branch-Specific Workflows

**On `feature/*` → `main` PR**:
1. Run tests with coverage
2. Run linters
3. Verify documentation updated

**On `main` push**:
1. Run full test suite
2. Generate coverage report
3. Update documentation

### Monitoring Workflow Status

```bash
# View recent workflow runs (when implemented)
gh run list --repo IAMSamuelRodda/cad-automation-system

# Watch latest workflow (blocks until complete)
gh run watch --repo IAMSamuelRodda/cad-automation-system

# View specific workflow logs
gh run view <run-id> --log --repo IAMSamuelRodda/cad-automation-system
```

### If Workflows Fail

1. **Check which workflow failed**: `gh run list`
2. **View failure logs**: `gh run view <run-id> --log`
3. **Fix issues locally** using pre-commit checklist
4. **Push fix**: CI will re-run automatically

**Common failures**:
- **Test failures**: Check pytest output, verify test data
- **Lint failures**: Run `ruff check . --fix` locally
- **Coverage failures**: Add tests for uncovered code

---

## 🗄️ Package Management Pattern

**RULE**: ALWAYS use `uv` instead of `pip` for package management.

### Supported Commands

1. **Install packages**:
   ```bash
   uv pip install <package>
   ```

2. **Install from requirements**:
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Uninstall packages**:
   ```bash
   uv pip uninstall <package>
   ```

### Why uv?

- 10-100x faster than pip
- Better dependency resolution
- Preferred tool per global CLAUDE.md

**Applies to**:
- All Python package installations
- requirements.txt updates
- Virtual environment setup

---

## 🧪 Test Organization

### Directory Structure

```
tests/
├── unit/                 # Unit tests (no external dependencies)
│   ├── templates/
│   │   └── test_mounting_bracket.py  # Template generation tests
│   └── validators/
│       └── test_sheet_layout.py      # Validator tests
│
└── integration/          # Integration tests (multi-component)
    └── test_end_to_end.py  # Full pipeline tests
```

### Test Types

| Test Type | Location | External Dependencies | Run Command |
|-----------|----------|----------------------|-------------|
| **Unit** | tests/unit/ | No | `pytest tests/unit/` |
| **Integration** | tests/integration/ | Yes (files, LLM API) | `pytest tests/integration/` |

**Rule**: Unit tests should not depend on external resources (files, APIs, databases). Use mocks.

### Running Tests Locally

```bash
# Unit tests (fast, no dependencies)
pytest tests/unit/

# Integration tests (requires API keys for LLM tests)
export ANTHROPIC_API_KEY=<your-key>
pytest tests/integration/

# All tests
pytest tests/

# With coverage
pytest --cov=src/cad_automation tests/

# With coverage report
pytest --cov=src/cad_automation --cov-report=html tests/
# Open htmlcov/index.html in browser
```

---

## 🔐 Environment Variables

### Required Variables

| Variable | Purpose | Required When | Example |
|----------|---------|---------------|---------|
| `ANTHROPIC_API_KEY` | Claude Haiku API access | LLM parameter extraction | `sk-ant-...` |
| `CAD_AUTOMATION_LOG_LEVEL` | Logging verbosity | Debugging | `DEBUG`, `INFO`, `WARNING` |

### Usage

```bash
# Set for current session
export ANTHROPIC_API_KEY=sk-ant-...
export CAD_AUTOMATION_LOG_LEVEL=DEBUG

# Or use .env file (not committed to git)
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
echo "CAD_AUTOMATION_LOG_LEVEL=INFO" >> .env

# Load in Python
from dotenv import load_dotenv
load_dotenv()
```

### Troubleshooting

#### Error: Missing ANTHROPIC_API_KEY

**Cause:** Environment variable not set when running LLM integration tests.

**Solutions**:
1. Set environment variable: `export ANTHROPIC_API_KEY=<your-key>`
2. Create .env file with API key
3. Skip LLM tests: `pytest tests/ -k "not llm"`

---

## 📦 Local Development Setup

### Python Environment Setup

```bash
cd ~/repos/cad-automation-system

# Create virtual environment (Python 3.11+)
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install dependencies via uv
uv pip install -r requirements.txt

# Verify installation
python -c "import build123d; import ezdxf; print('CAD libraries installed')"
pytest tests/ -v
```

### Development Dependencies

**Core CAD Libraries:**
- build123d 0.5+
- ezdxf 1.1+
- OCP (OpenCascade Python wrapper)

**Backend:**
- fastapi 0.100+ (Milestone 2)
- pydantic 2.0+
- sqlalchemy 2.0+

**Testing:**
- pytest 7.4+
- pytest-cov 4.1+

**Code Quality (Milestone 1):**
- ruff (linter)
- black (formatter)
- mypy (type checker)

---

## 🐛 Troubleshooting

### OpenCascade (OCP) Installation Fails

**Symptom:** `pip install OCP` or `uv pip install OCP` fails with compilation errors.

**Cause:** OCP requires system-level OpenCascade libraries.

**Solution (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y libocct-*-dev
uv pip install OCP
```

**Solution (macOS):**
```bash
brew install opencascade
uv pip install OCP
```

### build123d Import Errors

**Symptom:** `ImportError: cannot import name 'Part' from 'build123d'`

**Cause:** Outdated build123d version or missing OCP dependency.

**Solution:**
```bash
uv pip install --upgrade build123d OCP
```

### pytest Not Found

**Symptom:** `pytest: command not found`

**Cause:** Virtual environment not activated or pytest not installed.

**Solution:**
```bash
source .venv/bin/activate
uv pip install pytest pytest-cov
```

---

## 📚 Additional Resources

- **Architecture**: `ARCHITECTURE.md` - Complete technical specifications
- **Progress Tracking**: `CONTRIBUTING.md` - Issue workflow and commands
- **Project Navigation**: `CLAUDE.md` - Quick reference for finding information

---

**Last Updated**: 2025-11-11
