# projectMount

本目录声明你的 plugin 想"物化"到每个 `.bcp` 项目下的脚手架文件 / 目录。

## 什么时候用 projectMount

需要为 plugin 提供"每项目一份"的初始化资源时,例如:

- 一份 `references/<plugin-id>/design_principles.md` 设计规范模板
- 一份 `schemes/<sceneId>/.gitkeep` 占位目录
- 一份 `<plugin-id>-config.json` 项目级配置初值

## 物化时机:bind-time(只在用户绑定新 scene 时)

主真理源 v1.1 §3.9 + §6.1 R10 防御:

- **唯一物化入口**:`POST /api/project/{id}/scenes` 端点
- **绝不**在 open project 时自动物化(防 R10 静默覆盖 legacy 项目)
- 物化路径自动加 sceneId 命名空间前缀,绝不污染其他 sceneId 的命名空间

## manifest.json 格式(草案;详细规范待 Phase 2 收紧)

```json
{
  "files": [
    {
      "from": "references/design_principles.md",
      "to": "references/{sceneId}/design_principles.md",
      "ifExists": "skip"
    }
  ],
  "directories": [
    {
      "to": "schemes/{sceneId}/",
      "ensure": true
    }
  ]
}
```

- `from`: 相对 `projectMount/` 的源路径
- `to`: 相对项目根的目标路径,**必须**包含 `{sceneId}` 占位符或在已显式按 sceneId 命名的子目录
- `ifExists`: `skip` / `overwrite` / `error`(Phase 1 默认 `skip`,避免 R10)

## 不需要 projectMount

如果你的 plugin 不依赖项目级初始资源,可以删除整个 `projectMount/` 目录并从
`bimcanvas-plugin.json` 移除 `projectMount.manifest` 字段。
