"""Base template abstract class for parametric CAD generation."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from build123d import Part, export_step
from ezdxf.document import Drawing
from pydantic import BaseModel


class TemplateParams(BaseModel):
    """Base parameter schema for all templates."""

    pass


class BaseTemplate(ABC):
    """Abstract base class for parametric CAD templates.

    All templates must implement:
    - generate_3d(): Create build123d Part from parameters
    - generate_2d(): Create ezdxf Drawing with AS 1100 layout from parameters
    """

    @abstractmethod
    def generate_3d(self, params: TemplateParams) -> Part:
        """Generate 3D model using build123d.

        Args:
            params: Template-specific parameters (Pydantic model)

        Returns:
            build123d Part object
        """
        pass

    @abstractmethod
    def generate_2d(self, params: TemplateParams) -> Drawing:
        """Generate 2D drawing with AS 1100 layout using ezdxf.

        Args:
            params: Template-specific parameters (Pydantic model)

        Returns:
            ezdxf Drawing object with AS 1100 compliant layout
        """
        pass

    def export_step(self, part: Part, path: Path) -> None:
        """Export build123d Part to STEP format.

        Args:
            part: build123d Part object
            path: Output file path (.step or .stp)
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        export_step(part, str(path))

    def export_dxf(self, drawing: Drawing, path: Path) -> None:
        """Export ezdxf Drawing to DXF format.

        Args:
            drawing: ezdxf Drawing object
            path: Output file path (.dxf)
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        drawing.saveas(str(path))
