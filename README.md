# Three Kingdoms Material Cards Skill

A reusable Codex skill for creating premium interactive material-lit cards for Chinese historical figures. It covers single-character image generation, ImageGen result recovery, material-map derivation, calibrated WebGL lighting, and one-by-one collection expansion.

![Guan Yu interactive material card](preview/guan-yu-interactive-card.png)

## What it includes

- A strict one-character-at-a-time production workflow
- A consistent midnight-navy, jade and antique-gold visual system
- ImageGen result extraction from Codex session JSONL
- Height, normal, roughness and blurred parallax map generation
- A tested WebGL material and motion preset
- Character-specific pose guidance for the Five Tiger Generals

## Install

Copy the skill directory into your Codex skills folder:

```bash
cp -R three-kingdoms-material-cards ~/.codex/skills/
```

Then invoke it with `$three-kingdoms-material-cards`.

## Requirements

- Codex with the built-in image generation tool
- Python 3
- Pillow and NumPy for `scripts/material_maps.py`

## Repository layout

```text
three-kingdoms-material-cards/
├── SKILL.md
├── agents/openai.yaml
├── references/style-preset.md
└── scripts/
```

## License

MIT
