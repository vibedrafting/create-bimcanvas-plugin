---
name: example-skill
description: |
  示范 Skill: 当用户说 "echo X" 时, 调用 mcp__my-plugin__example 回显 X。
  替换为你自己的触发场景描述; description 越具体, Skill 被正确触发的概率越高。
allowed-tools:
  - mcp__my-plugin__example
---

# example-skill

> 这是一份示范 Skill, 演示 Skill 文件的 frontmatter 与 body 格式。把它改成你自己的工作流。

## 触发条件

当用户的请求满足以下任一条件时, 你应该使用本 Skill:

- 用户说 "echo <something>"
- 用户要求 "测试一下 plugin 是否正常工作"

## 执行步骤

1. 调用 `mcp__my-plugin__example`, 把用户的输入作为 `text` 参数传入
2. 把工具返回的文本展示给用户
3. 如果工具失败 (含 `is_error: true` 或文本含 "ERROR"), 提示用户检查
   `BIMCANVAS_HOME/plugins/my-plugin/` 目录是否完整

## 禁止行为

- 不要在本 Skill 中执行任何写操作 (本 Skill 仅做只读演示)
- 不要绕过工具直接编造 echo 内容

## 示例

```
用户: echo hello world
你: [调用 mcp__my-plugin__example text="hello world"]
工具返回: "[my-plugin] hello world (plugin_id=my-plugin, scene_id=None, server_url=http://...)"
你: 工具回显: hello world
```
