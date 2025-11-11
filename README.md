# CAD Automation System

> **Purpose**: Project introduction and quick start guide for developers and AI agents
> **Lifecycle**: Stable (update when project fundamentals change)

Automated CAD drawing generation for AS 1100 compliant manufacturing drawings using build123d, ezdxf, and Claude AI for specification extraction.

## Project Status

**Architecture**: Template-Based Parametric CAD Generation

**Current Work**: See [`STATUS.md`](./STATUS.md) for active work, known issues, and recent changes

**Progress**: [View Project Board](https://github.com/IAMSamuelRodda/cad-automation-system/projects) | [View Issues](https://github.com/IAMSamuelRodda/cad-automation-system/issues)

---

## Overview

This system generates Australian Standard (AS 1100) compliant CAD drawings from user specifications using parametric templates and LLM-powered parameter extraction. It exports to open formats (STEP, DXF) and validates compliance against AS 1100.101/201 standards.

**Key Features:**
- **Template-Based Generation**: Parametric CAD templates for standard components (brackets, flanges, enclosures)
- **AS 1100 Validation**: Automated compliance checking (70%+ coverage) with scoring rubric
- **LLM Parameter Extraction**: Claude Haiku API extracts specifications from natural language
- **Open Formats**: STEP (3D) and DXF (2D) outputs without vendor lock-in

---

## Quick Start

### For AI Agents

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for detailed progress tracking workflow.

```bash
# View current progress
gh issue list --repo IAMSamuelRodda/cad-automation-system --state open

# View Epic/Feature tasks
gh issue view <issue-number> --repo IAMSamuelRodda/cad-automation-system

# Start working on a task
gh issue edit <issue-number> --add-label "status: in-progress" --repo IAMSamuelRodda/cad-automation-system
```

### For Developers

**🚀 Quick Start (Automated)**

```bash
# Clone repository
git clone https://github.com/IAMSamuelRodda/cad-automation-system.git
cd cad-automation-system

# Setup environment and run tests
python3 -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
pytest tests/
```

**What it does:**
- ✅ Creates Python 3.11+ virtual environment
- ✅ Installs build123d, ezdxf, FastAPI dependencies via uv
- ✅ Runs unit tests to verify installation

**See also:**
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) - System architecture and technical details
- [`DEVELOPMENT.md`](./DEVELOPMENT.md) - Development workflow and setup

---

## Architecture

**CAD Generation**:
- build123d 0.5+ (3D parametric modeling)
- ezdxf 1.1+ (2D DXF generation)
- OpenCascade (OCP wrapper for STEP export)

**Backend**:
- FastAPI 0.100+ (API framework)
- Python 3.11+ (type hints, async)
- SQLite (MVP) → PostgreSQL (production)
- Pydantic 2.0+ (schema validation)

**AI Integration**:
- Anthropic Claude Haiku API (parameter extraction)
- Confidence scoring for fallback to manual input

**Cost**: ~$300 MVP (LLM API), $3-10/month operational (Claude Haiku), $50-100/month infrastructure (production)

---

## Implementation Plan

The project is organized into 15 major epics with features and tasks tracked in GitHub Issues.

**View Current Status**: [GitHub Issues](https://github.com/IAMSamuelRodda/cad-automation-system/issues) | [Project Board](https://github.com/IAMSamuelRodda/cad-automation-system/projects)

**Technical Details**: See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for complete system architecture, database schema, and implementation specifications.

**Milestones**:
1. **v1.0 MVP** (Weeks 1-4): Template-based CAD engine, basic AS 1100 validation, CLI
2. **v1.1 AI-Assisted** (Weeks 5-10): LLM integration, web UI, expanded templates
3. **v2.0 Production** (Weeks 11-18): AI generation, human review workflow, cloud deployment

---

## Key Features

### Template-Based CAD Generation

Parametric templates for standard manufacturing components using build123d (3D) and ezdxf (2D). Supports mounting brackets, flanges, enclosures with dimensional parameters extracted from specs.

**Details**: See [`ARCHITECTURE.md`](./ARCHITECTURE.md) § CAD Generation Architecture

### AS 1100 Compliance Validation

Automated validation of Australian Standard 1100.101/201 compliance including sheet layout, line standards, dimensioning, text/symbols. Target 70%+ automated coverage with ≥95% pass threshold.

**Details**: See [`ARCHITECTURE.md`](./ARCHITECTURE.md) § Validation Architecture

### LLM Parameter Extraction

Claude Haiku API extracts dimensional parameters from natural language specifications with confidence scoring. Falls back to manual input for <70% confidence.

**Details**: See [`ARCHITECTURE.md`](./ARCHITECTURE.md) § LLM Integration Architecture

---

## Documentation

- **[`ARCHITECTURE.md`](./ARCHITECTURE.md)**: System architecture, database schema, tech stack, ADRs
- **[`STATUS.md`](./STATUS.md)**: Current work, known issues, recent changes
- **[`CONTRIBUTING.md`](./CONTRIBUTING.md)**: Workflow, progress tracking, Definition of Done
- **[`DEVELOPMENT.md`](./DEVELOPMENT.md)**: Git workflow, CI/CD, testing setup
- **[`CHANGELOG.md`](./CHANGELOG.md)**: Release history
- **[`CLAUDE.md`](./CLAUDE.md)**: AI agent navigation guide (comprehensive reference)

---

## Progress Tracking

This project uses **GitHub Issues + Projects** for dynamic progress tracking.

**View Progress**:
- [Project Board](https://github.com/IAMSamuelRodda/cad-automation-system/projects) (visual roadmap)
- [All Issues](https://github.com/IAMSamuelRodda/cad-automation-system/issues) (hierarchical: epic → feature → task)

**Update Progress** (agents):
```bash
# Mark epic/feature in-progress
gh issue edit <issue-number> --add-label "status: in-progress" --repo IAMSamuelRodda/cad-automation-system

# Close completed feature/task
gh issue close <issue-number> --comment "Feature complete" --repo IAMSamuelRodda/cad-automation-system
```

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for complete workflow.

---

## Testing

**Unit Tests**:
```bash
cd ~/repos/cad-automation-system
source .venv/bin/activate
pytest tests/
```

**With Coverage**:
```bash
pytest --cov=src/cad_automation tests/
```

**Test Coverage**:
- ✅ Template generation (parametric validation)
- ✅ AS 1100 validators (compliance checks)
- ✅ LLM parameter extraction (confidence scoring)

**See [`DEVELOPMENT.md`](./DEVELOPMENT.md)** for:
- Complete test setup instructions
- Test organization patterns
- Troubleshooting guide

---

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for:
- Workflow guide
- Progress tracking commands
- Best practices
- Example workflows

---

## License

Private

---

## Links

- **Repository**: https://github.com/IAMSamuelRodda/cad-automation-system
- **Project Board**: https://github.com/IAMSamuelRodda/cad-automation-system/projects
- **Issues**: https://github.com/IAMSamuelRodda/cad-automation-system/issues

---

**Last Updated**: 2025-11-11
