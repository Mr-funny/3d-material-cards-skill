---
name: three-kingdoms-material-cards
description: Create premium, interactive material-lit card art for Chinese historical figures, especially Three Kingdoms characters. Use when generating a single new character card with crisp embossed/engraved art, recovering the built-in ImageGen result, deriving normal/height/roughness maps, applying calibrated WebGL lighting, or extending an existing historical-card collection one character at a time.
---

# Three Kingdoms Material Cards

Create one complete card before starting another. Never batch-generate characters or skip asset validation.

## Required workflow

1. Inspect the target app and its existing card assets. Preserve existing cards and use a lowercase hyphenated slug.
2. Read [style-preset.md](references/style-preset.md). Keep every character in the same midnight-navy, jade, old-gold engraved card series.
3. Generate one **single, complete front card image** with the built-in `image_gen` tool. It must be a 2:3 card face with no outer mockup, readable material separation, no text or numerals, and blank decorative cartouches. Do not create a separate foreground character layer.
   - Give every character a historically appropriate signature action and a distinct silhouette. Do not repeat the same frontal standing pose across the collection.
4. Recover the selected image result from the session log with `scripts/extract_image_result.py`. Inspect the recovered PNG before accepting it. Regenerate only the current character if pose, weapon, anatomy, framing, or series style fails.
5. Create material maps with `scripts/material_maps.py`. The normal map supplies fine engraved detail; the blurred parallax map is the only map allowed to move UVs.
6. Validate that the front, normal, height, roughness, and parallax assets all have identical dimensions and that the front is 2:3.
7. Integrate the card as a flat WebGL face: diffuse + normal + roughness + detailed height for directional relief shadows + blurred parallax for UV movement. Do not show a duplicate transparent subject layer. Keep UV displacement at or below `0.00035` by default.
8. Add the new card to the collection without replacing, deleting, or reordering an existing card. Verify the fallback image is visible if WebGL fails.
9. Complete visual QA for this character before starting the next one.

## Baseline rendering preset

Use these as the initial UI/shader values. They are the approved Guan Yu tuning and must be exposed to users as adjustable live controls.

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

The card may use pointer tilt and dynamic light. Do not use foreground parallax, heavy grain overlays, moving particles, or visible texture swimming.

## Asset commands

```bash
python scripts/extract_image_result.py \
  --session <session.jsonl> --contains "Zhao Yun" \
  --output public/assets/zhao-yun-front.png

python scripts/material_maps.py \
  --front public/assets/zhao-yun-front.png \
  --prefix public/assets/zhao-yun
```

Use the workspace's bundled Python runtime when Pillow/NumPy are unavailable in the system interpreter.

## Character handling

- Preserve the canonical weapon, clothing, age, and military identity for the historical figure.
- Express personality through action: choose a guarded turn, braced stance, advancing spear sweep, full bow draw, mounted command, or another historically credible pose appropriate to the figure.
- Keep a clean, central, full-body or three-quarter composition with all essential weapon parts inside the frame.
- Use one original illustration per card. Never copy another card’s composition or a reference site’s image assets.
- For the Five Tiger Generals, process in this order after Guan Yu: Zhao Yun, Zhang Fei, Ma Chao, Huang Zhong.
