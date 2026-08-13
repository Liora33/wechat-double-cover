# wechat-double-cover

A reusable skill for creating **WeChat Official Account dual-purpose cover images** that work correctly in both major crop contexts:

- Message list: wide cover
- Share card / Official Account profile: square cover

This project does not treat the cover as a generic panoramic banner. Instead, it uses verified crop geometry, requires both regions to be composed independently, and then merges them precisely into one master image.

## Core dimensions

| Use case | Size | Position |
|---|---:|---|
| Final master image | **1252×374 px** | — |
| Left message-list cover | **879×374 px** | starts at x=0 |
| Right square cover | **374×374 px** | starts at x≈878 |

> Note: the left and right regions intentionally share 1 px at `x=878` so the final canvas remains exactly 1252 px wide.

## Why not just use 3:1 or 16:9?

Because those ratios only look similar to a WeChat dual cover. They do not match the actual crop geometry.

Typical failures include:

- extra visual content leaking into the left crop
- insufficient content in the right square crop
- cropped people, hands, fingers, buildings, or key subjects
- an incorrect seam or divider position
- typography that becomes too small on the right
- a cover that changes dramatically after WeChat applies its own crop

## Correct workflow

1. Design the left region independently at **879×374 px**.
2. Design the right region independently at **374×374 px**.
3. Place the right region starting at **x=878**.
4. Merge both into a **1252×374 px** master image.
5. Simulate the two real WeChat crops.
6. Deliver only after both crop previews pass visual inspection.

## Default rules

- Do **not** add a logo unless the user explicitly requests one.
- Do not add, remove, rewrite, or paraphrase user-provided copy without permission.
- Right-side typography must be designed specifically for the 1:1 crop and remain large enough to read immediately.
- Do not stretch, distort, or aggressively crop user-provided source images.
- Do not sacrifice the usability of either real crop just to make the full-width master look more unified.

## Repository structure

```text
wechat-double-cover/
├─ SKILL.md
├─ README.md
├─ LICENSE
├─ scripts/
│  └─ validate_cover.py
└─ examples/
   └─ README.md
```

## Validation script

Install Pillow:

```bash
pip install pillow
```

Validate a finished cover:

```bash
python scripts/validate_cover.py path/to/cover.png
```

Validate and export both crop previews:

```bash
python scripts/validate_cover.py path/to/cover.png --export-previews
```

The script checks:

- whether the master image is exactly **1252×374 px**
- whether the left crop is exactly **879×374 px**
- whether the right crop is exactly **374×374 px**
- whether the right crop begins at **x=878**
- and can export both previews for manual review

## Skill usage

The full production rules live in [`SKILL.md`](./SKILL.md).

Typical trigger phrases include:

- `WeChat double cover`
- `WeChat Official Account dual cover`
- `公众号双拼封面图`
- `微信公众号双封面`

Chinese trigger phrases are intentionally kept for compatibility with real-world Chinese-language workflows; the public repository documentation itself is written in English.

## Version

Current specification: **v2.0.0**

This version supersedes older workflows that relied on approximate aspect ratios or generated a generic ultra-wide image before hard-cropping it.
