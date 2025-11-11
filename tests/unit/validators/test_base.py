"""Unit tests for base validator classes."""

import pytest
from cad_automation.validators.base import BaseValidator, ValidationResult


class TestValidationResult:
    """Test ValidationResult dataclass."""

    def test_valid_result(self) -> None:
        """Test creating a valid ValidationResult."""
        result = ValidationResult(
            passed=True,
            score=0.95,
            errors=[],
            warnings=["Minor issue"],
            checks_performed=10,
            checks_passed=9,
        )
        assert result.passed is True
        assert result.score == 0.95
        assert len(result.errors) == 0
        assert len(result.warnings) == 1
        assert result.checks_performed == 10
        assert result.checks_passed == 9

    def test_invalid_score_too_high(self) -> None:
        """Test that score > 1.0 raises ValueError."""
        with pytest.raises(ValueError, match="Score must be between 0.0 and 1.0"):
            ValidationResult(passed=True, score=1.5, errors=[], warnings=[])

    def test_invalid_score_negative(self) -> None:
        """Test that score < 0.0 raises ValueError."""
        with pytest.raises(ValueError, match="Score must be between 0.0 and 1.0"):
            ValidationResult(passed=False, score=-0.1, errors=[], warnings=[])

    def test_default_lists(self) -> None:
        """Test that errors and warnings default to empty lists."""
        result = ValidationResult(passed=True, score=1.0)
        assert result.errors == []
        assert result.warnings == []
        assert result.checks_performed == 0
        assert result.checks_passed == 0


class TestBaseValidator:
    """Test BaseValidator abstract class."""

    def test_init_valid_weight(self) -> None:
        """Test creating validator with valid weight."""

        class DummyValidator(BaseValidator):
            def validate(self, drawing):
                return ValidationResult(passed=True, score=1.0)

        validator = DummyValidator(weight=0.15, name="Test", standard="AS 1100.101")
        assert validator.weight == 0.15
        assert validator.name == "Test"
        assert validator.standard == "AS 1100.101"

    def test_init_invalid_weight_too_high(self) -> None:
        """Test that weight > 1.0 raises ValueError."""

        class DummyValidator(BaseValidator):
            def validate(self, drawing):
                return ValidationResult(passed=True, score=1.0)

        with pytest.raises(ValueError, match="Weight must be between 0.0 and 1.0"):
            DummyValidator(weight=1.5, name="Test", standard="AS 1100.101")

    def test_init_invalid_weight_negative(self) -> None:
        """Test that weight < 0.0 raises ValueError."""

        class DummyValidator(BaseValidator):
            def validate(self, drawing):
                return ValidationResult(passed=True, score=1.0)

        with pytest.raises(ValueError, match="Weight must be between 0.0 and 1.0"):
            DummyValidator(weight=-0.1, name="Test", standard="AS 1100.101")

    def test_repr(self) -> None:
        """Test string representation."""

        class DummyValidator(BaseValidator):
            def validate(self, drawing):
                return ValidationResult(passed=True, score=1.0)

        validator = DummyValidator(weight=0.15, name="Test", standard="AS 1100.101")
        repr_str = repr(validator)
        assert "DummyValidator" in repr_str
        assert "0.15" in repr_str
        assert "AS 1100.101" in repr_str
