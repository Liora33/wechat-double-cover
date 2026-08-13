---
name: wechat-double-cover
version: 2.0.0
description: Create WeChat Official Account dual-purpose cover images that simultaneously satisfy the message-list wide crop and the share/profile square crop, using exact verified crop geometry instead of approximate aspect ratios.
---

# WeChat Official Account Dual Cover Skill

## Purpose

Use this skill whenever the user asks for a **公众号双拼封面图 / 微信公众号双封面 / WeChat double cover**.

The goal is not to make a generic panoramic banner. The goal is to produce one exact master image that survives **two different WeChat crop contexts**:

- Message-list wide cover
- Share card / Official Account profile square cover

## Hard Geometry — MUST NOT CHANGE

### Final master canvas

- **1252 × 374 px** exactly
- Do not deliver 3:1, 16:9, 2172×724, or any approximate substitute.

### Left region — message-list crop

- **879 × 374 px**
- Aspect ratio ≈ **2.3503:1**
- Intended crop: `x=0..878`, `y=0..373`

### Right region — share/profile crop

- **374 × 374 px**
- Aspect ratio **1:1**
- Intended crop starts at approximately **x=878**
- Intended crop: `x=878..1251`, `y=0..373`

### Seam / overlap rule

Because `879 + 374 = 1253`, while the final master width is `1252`, the verified layout uses a **1 px overlap** at the seam:

- Left region ends at `x=878`
- Right region starts at `x=878`
- Shared seam column: `x=878`

This is intentional. Do not “fix” it by moving the right crop to `x=879` or by changing the total canvas width.

## Core Composition Principle

**Design the two crop regions independently for their actual final use, then merge them precisely.**

Never:

1. Generate a generic ultra-wide image.
2. Guess a visual split.
3. Let WeChat auto-crop it later.

That workflow repeatedly causes broken proportions, truncated subjects, missing right-side content, and visible seam problems.

## Production Workflow

### Step 1 — Parse the user's exact text

- Preserve all text exactly unless the user explicitly allows editing.
- Do not add, delete, paraphrase, or invent copy.
- Split copy by intended crop region:
  - Left = message-list cover copy
  - Right = square-card copy

### Step 2 — Build the left region independently

Canvas: **879 × 374 px**.

Requirements:

- Treat it as a finished wide cover, not as the left half of a panorama.
- Keep headline, subtitle, and important subject fully inside this crop.
- Avoid placing important content too close to the seam or outer edges.
- Preserve full human anatomy and key objects; no cropped heads, hands, fingers, vehicles, buildings, or focal subjects.
- Ensure the visual weight reads correctly when the right square is completely hidden.

### Step 3 — Build the right region independently

Canvas: **374 × 374 px**.

Requirements:

- Treat it as a finished square cover.
- The right-side text must be **large, immediately readable, and intentionally composed for 1:1**.
- Do not shrink right-side typography just because the overall master is wide.
- Keep key words and focal subject away from the seam and outer edges.
- It must still make sense when viewed alone.

### Step 4 — Logo rule

Default: **NO logo**.

This includes:

- Brand logos
- School emblems
- Organization marks

Only add a logo when the user explicitly requests one for that specific cover.

### Step 5 — Exact assembly

Create the final **1252 × 374 px** master:

1. Place the left 879×374 region at `(0, 0)`.
2. Place the right 374×374 region at `(878, 0)`.
3. Preserve the 1 px seam overlap at `x=878`.
4. Do not add a visible divider unless the user explicitly requests one.
5. Do not stretch, squeeze, or distort either region during assembly.

## Three-Stage Pre-Delivery Self-Check

A cover is not finished until all three checks pass.

### Check A — Master geometry

Reject immediately if:

- Canvas is not exactly **1252×374 px**.
- Left crop is not exactly **879×374 px**.
- Right crop is not exactly **374×374 px** starting at **x=878**.

### Check B — Simulated WeChat crops

Export or preview both real use-cases:

- `left-preview.png` = crop `(0, 0, 879, 374)`
- `right-preview.png` = crop `(878, 0, 1252, 374)`

Verify:

- No headline/subtitle is cut off.
- No key subject is truncated.
- The left crop looks complete without the right crop.
- The right crop looks complete without the left crop.
- Right-side typography remains large enough.

### Check C — Visual integrity

Reject if any of these occur:

- Human anatomy distortion, especially fingers/hands/limbs/faces.
- User-supplied source material is stretched or deformed.
- Key subject is cropped by the master edge.
- Right square lacks enough content or looks empty.
- Left crop contains unintended extra content from the right.
- Obvious hard divider or ugly seam appears unexpectedly.
- Text is garbled, misspelled, missing, duplicated, or invented.
- Overall composition becomes too dark, muddy, noisy, or illegible when the brief requires a bright clean style.

## Non-Negotiable Failure Conditions

The output is considered invalid if any of the following is true:

- Wrong master size.
- Approximate ratio substituted for the verified geometry.
- One generic wide image was generated first and only later hard-cropped.
- Left/right crops were not independently composed.
- Right-side text is too small.
- Default logo was added without permission.
- User copy was added, deleted, or altered without permission.
- Focal subjects are distorted or cut off.
- The two simulated WeChat crops were not checked before delivery.

## Recommended File Outputs

For each completed cover, keep:

- `wechat-double-cover.png` — final 1252×374 master
- `left-preview.png` — 879×374 message-list preview
- `right-preview.png` — 374×374 share/profile preview

Optional validation command:

```bash
python scripts/validate_cover.py wechat-double-cover.png --export-previews
```

## Invocation Examples

Trigger phrases include:

- “做公众号双拼封面图”
- “调用 skill 做公众号双拼封面”
- “做微信后台左右双封面”
- “做 1252×374 的公众号双封面”

When triggered, apply this skill before deciding visual style.

## Priority

This **v2.0.0** specification supersedes earlier approximate-ratio versions of the workflow.
