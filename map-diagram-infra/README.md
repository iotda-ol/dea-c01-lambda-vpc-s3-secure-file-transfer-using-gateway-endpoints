# Universal Multi-Cloud Infrastructure Diagrams

This directory contains universal infrastructure diagrams and component mappings that can be used across AWS, GCP, and Azure cloud platforms.

## Contents

1. **UNIVERSAL-ARCHITECTURE.md** - Cloud-agnostic architecture overview
2. **COMPONENT-MAPPING.md** - Detailed mapping of components across AWS/GCP/Azure
3. **architecture.mermaid** - Mermaid diagram format (universal)
4. **architecture.plantuml** - PlantUML diagram format (universal)
5. **architecture-ascii.txt** - ASCII art diagram (universal)
6. **infrastructure-composer.json** - Machine-readable infrastructure definition
7. **deployment-matrix.md** - Deployment guide for each cloud platform

## Purpose

These diagrams provide a cloud-agnostic view of the secure file transfer architecture, allowing teams to:

- Understand the solution architecture independent of cloud provider
- Migrate between cloud platforms (AWS ↔ GCP ↔ Azure)
- Compare implementation approaches across providers
- Use the same conceptual design across multiple clouds

## Usage

Choose the format that best suits your needs:

- **Mermaid**: For GitHub/GitLab markdown rendering
- **PlantUML**: For detailed UML diagrams
- **ASCII**: For documentation and text-based viewing
- **JSON**: For programmatic processing and automation
- **Markdown**: For detailed component descriptions

## Cloud Provider Equivalents

All diagrams use universal terminology with cloud-specific mappings documented in `COMPONENT-MAPPING.md`.
