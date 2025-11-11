"""Unit tests for SheetLayoutValidator."""

from cad_automation.validators.sheet_layout import (
    AS1100_BORDER_LEFT,
    AS1100_BORDER_OTHERS,
    AS1100_SHEET_SIZES,
    SheetLayoutValidator,
)
from ezdxf import new


class TestSheetLayoutValidator:
    """Test AS 1100.101 sheet layout validation."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.validator = SheetLayoutValidator()

    def test_validator_properties(self) -> None:
        """Test validator has correct properties."""
        assert self.validator.weight == 0.15
        assert self.validator.name == "Sheet Layout Validator"
        assert self.validator.standard == "AS 1100.101"

    def test_valid_a4_landscape_drawing(self) -> None:
        """Test validation of compliant A4 landscape drawing."""
        # Create A4 landscape drawing (297x210mm)
        doc = new("R2010", setup=True)
        doc.header["$LIMMIN"] = (0, 0)
        doc.header["$LIMMAX"] = (297, 210)

        msp = doc.modelspace()

        # Add border (simplified - just a rectangle)
        border_points = [
            (AS1100_BORDER_LEFT, AS1100_BORDER_OTHERS),
            (297 - AS1100_BORDER_OTHERS, AS1100_BORDER_OTHERS),
            (297 - AS1100_BORDER_OTHERS, 210 - AS1100_BORDER_OTHERS),
            (AS1100_BORDER_LEFT, 210 - AS1100_BORDER_OTHERS),
            (AS1100_BORDER_LEFT, AS1100_BORDER_OTHERS),
        ]
        msp.add_lwpolyline(border_points, dxfattribs={"layer": "BORDER"})

        # Add title block text in bottom-right corner
        msp.add_text(
            "DRAWING TITLE",
            dxfattribs={
                "layer": "TEXT",
                "height": 5,
                "insert": (200, 20),  # Bottom-right region
            },
        )

        result = self.validator.validate(doc)

        assert result.passed is True
        assert result.score >= 0.8  # At least 80% passing
        assert len(result.errors) == 0
        assert result.checks_performed == 3
        assert result.checks_passed >= 2  # Sheet size + borders minimum

    def test_valid_a3_drawing(self) -> None:
        """Test validation of A3 sheet size."""
        doc = new("R2010", setup=True)
        doc.header["$LIMMIN"] = (0, 0)
        doc.header["$LIMMAX"] = (420, 297)  # A3

        msp = doc.modelspace()
        msp.add_lwpolyline([(20, 10), (410, 10), (410, 287), (20, 287), (20, 10)])

        result = self.validator.validate(doc)

        assert "A3" in str(result.warnings)  # Sheet size mentioned in warnings
        assert result.score > 0  # Some checks should pass

    def test_invalid_sheet_size(self) -> None:
        """Test validation fails for non-standard sheet size."""
        doc = new("R2010", setup=True)
        doc.header["$LIMMIN"] = (0, 0)
        doc.header["$LIMMAX"] = (500, 500)  # Invalid size

        result = self.validator.validate(doc)

        assert result.passed is False
        assert result.score < 1.0
        assert any("Invalid sheet size" in error for error in result.errors)

    def test_missing_drawing_limits(self) -> None:
        """Test validation fails gracefully when limits are missing."""
        doc = new("R2010")  # Don't use setup=True to avoid default limits
        # Explicitly delete drawing limits if they exist
        try:
            del doc.header["$LIMMIN"]
            del doc.header["$LIMMAX"]
        except KeyError:
            pass

        result = self.validator.validate(doc)

        assert result.passed is False
        assert result.score == 0.0
        assert any("Drawing limits" in error for error in result.errors)

    def test_missing_borders(self) -> None:
        """Test warning when no border entities found."""
        doc = new("R2010", setup=True)
        doc.header["$LIMMIN"] = (0, 0)
        doc.header["$LIMMAX"] = (297, 210)  # A4

        # Don't add any border entities

        result = self.validator.validate(doc)

        # Should warn about missing borders but not fail (warning only)
        assert any("border" in warning.lower() for warning in result.warnings)

    def test_missing_title_block(self) -> None:
        """Test warning when title block not found."""
        doc = new("R2010", setup=True)
        doc.header["$LIMMIN"] = (0, 0)
        doc.header["$LIMMAX"] = (297, 210)  # A4

        msp = doc.modelspace()
        # Add border but no title block
        msp.add_lwpolyline([(20, 10), (287, 10), (287, 200), (20, 200), (20, 10)])

        result = self.validator.validate(doc)

        # Should warn about missing title block
        assert any("title block" in warning.lower() for warning in result.warnings)

    def test_all_standard_sheet_sizes(self) -> None:
        """Test validation recognizes all AS 1100 sheet sizes."""
        for size_name, (width, height) in AS1100_SHEET_SIZES.items():
            doc = new("R2010", setup=True)
            doc.header["$LIMMIN"] = (0, 0)
            doc.header["$LIMMAX"] = (width, height)

            msp = doc.modelspace()
            msp.add_lwpolyline([(20, 10), (width - 10, 10)])

            result = self.validator.validate(doc)

            # Should recognize the sheet size (mentioned in warnings)
            assert any(
                size_name.replace("L", "") in str(result.warnings)
                for warning in [str(result.warnings)]
            ), f"Sheet size {size_name} not recognized"

    def test_score_calculation(self) -> None:
        """Test score is calculated correctly."""
        doc = new("R2010", setup=True)
        doc.header["$LIMMIN"] = (0, 0)
        doc.header["$LIMMAX"] = (297, 210)  # Valid A4

        msp = doc.modelspace()
        msp.add_lwpolyline([(20, 10), (287, 10)])  # Border
        msp.add_text("TITLE", dxfattribs={"insert": (200, 20)})  # Title block

        result = self.validator.validate(doc)

        # Score should be checks_passed / checks_performed
        expected_score = result.checks_passed / result.checks_performed
        assert result.score == expected_score
        assert 0.0 <= result.score <= 1.0

    def test_tolerance_in_sheet_size(self) -> None:
        """Test that small variations in sheet size are accepted (within tolerance)."""
        doc = new("R2010", setup=True)
        doc.header["$LIMMIN"] = (0, 0)
        # A4 is 297x210, test with 297.5x210.5 (within 1mm tolerance)
        doc.header["$LIMMAX"] = (297.5, 210.5)

        msp = doc.modelspace()
        msp.add_lwpolyline([(20, 10), (287, 10)])

        result = self.validator.validate(doc)

        # Should still recognize as A4
        assert "A4" in str(result.warnings)
