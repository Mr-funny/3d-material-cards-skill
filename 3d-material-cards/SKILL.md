---
name: 3d-material-cards
description: Create premium interactive 3D and 2.5D material-lit cards for characters, collectibles, products, games, exhibitions, and historical subjects. Use when generating a card-front image, recovering a built-in ImageGen result, deriving normal/height/roughness/parallax maps, applying calibrated WebGL lighting and pointer tilt, or extending an interactive card collection one card at a time.
---

# 3D Material Cards

Create one complete card before starting another. Preserve established art direction and validate every asset before collection integration.

## Required workflow

1. Inspect the target app, existing card assets, aspect ratio, naming scheme, and interaction model. Preserve existing cards and use a lowercase hyphenated slug.
2. Establish a clear series art direction before image generation. Match the existing collection when one exists. For Chinese historical engraved cards, read [historical-card-style.md](references/historical-card-style.md).
3. Generate one **single, complete front-card image** with the built-in `image_gen` tool. Use the target card ratio, fill the card face without an outer mockup, preserve readable material separation, and avoid text, logos, or watermarks unless explicitly requested. Do not create a second transparent foreground subject layer.
   - Give each subject a distinct silhouette, composition, or action appropriate to its identity. Avoid repeating the same static pose across a collection.
4. Recover the selected image result from the session log with `scripts/extract_image_result.py`. Inspect the recovered PNG before accepting it. Regenerate only the current card if anatomy, geometry, framing, identity, or series style fails.
5. Create material maps with `scripts/material_maps.py`. Use the normal map for fine surface detail, detailed height for directional self-shadow, roughness for specular response, and blurred parallax as the only map allowed to move UVs.
6. Validate that the front, normal, height, roughness, and parallax assets have identical dimensions and the expected aspect ratio.
7. Integrate the art as one flat WebGL face: diffuse + normal + roughness + detailed height + blurred parallax. Do not add duplicate subject layers. Keep UV displacement at or below `0.00035` initially.
8. Add the card without deleting or reordering existing cards. Keep a visible fallback image when WebGL is unavailable.
9. Complete visual QA for the current card before generating the next one. Check crispness, texture stability, pointer lighting, edge shadows, fallback behavior, and mobile layout.

## Baseline rendering preset

Start with this tested material and motion preset, then expose the values as adjustable live controls.

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

Use pointer tilt and dynamic light to reveal depth. Avoid heavy grain overlays, moving particles, foreground parallax, excessive displacement, and visible texture swimming.

## Asset commands

```bash
python scripts/extract_image_result.py \
  --session <session.jsonl> --contains "target subject" \
  --output public/assets/subject-front.png

python scripts/material_maps.py \
  --front public/assets/subject-front.png \
  --prefix public/assets/subject
```

Use the workspace's bundled Python runtime when Pillow or NumPy are unavailable in the system interpreter.

## Subject handling

- Preserve the canonical identity, proportions, materials, colors, and signature features of the subject.
- Express identity through pose, viewing angle, lighting, supporting motifs, or product orientation.
- Keep essential anatomy, silhouettes, weapons, product edges, or collectible details inside the frame.
- Use one original illustration per card. Never copy another card's composition or a reference site's protected image assets.
- Process collections one card at a time when visual consistency and material quality are important.
