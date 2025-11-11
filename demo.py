"""Demo script to generate mounting bracket STEP and DXF files."""

from pathlib import Path

from src.cad_automation.templates.mounting_bracket import (
    MountingBracketParams,
    MountingBracketTemplate,
)


def main():
    """Generate example mounting brackets."""
    # Create output directory
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # Initialize template
    template = MountingBracketTemplate()

    # Example 1: L-bracket
    print("Generating L-bracket...")
    l_bracket_params = MountingBracketParams(
        width=100.0,
        height=80.0,
        thickness=5.0,
        hole_diameter=8.0,
        hole_count=4,
        material="Steel",
        bracket_type="L",
    )

    # Generate 3D model
    l_bracket_3d = template.generate_3d(l_bracket_params)
    template.export_step(l_bracket_3d, output_dir / "l_bracket.step")
    print(f"  ✓ Exported: {output_dir / 'l_bracket.step'}")

    # Generate 2D drawing
    l_bracket_2d = template.generate_2d(l_bracket_params)
    template.export_dxf(l_bracket_2d, output_dir / "l_bracket.dxf")
    print(f"  ✓ Exported: {output_dir / 'l_bracket.dxf'}")

    # Example 2: Flat bracket
    print("\nGenerating flat bracket...")
    flat_bracket_params = MountingBracketParams(
        width=120.0,
        height=60.0,
        thickness=3.0,
        hole_diameter=6.0,
        hole_count=6,
        material="Aluminum",
        bracket_type="flat",
    )

    # Generate 3D model
    flat_bracket_3d = template.generate_3d(flat_bracket_params)
    template.export_step(flat_bracket_3d, output_dir / "flat_bracket.step")
    print(f"  ✓ Exported: {output_dir / 'flat_bracket.step'}")

    # Generate 2D drawing
    flat_bracket_2d = template.generate_2d(flat_bracket_params)
    template.export_dxf(flat_bracket_2d, output_dir / "flat_bracket.dxf")
    print(f"  ✓ Exported: {output_dir / 'flat_bracket.dxf'}")

    print("\n✓ All files generated successfully!")
    print(f"\nOutput directory: {output_dir.absolute()}")
    print("\nGenerated files:")
    for file in output_dir.glob("*"):
        size_kb = file.stat().st_size / 1024
        print(f"  - {file.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
