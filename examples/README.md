# Examples

建议每个实际项目保留三张图用于验收：

```text
wechat-double-cover.png   # 1252×374 最终成品
left-preview.png          # 879×374 消息列表预览
right-preview.png         # 374×374 转发卡片 / 公众号主页预览
```

生成预览：

```bash
python ../scripts/validate_cover.py wechat-double-cover.png --export-previews
```

人工验收时，请分别看两个 preview，不要只看总图。
