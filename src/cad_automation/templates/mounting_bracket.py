"""Mounting bracket parametric template - L-bracket and flat bracket variants."""

from build123d import *
from ezdxf import new
from ezdxf.document import Drawing
from pydantic import Field

from .base import BaseTemplate, TemplateParams


class MountingBracketParams(TemplateParams):
    """Parameters for mounting bracket generation.

    Supports L-bracket (90-degree) and flat bracket variants.
    """

    width: float = Field(gt=0, description="Bracket width in mm")
    height: float = Field(gt=0, description="Bracket height in mm")
    thickness: float = Field(gt=0, description="Material thickness in mm")
    hole_diameter: float = Field(gt=0, description="Mounting hole diameter in mm")
    hole_count: int = Field(ge=1, le=10, description="Number of mounting holes")
    material: str = Field(default="Steel", description="Material specification")
    bracket_type: str = Field(
        default="L", description="Bracket type: 'L' for L-bracket, 'flat' for flat"
    )


class MountingBracketTemplate(BaseTemplate):
    """Parametric mounting bracket template.

    Generates L-brackets and flat brackets with mounting holes.
    """

    def generate_3d(self, params: MountingBracketParams) -> Part:
        """Generate 3D L-bracket or flat bracket.

        Args:
            params: Mounting bracket parameters

        Returns:
            build123d Part object
        """
        if params.bracket_type.lower() == "l":
            return self._generate_l_bracket_3d(params)
        else:
            return self._generate_flat_bracket_3d(params)

    def _generate_l_bracket_3d(self, params: MountingBracketParams) -> Part:
        """Generate 3D L-bracket (90-degree angle)."""
        with BuildPart() as bracket:
            # Create vertical plate
            with BuildSketch():
                Rectangle(params.width, params.height)

            extrude(amount=params.thickness)

            # Create horizontal plate
            with BuildSketch(Plane.XY.offset(0)):
                Rectangle(params.width, params.height)

            extrude(amount=params.thickness)

            # Create mounting holes in vertical plate
            hole_spacing = params.width / (params.hole_count + 1)
            for i in range(1, params.hole_count + 1):
                x_pos = -params.width / 2 + i * hole_spacing
                y_pos = params.height / 2

                with BuildSketch(Plane.XY.offset(params.thickness / 2)):
                    with Locations((x_pos, y_pos)):
                        Circle(params.hole_diameter / 2)

                extrude(amount=-params.thickness, mode=Mode.SUBTRACT)

            # Create mounting holes in horizontal plate
            for i in range(1, params.hole_count + 1):
                x_pos = -params.width / 2 + i * hole_spacing
                y_pos = -params.height / 2

                with BuildSketch(Plane.XY.offset(params.thickness / 2)):
                    with Locations((x_pos, y_pos)):
                        Circle(params.hole_diameter / 2)

                extrude(amount=-params.thickness, mode=Mode.SUBTRACT)

        return bracket.part

    def _generate_flat_bracket_3d(self, params: MountingBracketParams) -> Part:
        """Generate 3D flat bracket (single plate)."""
        with BuildPart() as bracket:
            # Create flat plate
            with BuildSketch():
                Rectangle(params.width, params.height)

            extrude(amount=params.thickness)

            # Create mounting holes
            hole_spacing = params.width / (params.hole_count + 1)
            for i in range(1, params.hole_count + 1):
                x_pos = -params.width / 2 + i * hole_spacing
                y_pos = 0

                with BuildSketch(Plane.XY.offset(params.thickness / 2)):
                    with Locations((x_pos, y_pos)):
                        Circle(params.hole_diameter / 2)

                extrude(amount=-params.thickness, mode=Mode.SUBTRACT)

        return bracket.part

    def generate_2d(self, params: MountingBracketParams) -> Drawing:
        """Generate 2D drawing with AS 1100 layout.

        Creates orthographic views (front, side) with dimensions.

        Args:
            params: Mounting bracket parameters

        Returns:
            ezdxf Drawing with AS 1100 compliant layout
        """
        # Create new DXF document (AS 1100 uses A4 landscape = 297x210mm)
        doc = new("R2010", setup=True)
        msp = doc.modelspace()

        # AS 1100.101 line thickness standards (mm)
        # Visible outlines: 0.5mm, Hidden lines: 0.25mm, Dimension lines: 0.25mm
        doc.layers.add("OUTLINE", color=7, linetype="CONTINUOUS")  # White, solid
        doc.layers.add("HIDDEN", color=8, linetype="DASHED")  # Grey, dashed
        doc.layers.add("DIMENSIONS", color=3, linetype="CONTINUOUS")  # Green, solid
        doc.layers.add("TEXT", color=7, linetype="CONTINUOUS")  # White, solid

        # Draw front view (looking at vertical plate for L-bracket)
        front_view_origin = (50, 150)  # Offset from border
        self._draw_front_view(msp, params, front_view_origin)

        # Draw side view
        side_view_origin = (200, 150)
        self._draw_side_view(msp, params, side_view_origin)

        # Add title block (simplified AS 1100 format)
        self._add_title_block(doc, msp, params)

        # Add dimensions
        self._add_dimensions(msp, params, front_view_origin, side_view_origin)

        return doc

    def _draw_front_view(
        self, msp, params: MountingBracketParams, origin: tuple[float, float]
    ) -> None:
        """Draw front view of bracket."""
        x0, y0 = origin

        # Draw outline rectangle (vertical plate)
        msp.add_lwpolyline(
            [
                (x0, y0),
                (x0 + params.width, y0),
                (x0 + params.width, y0 + params.height),
                (x0, y0 + params.height),
                (x0, y0),
            ],
            dxfattribs={"layer": "OUTLINE"},
        )

        # Draw mounting holes
        hole_spacing = params.width / (params.hole_count + 1)
        for i in range(1, params.hole_count + 1):
            x_center = x0 + i * hole_spacing
            y_center = y0 + params.height / 2
            msp.add_circle(
                (x_center, y_center),
                radius=params.hole_diameter / 2,
                dxfattribs={"layer": "OUTLINE"},
            )

    def _draw_side_view(
        self, msp, params: MountingBracketParams, origin: tuple[float, float]
    ) -> None:
        """Draw side view showing thickness."""
        x0, y0 = origin

        # Draw thickness rectangle
        msp.add_lwpolyline(
            [
                (x0, y0),
                (x0 + params.thickness, y0),
                (x0 + params.thickness, y0 + params.height),
                (x0, y0 + params.height),
                (x0, y0),
            ],
            dxfattribs={"layer": "OUTLINE"},
        )

    def _add_dimensions(
        self,
        msp,
        params: MountingBracketParams,
        front_origin: tuple[float, float],
        side_origin: tuple[float, float],
    ) -> None:
        """Add AS 1100 compliant dimensions."""
        x0, y0 = front_origin

        # Width dimension (above front view)
        msp.add_linear_dim(
            base=(x0 + params.width / 2, y0 + params.height + 10),
            p1=(x0, y0 + params.height + 5),
            p2=(x0 + params.width, y0 + params.height + 5),
            dimstyle="EZDXF",
            dxfattribs={"layer": "DIMENSIONS"},
        )

        # Height dimension (right of front view)
        msp.add_linear_dim(
            base=(x0 + params.width + 10, y0 + params.height / 2),
            p1=(x0 + params.width + 5, y0),
            p2=(x0 + params.width + 5, y0 + params.height),
            angle=90,
            dimstyle="EZDXF",
            dxfattribs={"layer": "DIMENSIONS"},
        )

        # Hole diameter dimension (leader to first hole)
        hole_x = x0 + params.width / (params.hole_count + 1)
        hole_y = y0 + params.height / 2
        msp.add_text(
            f"Ø{params.hole_diameter}",
            dxfattribs={
                "layer": "TEXT",
                "height": 3.5,  # AS 1100.101 minimum text height 3.5mm
                "insert": (hole_x + 10, hole_y),
            },
        )

    def _add_title_block(self, doc: Drawing, msp, params: MountingBracketParams) -> None:
        """Add simplified AS 1100 title block."""
        # AS 1100.101 title block location: bottom right corner
        # A4 landscape: 297x210mm, border 20mm left, 10mm others
        # Title block typically 170mm wide x 50mm high

        title_x = 297 - 170 - 10  # Right aligned with 10mm margin
        title_y = 10  # Bottom aligned with 10mm margin

        # Draw title block border
        msp.add_lwpolyline(
            [
                (title_x, title_y),
                (title_x + 170, title_y),
                (title_x + 170, title_y + 50),
                (title_x, title_y + 50),
                (title_x, title_y),
            ],
            dxfattribs={"layer": "OUTLINE"},
        )

        # Add title text
        msp.add_text(
            f"MOUNTING BRACKET - {params.bracket_type.upper()}",
            dxfattribs={
                "layer": "TEXT",
                "height": 5,  # Title text larger
                "insert": (title_x + 5, title_y + 35),
            },
        )

        # Add material specification
        msp.add_text(
            f"MATERIAL: {params.material}",
            dxfattribs={
                "layer": "TEXT",
                "height": 3.5,
                "insert": (title_x + 5, title_y + 25),
            },
        )

        # Add dimensions summary
        msp.add_text(
            f"{params.width}x{params.height}x{params.thickness}mm",
            dxfattribs={
                "layer": "TEXT",
                "height": 3.5,
                "insert": (title_x + 5, title_y + 15),
            },
        )

        # Add hole specification
        msp.add_text(
            f"{params.hole_count}x Ø{params.hole_diameter}mm HOLES",
            dxfattribs={
                "layer": "TEXT",
                "height": 3.5,
                "insert": (title_x + 5, title_y + 5),
            },
        )
