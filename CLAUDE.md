# CAD Automation System - CLAUDE.md

> **Purpose**: Minimal critical directives for AI agents (pointers to detailed documentation)
> **Lifecycle**: Living (keep minimal, move verbose content to CONTRIBUTING.md or DEVELOPMENT.md)

## 📍 Critical Documents

**Before starting work:**
1. Read `STATUS.md` → Current issues, active work, what's broken
2. Read `ARCHITECTURE.md` → System architecture, tech stack, AS 1100 compliance
3. Read `CONTRIBUTING.md` → How to track progress with GitHub issues

**Before finishing work:**
1. Update `STATUS.md` → Add investigation notes, mark issues resolved
2. Update GitHub issues → Close completed tasks, link commits
3. Check `DEVELOPMENT.md` → Run pre-commit checklist (lint, format, tests)

**Planning artifact:** `specs/BLUEPRINT.yaml` is for generating GitHub issues when planning NEW features, NOT for reference during implementation. It becomes historical once issues are created.

---

## 📋 Issue Hierarchy

This project uses GitHub's hierarchical issue structure:

```
Milestone (timeboxed release group)
  └─ Epic (large feature/initiative, e.g., "Foundation", "Template Library")
      └─ Feature (user-facing functionality, e.g., "AS 1100 Validation")
          └─ Task (implementation work, e.g., "Sheet Layout Validator")
              └─ Subtask (granular steps, if needed)
```

**YAML Structure**: The BLUEPRINT.yaml uses `milestones.milestone_1.epics.epic_1`, `feature_1_1`, `task_1_2_1` keys matching this hierarchy.

**Key Milestones**:
- **v1.0 MVP** (Weeks 1-4): Template-based CAD engine, basic AS 1100 validation, CLI
- **v1.1 AI-Assisted** (Weeks 5-10): LLM integration, web UI, expanded templates
- **v2.0 Production** (Weeks 11-18): AI generation, human review workflow, cloud deployment

See `github-project-setup` skill for automated issue creation from BLUEPRINT.

---

## 🏗️ Architecture Quick Facts

### Style
- **Template-Based CAD Generation** (parametric components → STEP/DXF output)
- **AS 1100 Compliance** (automated validation + manual review workflow)

### Technology Stack
- **CAD**: build123d (3D), ezdxf (2D), OpenCascade (kernel)
- **Backend**: FastAPI (Python 3.11+)
- **Package Management**: uv (ALWAYS use instead of pip)
- **LLM**: Claude Haiku API (specification extraction)

### High-Level Flow
```
User Input → Specification Extraction → CAD Generation → AS 1100 Validation → Output (STEP/DXF)
```

See `ARCHITECTURE.md` for complete details (project structure, AS 1100 compliance rubric, validation strategy).

---

## 🎯 Project-Specific Conventions

### Naming Conventions
- Templates: `PascalCase` classes extending `BaseTemplate`
- Validators: `PascalCase` classes in `validators/`
- Services: `snake_case.py` in feature directories
- Tests: `test_<module>.py`

### AS 1100 Standards
- **AS 1100.101**: General principles (sheet layout, line standards, dimensioning)
- **AS 1100.201**: Mechanical engineering drawing
- **Target compliance**: ≥95% automated checks before output

See `ARCHITECTURE.md` § AS 1100 Compliance for rubric and validation strategy.

---

## ⚠️ Critical Constraints

1. **File Formats**: STEP (primary), DXF (secondary) - open standards only (no commercial CAD)
2. **Package Management**: ALWAYS use `uv` instead of `pip` (10-100x faster)
3. **AS 1100 Compliance**: ≥95% compliance score required before output
4. **AI Calibration**: 22.8x speedup over human estimates (0.044 × 1.3 multiplier)
5. **Cost Limits**: MVP $300 total, avoid Zoo API ($250-500/month) until Milestone 3

---

## 🚀 Getting Started

```bash
# Mark epic/feature/task in progress
gh issue edit <issue-number> --add-label "status: in-progress" --repo IAMSamuelRodda/cad-automation-system
```

See `CONTRIBUTING.md` for complete workflow and `README.md` for quick start setup.

---

## 🔄 GitHub Workflow

**Commit-Issue Linking**: Every commit MUST reference a GitHub issue (`Closes #N`, `Relates to #N`). See `CONTRIBUTING.md` § Link Commits to Issues.

**PR Merge Strategy**: Use `gh pr merge --merge` (NOT `--squash`) to preserve feature branch history. See `DEVELOPMENT.md` § Git Branching Strategy.

---

## 📘 Planning New Features

**BLUEPRINT.yaml** is for planning NEW features before converting to GitHub issues. Once issues are created, it becomes historical. See `CONTRIBUTING.md` § Planning New Features for complete workflow.

**Blueprint Change Management**: When plans change, update GitHub first, then BLUEPRINT.yaml with concise comments. See `CONTRIBUTING.md` § Blueprint Change Management.

---

## 🔗 External Links

- **Project Board**: https://github.com/users/IAMSamuelRodda/projects/3
- **Issues**: https://github.com/IAMSamuelRodda/cad-automation-system/issues
- **Repository**: https://github.com/IAMSamuelRodda/cad-automation-system

---

## 🧪 Testing & Development

**Run tests**: `pytest tests/` (unit + integration)

**Test coverage**: `pytest --cov=src/cad_automation tests/` (target ≥80%)

**Package management**: `uv pip install -r requirements.txt` (NEVER use `pip`)

**Details**: See `DEVELOPMENT.md` for complete testing strategy, pre-commit checklist, and troubleshooting.

---

**Last Updated**: 2025-11-11
**Blueprint Version**: 1.0
**Milestone**: v1.0 MVP - Template-Based CAD Engine
