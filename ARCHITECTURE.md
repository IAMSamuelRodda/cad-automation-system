# Architecture Documentation

> **Purpose**: Technical reference for system architecture, database schema, tech stack, and ADRs
> **Lifecycle**: Living (update as implementation diverges from original plan)

**Version:** 1.0
**Last Updated:** 2025-11-11

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Pattern](#architecture-pattern)
3. [Technology Stack](#technology-stack)
4. [CAD Generation Architecture](#cad-generation-architecture)
5. [Validation Architecture](#validation-architecture)
6. [LLM Integration Architecture](#llm-integration-architecture)
7. [Database Schema](#database-schema)
8. [API Architecture](#api-architecture)
9. [Security](#security)
10. [AS 1100 Compliance Strategy](#as-1100-compliance-strategy)
11. [Architecture Decision Records](#architecture-decision-records)

---

## System Overview

The CAD Automation System generates Australian Standard (AS 1100) compliant manufacturing drawings from user specifications. It uses parametric templates for standardized components (brackets, flanges, enclosures), validates output against AS 1100.101/201 standards, and exports to open formats (STEP, DXF).

**Key Characteristics:**
- **Template-Based**: Parametric CAD templates with dimensional parameters
- **Compliance-First**: Automated AS 1100 validation with 70%+ coverage target
- **Open Standards**: STEP (3D) and DXF (2D) outputs without vendor lock-in
- **AI-Assisted**: Claude Haiku API for specification parameter extraction

**Primary Use Case:**
User provides component specification → LLM extracts parameters → Template generates 3D/2D CAD → AS 1100 validator checks compliance → Output STEP/DXF files

---

## Architecture Pattern

### Modular Pipeline Architecture

The system uses a modular pipeline where each stage has well-defined inputs/outputs and can be tested independently.

**Benefits:**
- Clear separation of concerns (extraction, generation, validation)
- Easy to add new templates or validators
- Testable components with mock inputs/outputs

**Structure Pattern:**
```
src/cad_automation/
├── templates/          # Parametric CAD generation
│   ├── base.py        # BaseTemplate abstract class
│   ├── mounting_bracket.py
│   └── flange.py
├── validators/        # AS 1100 compliance checking
│   ├── base.py        # BaseValidator abstract class
│   ├── sheet_layout.py
│   └── dimensioning.py
├── llm/               # LLM parameter extraction
│   ├── extractor.py   # Claude Haiku integration
│   └── prompts.py     # System prompts
├── cli/               # Command-line interface
│   └── main.py
└── utils/             # Shared utilities
    ├── step_export.py
    └── dxf_export.py
```

**Example:** The `mounting_bracket` template:
```
templates/mounting_bracket.py:
- MountingBracketParams (Pydantic schema)
- MountingBracketTemplate.generate_3d() → build123d Part
- MountingBracketTemplate.generate_2d() → ezdxf Drawing
- MountingBracketTemplate.export_step() → .step file
```

---

## Technology Stack

### CAD Generation
| Technology | Version | Purpose |
|------------|---------|---------|
| **build123d** | 0.5+ | 3D parametric modeling with Pythonic API |
| **ezdxf** | 1.1+ | 2D DXF generation for AS 1100 layouts |
| **OpenCascade (OCP)** | 7.7+ | STEP export via build123d wrapper |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Type hints, async, performance |
| **FastAPI** | 0.100+ | REST API framework (Milestone 2) |
| **Pydantic** | 2.0+ | Schema validation and serialization |
| **SQLite** | 3.40+ | MVP database (→ PostgreSQL prod) |

### AI Integration
| Technology | Version | Purpose |
|------------|---------|---------|
| **Anthropic API** | Latest | Claude Haiku for parameter extraction |
| **langchain** | 0.1+ | LLM orchestration and prompting |

### Testing
| Technology | Version | Purpose |
|------------|---------|---------|
| **pytest** | 7.4+ | Unit and integration testing |
| **pytest-cov** | 4.1+ | Code coverage reporting |

---

## CAD Generation Architecture

### Directory Structure
```
src/cad_automation/templates/
├── base.py                     # BaseTemplate abstract class
├── mounting_bracket.py         # L-bracket, flat bracket templates
├── flange.py                   # Circular flange templates
└── enclosure.py                # Rectangular enclosure templates
```

### Template Pattern

All templates extend `BaseTemplate` and implement:

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel
from build123d import Part
from ezdxf.document import Drawing

class BaseTemplate(ABC):
    @abstractmethod
    def generate_3d(self, params: BaseModel) -> Part:
        """Generate build123d 3D model"""
        pass

    @abstractmethod
    def generate_2d(self, params: BaseModel) -> Drawing:
        """Generate ezdxf 2D drawing with AS 1100 layout"""
        pass

    def export_step(self, part: Part, path: str) -> None:
        """Export to STEP format"""
        pass

    def export_dxf(self, drawing: Drawing, path: str) -> None:
        """Export to DXF format"""
        pass
```

**Example:**
```python
class MountingBracketParams(BaseModel):
    width: float
    height: float
    thickness: float
    hole_diameter: float
    material: str

class MountingBracketTemplate(BaseTemplate):
    def generate_3d(self, params: MountingBracketParams) -> Part:
        # build123d code to generate L-bracket
        pass
```

---

## Validation Architecture

### Directory Structure
```
src/cad_automation/validators/
├── base.py                     # BaseValidator abstract class
├── sheet_layout.py             # AS 1100.101 sheet size, borders
├── line_standards.py           # AS 1100.101 line thickness, types
├── dimensioning.py             # AS 1100.101 dimension format
└── text_symbols.py             # AS 1100.101 text height, symbols
```

### Validation Pattern

All validators extend `BaseValidator` and return `ValidationResult`:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    passed: bool
    score: float  # 0.0 to 1.0
    errors: List[str]
    warnings: List[str]

class BaseValidator(ABC):
    weight: float  # For compliance rubric

    @abstractmethod
    def validate(self, drawing: Drawing) -> ValidationResult:
        """Validate drawing against AS 1100 standard"""
        pass
```

### Compliance Rubric

Target score: ≥95% weighted average across all validators

| Validator | Weight | Threshold | Automated |
|-----------|--------|-----------|-----------|
| Sheet Layout | 15% | 100% | ✅ Yes |
| Line Standards | 20% | 95% | ✅ Yes |
| Dimensioning | 25% | 90% | ✅ Yes |
| Text/Symbols | 15% | 95% | ✅ Yes |
| Projection/Views | 15% | N/A | ❌ Manual |
| Manufacturing Info | 10% | N/A | ❌ Manual |

---

## LLM Integration Architecture

### Directory Structure
```
src/cad_automation/llm/
├── extractor.py               # Claude Haiku integration
├── prompts.py                 # System prompts with AS 1100 context
└── confidence.py              # Confidence scoring logic
```

### Parameter Extraction Flow

```
User Spec → LLM Prompt → Claude Haiku API → JSON Response → Pydantic Validation → Confidence Score
                                                                                         ↓
                                                                           <70% → Manual Input
                                                                           ≥70% → Use Extracted Params
```

### Prompt Structure

```python
SYSTEM_PROMPT = """You are an expert in Australian Standard AS 1100 manufacturing drawings.
Extract dimensional parameters from user specifications for CAD template generation.

Standards context:
- AS 1100.101: General drawing principles
- AS 1100.201: Mechanical engineering drawing

Return JSON with:
- dimensions (width, height, thickness, etc.)
- material specification
- tolerance requirements
- confidence score (0.0-1.0)
"""
```

### Cost Management

- **API**: Claude Haiku (~$0.25/million input tokens, ~$1.25/million output tokens)
- **MVP Budget**: $300 for ~1M requests (conservative)
- **Operational**: $3-10/month for typical usage

---

## Database Schema

**Primary Database:** SQLite (MVP) → PostgreSQL (production)

**ORM:** SQLAlchemy 2.0+

### Core Tables

**1. templates**
```sql
CREATE TABLE templates (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  category TEXT NOT NULL,  -- 'bracket', 'flange', 'enclosure'
  parameter_schema JSON NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**2. drawings**
```sql
CREATE TABLE drawings (
  id INTEGER PRIMARY KEY,
  template_id INTEGER NOT NULL REFERENCES templates(id),
  parameters JSON NOT NULL,
  compliance_score REAL NOT NULL,
  step_path TEXT,
  dxf_path TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (template_id) REFERENCES templates(id)
);
```

**3. validation_results**
```sql
CREATE TABLE validation_results (
  id INTEGER PRIMARY KEY,
  drawing_id INTEGER NOT NULL REFERENCES drawings(id),
  validator_name TEXT NOT NULL,
  passed BOOLEAN NOT NULL,
  score REAL NOT NULL,
  errors JSON,
  warnings JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (drawing_id) REFERENCES drawings(id)
);
```

### Indexing Strategy
```sql
CREATE INDEX idx_drawings_template ON drawings(template_id);
CREATE INDEX idx_drawings_compliance ON drawings(compliance_score);
CREATE INDEX idx_validation_drawing ON validation_results(drawing_id);
```

---

## API Architecture

**RESTful API Design** (Milestone 2):
```
POST   /api/v1/generate              Generate drawing from template + params
GET    /api/v1/templates              List available templates
GET    /api/v1/templates/{id}         Get template details
POST   /api/v1/extract                Extract parameters from user spec (LLM)
GET    /api/v1/drawings/{id}          Get drawing details
GET    /api/v1/drawings/{id}/download Download STEP/DXF files
POST   /api/v1/validate               Validate drawing compliance
```

**Authentication:** Not required for MVP (CLI-only). JWT tokens for web UI (Milestone 2).

**Authorization:** Not applicable for single-user MVP.

---

## Security

### Authentication & Authorization

**MVP (CLI)**: No authentication required (local execution)

**Milestone 2 (Web UI)**: JWT tokens with FastAPI security middleware

### Data Security

**In Transit:**
- HTTPS for API endpoints (Milestone 2)
- TLS 1.3 for Anthropic API calls

**At Rest:**
- SQLite file permissions (600) for MVP
- PostgreSQL encryption at rest (production)

**Secrets Management:**
- Anthropic API key via environment variable `ANTHROPIC_API_KEY`
- No secrets in git repository (.env in .gitignore)

### API Security

**Rate Limiting:** Not required for MVP (single-user CLI)
**CORS:** Permissive for localhost (dev), restricted for production
**Input Validation:** Pydantic schemas for all user inputs
**Security Headers:** HSTS, X-Content-Type-Options, X-Frame-Options (Milestone 2)

---

## AS 1100 Compliance Strategy

### Standards Coverage

**AS 1100.101** - General Principles:
- Sheet sizes (A0-A4)
- Line types and thickness
- Dimensioning format
- Text height and font
- Title blocks and borders

**AS 1100.201** - Mechanical Engineering Drawing:
- View projection (first-angle)
- Section views and hatching
- Tolerance representation
- Surface finish symbols

### Automated Validation (70%+ target)

1. **Sheet Layout** (100% automated):
   - Sheet size compliance (A0-A4)
   - Border dimensions (20mm left, 10mm others)
   - Title block presence and format

2. **Line Standards** (95% automated):
   - Line thickness (0.18, 0.25, 0.35, 0.5, 0.7 mm)
   - Line types (continuous, dashed, chain)
   - Line usage (visible, hidden, center lines)

3. **Dimensioning** (90% automated):
   - Arrow size (3x line width)
   - Extension line gaps (1-2mm)
   - Dimension text height (3.5mm minimum)
   - Decimal places consistency

4. **Text/Symbols** (95% automated):
   - Text height (2.5, 3.5, 5, 7, 10, 14, 20mm)
   - Font compliance (ISO 3098)
   - Symbol library usage

### Manual Review (30%)

- View projection correctness
- Tolerance adequacy for manufacturing
- Completeness of manufacturing information

---

## Architecture Decision Records

### ADR-001: Use build123d Instead of CadQuery
**Date:** 2025-11-11
**Status:** Accepted

**Context:** Need Python-based 3D CAD library with OpenCascade backend for STEP export. CadQuery was initial consideration but build123d offers modern API.

**Decision:** Use build123d 0.5+ for 3D parametric modeling

**Consequences:**
- ✅ Modern Pythonic API with type hints
- ✅ Active development and community support
- ✅ Native STEP export via OCP wrapper
- ❌ Smaller ecosystem than CadQuery
- ❌ Breaking changes possible (pre-1.0)

**Alternatives Considered:**
- CadQuery (rejected - less Pythonic API, older design patterns)
- FreeCAD Python API (rejected - heavyweight, GUI dependencies)

---

### ADR-002: Use ezdxf Instead of dxfwrite
**Date:** 2025-11-11
**Status:** Accepted

**Context:** Need DXF generation library for AS 1100 compliant 2D drawings. dxfwrite is unmaintained.

**Decision:** Use ezdxf 1.1+ for 2D DXF generation

**Consequences:**
- ✅ Actively maintained (latest DXF specs)
- ✅ Comprehensive AS 1100 layout support
- ✅ Pure Python (no binary dependencies)
- ✅ Excellent documentation
- ❌ Learning curve for DXF internals

**Alternatives Considered:**
- dxfwrite (rejected - unmaintained since 2016)
- PyDXF (rejected - limited features)

---

### ADR-003: Use Claude Haiku Instead of GPT-4-mini
**Date:** 2025-11-11
**Status:** Accepted

**Context:** Need cost-effective LLM for parameter extraction from specifications. MVP budget is $300.

**Decision:** Use Claude Haiku API for parameter extraction

**Consequences:**
- ✅ Low cost (~$0.25/M input tokens)
- ✅ Good structured output support
- ✅ Fast response times
- ✅ Anthropic API familiarity
- ❌ Requires Anthropic API key

**Alternatives Considered:**
- GPT-4-mini (rejected - higher cost at scale)
- Open-source models (rejected - requires infrastructure)

---

### ADR-004: SQLite MVP → PostgreSQL Production
**Date:** 2025-11-11
**Status:** Accepted

**Context:** Need database for templates, drawings, validation results. MVP is single-user CLI.

**Decision:** Use SQLite for MVP, migrate to PostgreSQL for production

**Consequences:**
- ✅ Zero setup for MVP (file-based)
- ✅ SQLAlchemy abstracts DB differences
- ✅ PostgreSQL for concurrent users (production)
- ❌ Manual migration required
- ❌ JSON column support differences

**Alternatives Considered:**
- PostgreSQL from start (rejected - overkill for MVP)
- JSON files (rejected - no relational queries)

---

## Update History

| Date | Updated By | Changes |
|------|------------|---------|
| 2025-11-11 | Claude Code | Initial ARCHITECTURE.md creation |

---

**Note:** Update this document when making significant architectural changes. Add new ADRs when making impactful technical decisions. Review quarterly for accuracy.
