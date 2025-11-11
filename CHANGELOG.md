# Changelog

All notable changes to CAD Automation System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Project foundation and documentation structure
- BLUEPRINT.yaml with 15 epics and 26.5 day AI-calibrated timeline
- GitHub repository with issue hierarchy and project tracking
- Core documentation (README, ARCHITECTURE, STATUS, CONTRIBUTING, DEVELOPMENT, CHANGELOG)

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

---

## [0.1.0] - 2025-11-11 (Planned)

### Summary
Initial MVP foundation including Python environment setup, BaseTemplate abstract class, and first proof-of-concept mounting bracket template with STEP/DXF export.

### Added
- **Python Environment Setup** - Virtual environment with build123d, ezdxf, OCP dependencies
  - uv package manager integration
  - requirements.txt with pinned versions
  - Virtual environment at ~/repos/cad-automation-system/.venv

- **BaseTemplate Abstract Class** - Foundation for parametric CAD templates
  - generate_3d() interface for build123d models
  - generate_2d() interface for ezdxf drawings with AS 1100 layout
  - export_step() and export_dxf() helper methods
  - Pydantic BaseModel for parameter validation

- **MountingBracketTemplate POC** - First working template implementation
  - MountingBracketParams schema (width, height, thickness, hole_diameter, material)
  - 3D L-bracket generation with build123d
  - 2D AS 1100 compliant drawing with ezdxf
  - STEP and DXF export functionality

### Changed
- N/A

### Fixed
- N/A

### Security
- API keys managed via environment variables (ANTHROPIC_API_KEY)
- .env file excluded from git via .gitignore

---

## Template for Future Releases

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Summary
Brief description of this release (2-3 sentences).

### Added
- New features
- New templates
- New validators

### Changed
- Changes to existing functionality
- Deprecations
- Refactoring

### Deprecated
- Features marked for removal in future versions

### Removed
- Features removed in this version

### Fixed
- Bug fixes
- Security patches

### Security
- Security-related changes
```

---

## Release Type Guidelines

### Major Version (X.0.0)
- Breaking changes to template API
- Incompatible parameter schema changes
- Database schema changes requiring migration
- Architectural changes

### Minor Version (0.X.0)
- New templates (backward compatible)
- New validators
- New API endpoints (Milestone 2+)
- Deprecations (with backward compatibility)

### Patch Version (0.0.X)
- Bug fixes
- Security patches
- Documentation updates
- Performance improvements

---

## Milestones

### v1.0 MVP (Weeks 1-4)
- Template-based CAD engine (3-5 templates)
- Basic AS 1100 validation (70%+ automated)
- CLI interface
- STEP/DXF export

### v1.1 AI-Assisted (Weeks 5-10)
- LLM integration (Claude Haiku parameter extraction)
- Web UI (FastAPI + React)
- Expanded template library (8-12 templates)
- Enhanced AS 1100 validation (80%+ automated)

### v2.0 Production (Weeks 11-18)
- AI-powered CAD generation (beyond templates)
- Human review workflow
- Cloud deployment (AWS ECS)
- Production database (PostgreSQL)
- Multi-user support

---

## Links

- **Repository:** https://github.com/IAMSamuelRodda/cad-automation-system
- **Project Board:** https://github.com/IAMSamuelRodda/cad-automation-system/projects
- **Issues:** https://github.com/IAMSamuelRodda/cad-automation-system/issues

---

[Unreleased]: https://github.com/IAMSamuelRodda/cad-automation-system/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/IAMSamuelRodda/cad-automation-system/releases/tag/v0.1.0
