# 3D Material Cards Skill

[**简体中文**](README.md) | **English**

A reusable Codex skill for producing interactive 3D and 2.5D material-lit cards for characters, collectibles, products, games, exhibitions, and historical subjects.

## Quick links

- 🃏 **[Launch the interactive Five Tiger Generals demo](https://mr-funny.github.io/five-tiger-generals-cards/)**
- 🎬 **[Watch the complete `3d卡牌.mp4` with sound](https://mr-funny.github.io/3d-material-cards-skill/preview/)**
- 🧩 **[Open the installable Skill directory](3d-material-cards/)**

The live demo supports pointer-controlled tilt, moving light, metallic highlights, relief shadows, five character selections, and real-time rendering controls.

## Video preview

[![Interactive 3D card animated preview](preview/3d-card-preview.gif)](https://mr-funny.github.io/3d-material-cards-skill/preview/)

Click the animated preview to open the complete 28.44-second MP4 with sound.

## Five Tiger Generals gallery

| Guan Yu | Zhao Yun | Zhang Fei | Ma Chao | Huang Zhong |
| :---: | :---: | :---: | :---: | :---: |
| [<img src="preview/cards/guan-yu.png" width="170" alt="Guan Yu material card" />](https://mr-funny.github.io/five-tiger-generals-cards/) | [<img src="preview/cards/zhao-yun.png" width="170" alt="Zhao Yun material card" />](https://mr-funny.github.io/five-tiger-generals-cards/#collection) | [<img src="preview/cards/zhang-fei.png" width="170" alt="Zhang Fei material card" />](https://mr-funny.github.io/five-tiger-generals-cards/#collection) | [<img src="preview/cards/ma-chao.png" width="170" alt="Ma Chao material card" />](https://mr-funny.github.io/five-tiger-generals-cards/#collection) | [<img src="preview/cards/huang-zhong.png" width="170" alt="Huang Zhong material card" />](https://mr-funny.github.io/five-tiger-generals-cards/#collection) |

The Five Tiger Generals are a worked example. The Skill itself is not limited to Three Kingdoms or historical characters.

## End-to-end workflow

The Skill deliberately completes one card before starting the next. This avoids style drift and makes visual QA manageable.

1. **Inspect the target project**
   - Identify the card ratio, asset naming convention, shader implementation, existing art direction, and fallback behavior.
2. **Define the series style**
   - Fix the border language, materials, palette, lighting mood, composition rules, and forbidden elements before generating art.
   - Chinese historical engraved cards can use `references/historical-card-style.md`.
3. **Design the subject and action**
   - Preserve identity-defining features and choose a silhouette, pose, product angle, or action that differs from previous cards.
4. **Generate one complete front image**
   - Generate a single card face with the built-in ImageGen tool.
   - Avoid separate transparent foreground figures, outer mockups, accidental text, watermarks, cropped weapons, or duplicated subjects.
5. **Recover the selected ImageGen result**
   - Decode the approved Base64 PNG from the Codex session JSONL with `scripts/extract_image_result.py`.
6. **Inspect the recovered front**
   - Check anatomy, identity, framing, texture separation, important edges, aspect ratio, and consistency with the series.
7. **Generate material maps**
   - Run `scripts/material_maps.py` to derive height, normal, roughness, and blurred parallax maps.
8. **Validate the asset set**
   - Confirm that all maps share identical dimensions and that the front image uses the intended card ratio.
9. **Integrate the WebGL material**
   - Use one flat card face with diffuse color, normal detail, roughness, directional height shadows, and restrained blurred parallax.
10. **Tune and verify**
    - Test pointer lighting, edge shadows, texture stability, fallback images, mobile layout, reduced-motion behavior, and live controls.
11. **Add the card to the collection**
    - Preserve existing entries. Only begin the next card after the current card passes visual QA.

## Process assets

The Guan Yu example below shows the material pipeline used by the interactive renderer.

| Front / diffuse | Height | Normal | Roughness | Blurred parallax |
| :---: | :---: | :---: | :---: | :---: |
| <img src="preview/cards/guan-yu.png" width="170" alt="Guan Yu front diffuse map" /> | <img src="preview/process/guan-yu-height.png" width="170" alt="Guan Yu height map" /> | <img src="preview/process/guan-yu-normal.png" width="170" alt="Guan Yu normal map" /> | <img src="preview/process/guan-yu-roughness.png" width="170" alt="Guan Yu roughness map" /> | <img src="preview/process/guan-yu-parallax.png" width="170" alt="Guan Yu blurred parallax map" /> |

| Asset | Purpose |
| --- | --- |
| **Front / diffuse** | Supplies the visible color, illustration, border, and surface detail. |
| **Height** | Represents detailed relief and is sampled for directional self-shadowing. |
| **Normal** | Encodes per-pixel surface direction so armor, paper, engraving, and borders react differently to light. |
| **Roughness** | Controls whether an area behaves as matte paper, cloth, lacquer, bronze, or polished gold. |
| **Blurred parallax** | Provides only broad, restrained UV movement. Blurring prevents detailed textures from visibly swimming. |

### Recommended asset contract

```text
subject-front.png
subject-height.png
subject-normal.png
subject-roughness.png
subject-parallax.png
```

Keep every file at the same width and height. Do not use the detailed height map for strong UV displacement.

## One-click installation

### Install by asking Codex

Paste this into Codex:

```text
Use $skill-installer to install https://github.com/Mr-funny/3d-material-cards-skill/tree/main/3d-material-cards
```

Codex will use its official Skill Installer, copy only the `3d-material-cards` directory into `$CODEX_HOME/skills`, and make it available on the next Codex turn.

### Install with the official Codex installer command

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/Mr-funny/3d-material-cards-skill/tree/main/3d-material-cards
```

### Ask another AI agent to install it

For an agent that supports Agent Skills, paste:

```text
Install the Agent Skill from https://github.com/Mr-funny/3d-material-cards-skill/tree/main/3d-material-cards. Copy the 3d-material-cards directory into your skills directory and load its SKILL.md instructions.
```

There is no universal installation directory shared by every AI agent. The agent should map the standard `SKILL.md`, `agents/`, `references/`, and `scripts/` structure to its own Skill directory.

### One-command manual installation for Codex

```bash
git clone --depth 1 https://github.com/Mr-funny/3d-material-cards-skill.git \
  && mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills" \
  && cp -R 3d-material-cards-skill/3d-material-cards "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## Manual installation

### Requirements

- Codex with the built-in image generation tool
- Git
- Python 3
- Pillow and NumPy when running `material_maps.py`

### 1. Clone the repository

```bash
git clone https://github.com/Mr-funny/3d-material-cards-skill.git
cd 3d-material-cards-skill
```

### 2. Copy the Skill into Codex

```bash
mkdir -p ~/.codex/skills
cp -R 3d-material-cards ~/.codex/skills/
```

The installed Skill must end up at:

```text
~/.codex/skills/3d-material-cards/SKILL.md
```

### 3. Prepare Python dependencies

If your workspace already provides Pillow and NumPy, no additional setup is needed. Otherwise create an isolated environment:

```bash
python3 -m venv ~/.codex/venvs/3d-material-cards
~/.codex/venvs/3d-material-cards/bin/pip install pillow numpy
```

Use that Python executable when running the material-map script manually.

### 4. Verify the installation

```bash
test -f ~/.codex/skills/3d-material-cards/SKILL.md \
  && echo "3d-material-cards installed"
```

Start a new Codex task so the Skill catalog refreshes, then invoke:

```text
Use $3d-material-cards to create an interactive material-lit card for my subject.
```

### Updating

```bash
cd 3d-material-cards-skill
git pull
cp -R 3d-material-cards ~/.codex/skills/
```

## Script usage

### Recover an ImageGen PNG from a Codex session

```bash
python 3d-material-cards/scripts/extract_image_result.py \
  --session /path/to/session.jsonl \
  --contains "target subject" \
  --output public/assets/subject-front.png
```

The script selects the latest matching built-in ImageGen PNG and decodes its Base64 payload.

### Generate material maps

```bash
python 3d-material-cards/scripts/material_maps.py \
  --front public/assets/subject-front.png \
  --prefix public/assets/subject
```

This creates:

```text
public/assets/subject-height.png
public/assets/subject-normal.png
public/assets/subject-roughness.png
public/assets/subject-parallax.png
```

## Example requests

```text
Use $3d-material-cards to create a 2:3 material-lit card for a cyberpunk detective.
```

```text
Use $3d-material-cards to convert this existing product card into a WebGL material card with subtle pointer tilt.
```

```text
Use $3d-material-cards to add one new historical figure to this collection while preserving its visual system.
```

```text
Use $3d-material-cards to derive height, normal, roughness, and parallax maps from this approved front image.
```

## Tested rendering preset

| Setting | Value |
| --- | ---: |
| Contrast | 1.08 |
| Ambient | 0.63 |
| Warm diffuse | 0.23 |
| Metallic specular | 0.71 |
| Normal strength | 0.26 |
| Relief shadow | 0.48 |
| Shadow reach | 0.00180 |
| Parallax | 0.00035 |
| Float amplitude | 0.5 px |
| Float speed | 0.00110 |
| Idle tilt | 1.85° |
| Pointer tilt | 12.0° |

Treat these as safe initial values, not hard limits. Expose them as live controls when the project benefits from visual tuning.

## Skill directory standard

The installable directory intentionally stays small:

```text
3d-material-cards/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── historical-card-style.md
└── scripts/
    ├── extract_image_result.py
    └── material_maps.py
```

Repository documentation, videos, galleries, and process images live outside the Skill directory so they do not consume the Skill context window.

## Validation status

- Official `quick_validate.py`: passed
- `SKILL.md`: 64 lines, below the recommended 500-line limit
- Frontmatter: only `name` and `description`
- Folder name and Skill name: identical
- `agents/openai.yaml`: validated
- Python scripts: compiled and executed successfully
- Material-map output: verified at 1024×1536 for height, normal, roughness, and parallax

## Troubleshooting

- **Skill does not appear:** start a new Codex task after copying the folder.
- **`ModuleNotFoundError: PIL` or `numpy`:** install Pillow and NumPy or use the workspace's bundled Python runtime.
- **Texture appears to swim:** reduce parallax and confirm that the blurred parallax map, not detailed height, controls UV movement.
- **Card looks flat:** verify normal-map orientation, canvas device-pixel ratio, ambient light, and specular strength.
- **Video does not play on the GitHub file page:** use the linked GitHub Pages HTML5 player.

## License

MIT
