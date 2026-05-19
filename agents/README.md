# SubAgents

把你的 SubAgent 定义放在本目录,每个 SubAgent 一个 `.md` 文件。

## 格式

```markdown
---
name: my-subagent
description: 一句话描述何时该派发本 SubAgent
tools:
  - Read
  - mcp__my-plugin__do_something
model: inherit  # 可选, 缺省继承主控
---

# 调度边界 (最高优先级)

何时**禁止**派发本 agent:
- ...

何时**应当**派发:
- ...

# 身份定位

你是 [角色名], 负责 ...

# 执行规范

1. ...
2. ...
```

## 加载方式

BIMCanvas `loader.py` 显式 `glob agents/*.md` 解析,**SDK plugin 机制不扫描本目录**
(主真理源 §3.6)。同名 agent 与 core-base 冲突时,**plugin 这份默认覆盖 base**
(v3.7 silent override + logger.info 记录),无需在 manifest 中显式声明
(v3.3.2 已删除 `overrides` 字段)。

## 何时该写 SubAgent

- 任务有强分支语义(主控判断 → 派发不同分身)
- 单分区多并行(layout-agent 是经典案例)
- 上下文隔离(避免污染主控)

如果你的 plugin 只是注册几个 MCP 工具,不一定需要 SubAgent。
