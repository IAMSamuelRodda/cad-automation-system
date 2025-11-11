"""Unit tests for DimensioningValidator."""

from cad_automation.validators.dimensioning import (
    DimensioningValidator,
)
from ezdxf import new


class TestDimensioningValidator:
    """Test AS 1100.101 dimensioning validation."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.validator = DimensioningValidator()

    def test_validator_properties(self) -> None:
        """Test validator has correct properties."""
        assert self.validator.weight == 0.25
        assert self.validator.name == "Dimensioning Validator"
        assert self.validator.standard == "AS 1100.101"

    def test_no_dimensions_passes(self) -> None:
        """Test validation passes when no dimensions present."""
        doc = new("R2010", setup=True)

        result = self.validator.validate(doc)

        assert result.passed is True
        assert result.score == 1.0
        assert len(result.errors) == 0
        assert any("No dimension entities" in warning for warning in result.warnings)

    def test_valid_dimensions(self) -> None:
        """Test validation of compliant dimensions."""
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        # Add dimension with valid properties using override
        dim_override = msp.add_linear_dim(
            base=(50, 20),
            p1=(10, 10),
            p2=(90, 10),
            override={"dimtxt": 3.5, "dimasz": 0.75, "dimdec": 2},
        )
        dim_override.render()

        result = self.validator.validate(doc)

        assert result.passed is True
        assert result.score >= 0.7
        assert len(result.errors) == 0
        assert result.checks_performed == 3

    def test_text_height_too_small(self) -> None:
        """Test validation fails for text height below minimum."""
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        # Add dimension with text too small
        dim_override = msp.add_linear_dim(
            base=(50, 20),
            p1=(10, 10),
            p2=(90, 10),
            override={"dimtxt": 2.0, "dimasz": 0.75, "dimdec": 2},
        )
        dim_override.render()

        result = self.validator.validate(doc)

        assert result.passed is False
        assert result.score < 1.0
        assert any("text height too small" in error.lower() for error in result.errors)

    def test_multiple_dimensions_text_height(self) -> None:
        """Test validation with multiple dimensions."""
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        # Add multiple dimensions
        for i in range(3):
            dim_override = msp.add_linear_dim(
                base=(50 + i * 20, 20),
                p1=(10, 10 + i * 10),
                p2=(90, 10 + i * 10),
                override={"dimtxt": 3.5, "dimasz": 0.75, "dimdec": 2},
            )
            dim_override.render()

        result = self.validator.validate(doc)

        assert result.passed is True
        assert any("3 dimensions checked" in warning for warning in result.warnings)

    def test_arrow_size_warning(self) -> None:
        """Test warning for non-standard arrow size."""
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        dim_override = msp.add_linear_dim(
            base=(50, 20),
            p1=(10, 10),
            p2=(90, 10),
            override={"dimtxt": 3.5, "dimasz": 2.0, "dimdec": 2},
        )
        dim_override.render()

        result = self.validator.validate(doc)

        # Should still pass but with warning
        assert result.passed is True
        assert any(
            "arrow size" in warning.lower() and "expected" in warning.lower()
            for warning in result.warnings
        )

    def test_decimal_consistency_pass(self) -> None:
        """Test validation passes with consistent decimal places."""
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        # All dimensions use 2 decimal places
        for i in range(3):
            dim_override = msp.add_linear_dim(
                base=(50 + i * 20, 20),
                p1=(10, 10 + i * 10),
                p2=(90, 10 + i * 10),
                override={"dimtxt": 3.5, "dimasz": 0.75, "dimdec": 2},
            )
            dim_override.render()

        result = self.validator.validate(doc)

        assert result.passed is True
        assert any(
            "consistent" in warning.lower() and "decimal" in warning.lower()
            for warning in result.warnings
        )

    def test_decimal_consistency_fail(self) -> None:
        """Test validation warns about inconsistent decimal places."""
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        # Mix of decimal places
        for i, dec_places in enumerate([2, 3, 2]):
            dim_override = msp.add_linear_dim(
                base=(50 + i * 20, 20),
                p1=(10, 10 + i * 10),
                p2=(90, 10 + i * 10),
                override={"dimtxt": 3.5, "dimasz": 0.75, "dimdec": dec_places},
            )
            dim_override.render()

        result = self.validator.validate(doc)

        # Should still pass overall but warn about inconsistency
        assert result.score < 1.0  # One check failed
        assert any("inconsistent decimal" in warning.lower() for warning in result.warnings)

    def test_score_calculation(self) -> None:
        """Test score calculation with mixed results."""
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        # Add dimension that passes text height but has warnings
        dim_override = msp.add_linear_dim(
            base=(50, 20),
            p1=(10, 10),
            p2=(90, 10),
            override={"dimtxt": 3.5, "dimasz": 2.0, "dimdec": 2},
        )
        dim_override.render()

        result = self.validator.validate(doc)

        # Score should be checks_passed / checks_performed
        expected_score = result.checks_passed / result.checks_performed
        assert result.score == expected_score
        assert 0.0 <= result.score <= 1.0

    def test_tolerance_in_text_height(self) -> None:
        """Test that tolerance is applied to text height checks."""
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        # Text height slightly below minimum but within tolerance
        dim_override = msp.add_linear_dim(
            base=(50, 20),
            p1=(10, 10),
            p2=(90, 10),
            override={"dimtxt": 3.2, "dimasz": 0.75, "dimdec": 2},
        )
        dim_override.render()

        result = self.validator.validate(doc)

        # Should pass because within tolerance
        assert len(result.errors) == 0

    def test_multiple_violations(self) -> None:
        """Test multiple text height violations."""
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        # Add multiple dimensions with small text
        for i in range(5):
            dim_override = msp.add_linear_dim(
                base=(50 + i * 20, 20),
                p1=(10, 10 + i * 10),
                p2=(90, 10 + i * 10),
                override={"dimtxt": 2.0, "dimasz": 0.75, "dimdec": 2},
            )
            dim_override.render()

        result = self.validator.validate(doc)

        assert result.passed is False
        # Should report 5 violations
        assert any("5 dimensions" in error for error in result.errors)
