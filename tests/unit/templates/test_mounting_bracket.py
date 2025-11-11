"""Unit tests for mounting bracket template."""

import tempfile
from pathlib import Path

import pytest
from build123d import Part
from cad_automation.templates.mounting_bracket import (
    MountingBracketParams,
    MountingBracketTemplate,
)


class TestMountingBracketParams:
    """Test parameter validation for mounting bracket."""

    def test_valid_params(self):
        """Test valid parameter creation."""
        params = MountingBracketParams(
            width=100.0,
            height=80.0,
            thickness=5.0,
            hole_diameter=8.0,
            hole_count=4,
            material="Steel",
            bracket_type="L",
        )
        assert params.width == 100.0
        assert params.height == 80.0
        assert params.thickness == 5.0
        assert params.hole_diameter == 8.0
        assert params.hole_count == 4
        assert params.material == "Steel"
        assert params.bracket_type == "L"

    def test_invalid_width(self):
        """Test negative width raises validation error."""
        with pytest.raises(ValueError):
            MountingBracketParams(
                width=-10.0,
                height=80.0,
                thickness=5.0,
                hole_diameter=8.0,
                hole_count=4,
            )

    def test_invalid_hole_count(self):
        """Test hole count outside range raises validation error."""
        with pytest.raises(ValueError):
            MountingBracketParams(
                width=100.0,
                height=80.0,
                thickness=5.0,
                hole_diameter=8.0,
                hole_count=20,  # Max is 10
            )


class TestMountingBracketTemplate:
    """Test mounting bracket 3D/2D generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.template = MountingBracketTemplate()
        self.params = MountingBracketParams(
            width=100.0,
            height=80.0,
            thickness=5.0,
            hole_diameter=8.0,
            hole_count=4,
            material="Steel",
            bracket_type="L",
        )

    def test_generate_3d_l_bracket(self):
        """Test 3D L-bracket generation."""
        part = self.template.generate_3d(self.params)
        assert isinstance(part, Part)
        # Verify part has volume (not empty)
        assert part.volume > 0

    def test_generate_3d_flat_bracket(self):
        """Test 3D flat bracket generation."""
        params = MountingBracketParams(
            width=100.0,
            height=80.0,
            thickness=5.0,
            hole_diameter=8.0,
            hole_count=4,
            material="Steel",
            bracket_type="flat",
        )
        part = self.template.generate_3d(params)
        assert isinstance(part, Part)
        assert part.volume > 0

    def test_generate_2d(self):
        """Test 2D drawing generation."""
        drawing = self.template.generate_2d(self.params)
        # Verify drawing has modelspace
        assert drawing.modelspace() is not None
        # Verify layers exist
        assert "OUTLINE" in drawing.layers
        assert "DIMENSIONS" in drawing.layers
        assert "TEXT" in drawing.layers

    def test_export_step(self):
        """Test STEP export."""
        part = self.template.generate_3d(self.params)
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_bracket.step"
            self.template.export_step(part, output_path)
            assert output_path.exists()
            assert output_path.stat().st_size > 0

    def test_export_dxf(self):
        """Test DXF export."""
        drawing = self.template.generate_2d(self.params)
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_bracket.dxf"
            self.template.export_dxf(drawing, output_path)
            assert output_path.exists()
            assert output_path.stat().st_size > 0

    def test_parametric_variation_width(self):
        """Test that changing width parameter affects output."""
        part1 = self.template.generate_3d(self.params)
        volume1 = part1.volume

        params2 = MountingBracketParams(
            width=200.0,  # Double width
            height=80.0,
            thickness=5.0,
            hole_diameter=8.0,
            hole_count=4,
            material="Steel",
            bracket_type="L",
        )
        part2 = self.template.generate_3d(params2)
        volume2 = part2.volume

        # Volume should increase with width
        assert volume2 > volume1

    def test_parametric_variation_thickness(self):
        """Test that changing thickness parameter affects output."""
        part1 = self.template.generate_3d(self.params)
        volume1 = part1.volume

        params2 = MountingBracketParams(
            width=100.0,
            height=80.0,
            thickness=10.0,  # Double thickness
            hole_diameter=8.0,
            hole_count=4,
            material="Steel",
            bracket_type="L",
        )
        part2 = self.template.generate_3d(params2)
        volume2 = part2.volume

        # Volume should increase with thickness
        assert volume2 > volume1
