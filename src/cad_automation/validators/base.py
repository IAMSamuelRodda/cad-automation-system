"""Base validator abstract class for AS 1100 compliance validation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ezdxf.document import Drawing


@dataclass
class ValidationResult:
    """Result of a validation check.

    Attributes:
        passed: Whether validation passed overall
        score: Compliance score (0.0 to 1.0)
        errors: List of critical errors (violations)
        warnings: List of warnings (recommendations)
        checks_performed: Number of validation checks performed
        checks_passed: Number of checks that passed
    """

    passed: bool
    score: float
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks_performed: int = 0
    checks_passed: int = 0

    def __post_init__(self):
        """Validate score is in valid range."""
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"Score must be between 0.0 and 1.0, got {self.score}")


class BaseValidator(ABC):
    """Abstract base class for AS 1100 compliance validators.

    All validators must implement the validate() method to check
    DXF drawings against specific AS 1100 standards.

    Attributes:
        weight: Weight for compliance rubric (0.0 to 1.0)
        name: Human-readable validator name
        standard: AS 1100 standard section (e.g., "AS 1100.101")
    """

    def __init__(self, weight: float, name: str, standard: str):
        """Initialize validator.

        Args:
            weight: Weight for compliance rubric (0.0 to 1.0)
            name: Human-readable validator name
            standard: AS 1100 standard section
        """
        if not 0.0 <= weight <= 1.0:
            raise ValueError(f"Weight must be between 0.0 and 1.0, got {weight}")

        self.weight = weight
        self.name = name
        self.standard = standard

    @abstractmethod
    def validate(self, drawing: Drawing) -> ValidationResult:
        """Validate drawing against AS 1100 standard.

        Args:
            drawing: ezdxf Drawing object to validate

        Returns:
            ValidationResult with passed status, score, and messages
        """
        pass

    def __repr__(self) -> str:
        """String representation of validator."""
        return f"{self.__class__.__name__}(weight={self.weight}, standard='{self.standard}')"
