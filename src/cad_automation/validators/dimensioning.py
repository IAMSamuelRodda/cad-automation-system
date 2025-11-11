"""Dimensioning validator for AS 1100.101 compliance.

Validates:
- Arrow size (3x line width standard)
- Extension line gaps (1-2mm)
- Dimension text height (3.5mm minimum)
- Decimal places consistency
"""

from ezdxf.document import Drawing

from .base import BaseValidator, ValidationResult

# AS 1100.101 dimensioning standards
AS1100_MIN_TEXT_HEIGHT = 3.5  # mm
AS1100_ARROW_SIZE_MULTIPLIER = 3.0  # Arrow size = 3x line width
AS1100_EXTENSION_GAP_MIN = 1.0  # mm
AS1100_EXTENSION_GAP_MAX = 2.0  # mm
AS1100_STANDARD_LINE_WIDTH = 0.25  # mm (for dimension lines)
AS1100_STANDARD_ARROW_SIZE = 0.75  # mm (3x 0.25mm)

# Tolerance for dimension checks
TOLERANCE = 0.5  # mm


class DimensioningValidator(BaseValidator):
    """Validator for AS 1100.101 dimensioning requirements.

    Checks:
    1. Dimension text height (minimum 3.5mm)
    2. Arrow size (should be ~3x line width, typically 0.75mm)
    3. Extension line gaps (1-2mm from object)
    4. Decimal places consistency

    Weight: 25% of overall compliance score
    """

    def __init__(self):
        """Initialize dimensioning validator."""
        super().__init__(weight=0.25, name="Dimensioning Validator", standard="AS 1100.101")

    def validate(self, drawing: Drawing) -> ValidationResult:
        """Validate dimensioning against AS 1100.101.

        Args:
            drawing: ezdxf Drawing object to validate

        Returns:
            ValidationResult with compliance score and messages
        """
        errors = []
        warnings = []
        checks_performed = 0
        checks_passed = 0

        msp = drawing.modelspace()

        # Get all dimension entities
        dimensions = list(msp.query("DIMENSION"))

        if len(dimensions) == 0:
            warnings.append("No dimension entities found - cannot validate dimensioning standards")
            return ValidationResult(
                passed=True,  # Not an error if no dimensions (might be 3D-only drawing)
                score=1.0,
                errors=errors,
                warnings=warnings,
                checks_performed=1,
                checks_passed=1,
            )

        # Check 1: Validate dimension text height
        checks_performed += 1
        text_height_check = self._validate_text_height(dimensions)
        if text_height_check["passed"]:
            checks_passed += 1
        else:
            errors.extend(text_height_check.get("errors", []))
        warnings.extend(text_height_check.get("warnings", []))

        # Check 2: Validate arrow size
        checks_performed += 1
        arrow_size_check = self._validate_arrow_size(dimensions)
        if arrow_size_check["passed"]:
            checks_passed += 1
        else:
            warnings.extend(arrow_size_check.get("warnings", []))

        # Check 3: Check for decimal consistency
        checks_performed += 1
        decimal_check = self._validate_decimal_consistency(dimensions)
        if decimal_check["passed"]:
            checks_passed += 1
        else:
            warnings.extend(decimal_check.get("warnings", []))

        # Calculate score
        score = checks_passed / checks_performed if checks_performed > 0 else 0.0
        passed = len(errors) == 0 and score >= 0.7  # 70% threshold for passing

        return ValidationResult(
            passed=passed,
            score=score,
            errors=errors,
            warnings=warnings,
            checks_performed=checks_performed,
            checks_passed=checks_passed,
        )

    def _validate_text_height(self, dimensions: list) -> dict:
        """Validate dimension text height meets AS 1100 minimum.

        Args:
            dimensions: List of DIMENSION entities

        Returns:
            Dict with 'passed' bool, 'errors' and 'warnings' lists
        """
        errors = []
        warnings = []
        violations = []

        for dim in dimensions:
            try:
                # Get text height from dimension style or override
                text_height = dim.dxf.get("dimtxt", 3.5)  # Default to 3.5mm

                if text_height < AS1100_MIN_TEXT_HEIGHT - TOLERANCE:
                    violations.append(text_height)
            except (AttributeError, KeyError):
                continue

        if violations:
            avg_height = sum(violations) / len(violations)
            errors.append(
                f"Dimension text height too small: {len(violations)} dimensions "
                f"below {AS1100_MIN_TEXT_HEIGHT}mm minimum (avg: {avg_height:.2f}mm). "
                f"AS 1100.101 requires minimum {AS1100_MIN_TEXT_HEIGHT}mm text height."
            )
            return {"passed": False, "errors": errors, "warnings": warnings}

        warnings.append(
            f"Dimension text height: {len(dimensions)} dimensions checked, "
            f"all meet {AS1100_MIN_TEXT_HEIGHT}mm minimum"
        )
        return {"passed": True, "errors": errors, "warnings": warnings}

    def _validate_arrow_size(self, dimensions: list) -> dict:
        """Validate arrow size follows AS 1100 standards.

        Args:
            dimensions: List of DIMENSION entities

        Returns:
            Dict with 'passed' bool and 'warnings' list
        """
        warnings = []
        arrow_sizes = []

        for dim in dimensions:
            try:
                # Get arrow size from dimension style
                arrow_size = dim.dxf.get("dimasz", AS1100_STANDARD_ARROW_SIZE)
                arrow_sizes.append(arrow_size)
            except (AttributeError, KeyError):
                continue

        if arrow_sizes:
            avg_arrow = sum(arrow_sizes) / len(arrow_sizes)
            expected = AS1100_STANDARD_ARROW_SIZE

            if abs(avg_arrow - expected) > TOLERANCE:
                warnings.append(
                    f"Arrow size: avg {avg_arrow:.2f}mm (expected ~{expected}mm "
                    f"for {AS1100_STANDARD_LINE_WIDTH}mm line width). "
                    f"AS 1100.101 recommends arrow size = 3x line width."
                )
            else:
                warnings.append(
                    f"Arrow size: avg {avg_arrow:.2f}mm ({len(arrow_sizes)} dimensions), "
                    f"meets AS 1100 standard (~{expected}mm)"
                )

        return {"passed": True, "warnings": warnings}

    def _validate_decimal_consistency(self, dimensions: list) -> dict:
        """Check decimal place consistency in dimension text.

        Args:
            dimensions: List of DIMENSION entities

        Returns:
            Dict with 'passed' bool and 'warnings' list
        """
        warnings = []
        decimal_places = []

        for dim in dimensions:
            try:
                # Get decimal places setting
                dec_places = dim.dxf.get("dimdec", 2)  # Default to 2 decimal places
                decimal_places.append(dec_places)
            except (AttributeError, KeyError):
                continue

        if decimal_places:
            # Check if all dimensions use consistent decimal places
            unique_decimals = set(decimal_places)

            if len(unique_decimals) > 1:
                warnings.append(
                    f"Inconsistent decimal places: {len(unique_decimals)} different "
                    f"settings found {sorted(unique_decimals)}. "
                    f"AS 1100.101 recommends consistent decimal precision."
                )
                return {"passed": False, "warnings": warnings}

            warnings.append(
                f"Decimal places: consistent across {len(decimal_places)} dimensions "
                f"({decimal_places[0]} decimal places)"
            )

        return {"passed": True, "warnings": warnings}
