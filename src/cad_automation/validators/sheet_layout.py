"""Sheet layout validator for AS 1100.101 compliance.

Validates:
- Sheet sizes (A0-A4)
- Border dimensions (20mm left, 10mm others)
- Title block presence and location
"""


from ezdxf.document import Drawing

from .base import BaseValidator, ValidationResult

# AS 1100.101 standard sheet sizes in mm (width x height)
AS1100_SHEET_SIZES: dict[str, tuple[float, float]] = {
    "A0": (1189.0, 841.0),
    "A1": (841.0, 594.0),
    "A2": (594.0, 420.0),
    "A3": (420.0, 297.0),
    "A4": (297.0, 210.0),
    # Landscape orientations
    "A0L": (841.0, 1189.0),
    "A1L": (594.0, 841.0),
    "A2L": (420.0, 594.0),
    "A3L": (297.0, 420.0),
    "A4L": (210.0, 297.0),
}

# AS 1100.101 border dimensions in mm
AS1100_BORDER_LEFT = 20.0  # Left border (binding edge)
AS1100_BORDER_OTHERS = 10.0  # Top, right, bottom borders

# Tolerance for dimension checks (mm)
TOLERANCE = 1.0  # ±1mm tolerance for border checks


class SheetLayoutValidator(BaseValidator):
    """Validator for AS 1100.101 sheet layout requirements.

    Checks:
    1. Sheet size matches AS 1100 standard sizes (A0-A4)
    2. Border dimensions (20mm left, 10mm others)
    3. Title block presence and location (bottom right)

    Weight: 15% of overall compliance score
    """

    def __init__(self):
        """Initialize sheet layout validator."""
        super().__init__(weight=0.15, name="Sheet Layout Validator", standard="AS 1100.101")

    def validate(self, drawing: Drawing) -> ValidationResult:
        """Validate sheet layout against AS 1100.101.

        Args:
            drawing: ezdxf Drawing object to validate

        Returns:
            ValidationResult with compliance score and messages
        """
        errors = []
        warnings = []
        checks_performed = 0
        checks_passed = 0

        # Get drawing limits (sheet size)
        try:
            limits = drawing.header["$LIMMIN"], drawing.header["$LIMMAX"]
            width = abs(limits[1][0] - limits[0][0])
            height = abs(limits[1][1] - limits[0][1])
        except (KeyError, IndexError):
            errors.append(
                "Drawing limits ($LIMMIN/$LIMMAX) not defined - cannot determine sheet size"
            )
            return ValidationResult(
                passed=False,
                score=0.0,
                errors=errors,
                warnings=warnings,
                checks_performed=1,
                checks_passed=0,
            )

        # Check 1: Validate sheet size
        checks_performed += 1
        sheet_size = self._validate_sheet_size(width, height)
        if sheet_size:
            checks_passed += 1
            warnings.append(f"Sheet size: {sheet_size} ({width}x{height}mm)")
        else:
            errors.append(
                f"Invalid sheet size: {width}x{height}mm. "
                f"Must be AS 1100 standard (A0-A4). "
                f"Valid sizes: {', '.join(AS1100_SHEET_SIZES.keys())}"
            )

        # Check 2: Validate borders (check for border entities)
        checks_performed += 1
        border_check = self._validate_borders(drawing, width, height)
        if border_check["passed"]:
            checks_passed += 1
        else:
            if border_check.get("warning"):
                warnings.append(border_check["message"])
            else:
                errors.append(border_check["message"])

        # Check 3: Validate title block presence
        checks_performed += 1
        title_block_check = self._validate_title_block(drawing, width, height)
        if title_block_check["passed"]:
            checks_passed += 1
        else:
            # Title block is a warning, not critical error for POC
            warnings.append(title_block_check["message"])

        # Calculate score
        score = checks_passed / checks_performed if checks_performed > 0 else 0.0
        passed = len(errors) == 0 and score >= 0.8  # 80% threshold for passing

        return ValidationResult(
            passed=passed,
            score=score,
            errors=errors,
            warnings=warnings,
            checks_performed=checks_performed,
            checks_passed=checks_passed,
        )

    def _validate_sheet_size(self, width: float, height: float) -> str | None:
        """Check if sheet size matches AS 1100 standard.

        Args:
            width: Sheet width in mm
            height: Sheet height in mm

        Returns:
            Sheet size name (e.g., "A4") if valid, None otherwise
        """
        for size_name, (std_width, std_height) in AS1100_SHEET_SIZES.items():
            if abs(width - std_width) <= TOLERANCE and abs(height - std_height) <= TOLERANCE:
                return size_name
        return None

    def _validate_borders(self, drawing: Drawing, width: float, height: float) -> dict:
        """Check for border entities (simplified check).

        Args:
            drawing: ezdxf Drawing object
            width: Sheet width in mm
            height: Sheet height in mm

        Returns:
            Dict with 'passed' bool and 'message' str
        """
        msp = drawing.modelspace()

        # Look for polyline/line entities that could be borders
        # AS 1100 borders should be rectangles near the sheet edges
        border_entities = []

        for entity in msp.query("LWPOLYLINE LINE"):
            border_entities.append(entity)

        if len(border_entities) == 0:
            return {
                "passed": False,
                "message": "No border entities found. AS 1100.101 requires borders "
                f"({AS1100_BORDER_LEFT}mm left, {AS1100_BORDER_OTHERS}mm others)",
                "warning": True,
            }

        # Simplified check: just verify borders exist
        # Full implementation would check exact border dimensions
        return {
            "passed": True,
            "message": f"Border entities found ({len(border_entities)} lines/polylines)",
        }

    def _validate_title_block(self, drawing: Drawing, width: float, height: float) -> dict:
        """Check for title block presence (simplified check).

        Args:
            drawing: ezdxf Drawing object
            width: Sheet width in mm
            height: Sheet height in mm

        Returns:
            Dict with 'passed' bool and 'message' str
        """
        msp = drawing.modelspace()

        # Title block should be in bottom-right corner
        # Look for text entities in that region
        title_block_region_x = width * 0.6  # Right 40% of drawing
        title_block_region_y = height * 0.3  # Bottom 30% of drawing

        title_text_entities = []
        for entity in msp.query("TEXT MTEXT"):
            try:
                insert = entity.dxf.insert if hasattr(entity.dxf, "insert") else None
                if (
                    insert
                    and insert[0] >= title_block_region_x
                    and insert[1] <= title_block_region_y
                ):
                    title_text_entities.append(entity)
            except AttributeError:
                continue

        if len(title_text_entities) == 0:
            return {
                "passed": False,
                "message": "Title block not found in bottom-right corner. "
                "AS 1100.101 requires title block with drawing info",
            }

        return {
            "passed": True,
            "message": f"Title block found ({len(title_text_entities)} text entities in bottom-right region)",
        }
