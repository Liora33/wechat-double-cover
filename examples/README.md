# Examples

For each completed project, keep three images for validation:

```text
wechat-double-cover.png   # 1252×374 final master image
left-preview.png          # 879×374 message-list preview
right-preview.png         # 374×374 share/profile preview
```

Generate the previews with:

```bash
python ../scripts/validate_cover.py wechat-double-cover.png --export-previews
```

During manual review, inspect both preview images independently. Do not approve a cover based only on how the full 1252×374 master image looks.
