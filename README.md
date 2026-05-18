# bimcanvas-plugin-template

> **GitHub Template** for building [BIMCanvas](https://github.com/vibedrafting/bimcanvas) domain plugins —
> 拿来即用的脚手架,覆盖 systemPrompt / SubAgents / Skills / MCP 工具 / projectMount 五层投影。

在右上角点 **[Use this template]** 即可派生一份新仓库,按下文三步走即可发布到 GitHub,
让任何 BIMCanvas 用户在 Web 设置页粘贴 URL 安装你的 plugin。

---

## 这是什么

[BIMCanvas](https://github.com/vibedrafting/bimcanvas) 是「通用 BIM 编辑器 + AI Agent 运行底座 + 文件驱动持久化」的开源平台。
真正的"专业能力"——室内布置、精装点位、商业空间规划、MEP 管线、装修材料推荐……——以独立 GitHub 仓库形态发布,每个仓库就是一个 **domain plugin**。

本仓库是创建这种 plugin 的官方起点。**这是一个 GitHub Template,本身不能装载运行**;
派生出的新仓库填好内容、本地沙盒验证通过后发布,才能被 BIMCanvas 安装。

## 一个 BIMCanvas plugin 包含什么

每个 plugin = 一份平台契约 `bimcanvas-plugin.json` + 最多五层资源:

| 层 | 文件 / 目录 | 用途 |
|---|---|---|
| 系统提示词 | `BIMCANVAS.md` | 你的 domain 上下文,运行时拼到平台 `core-base` 提示词之后,边界标识由平台插入 |
| SubAgents | `agents/*.md` | 主控按需派发的分身(如分区并行布置);BIMCanvas 显式 glob 加载,**不依赖 SDK 扫描** |
| Skills | `skills/<skill-name>/SKILL.md` | Claude SDK 触发的工作流,按 frontmatter `description` 命中 |
| MCP 工具 | `mcp_tools/<entry>.py` | 暴露 `register(builder)`,工具暴露为 `mcp__<mcpNamespace>__<tool>` |
| 项目脚手架 | `projectMount/*` | 用户绑定 scene 时 **bind-time** 一次性物化到 `.bcp` 内的初始资源 |

平台启动 Agent 子进程时把五层装配成 `ResolvedPluginBundle`,同时注入 core-base 的不变量与边界标识(防止 domain plugin 在 prompt 层覆盖平台约束)。

## 模板目录结构

```
.
├── bimcanvas-plugin.json          # 平台契约 manifest (plugin 作者手写)
├── .claude-plugin/plugin.json     # Claude SDK 触发器 (三字段与上文保持一致,
│                                  #   未来由 bimcanvas-plugin-validate CLI 派生)
├── BIMCANVAS.md                   # domain 系统提示词, 含「Plugin 边界(必读)」段
├── agents/                        # SubAgent .md 文件 (空骨架, README 含范式说明)
├── skills/example-skill/SKILL.md  # 示范 Skill — echo 触发 → 调用 example MCP 工具
├── mcp_tools/example.py           # 示范 MCP 工具 + register(builder) 两条硬约束注释
├── projectMount/                  # 项目级脚手架 (bind-time 物化, 空 manifest)
├── .dev-home/plugins/my-plugin/   # 本地开发态沙盒入口 (含详细 README)
└── .gitignore                     # 预禁 CLAUDE.md / settings.local.json / .claude/ 等污染文件
```

---

## 三步走

### Step 1 — Use this template → clone → 替换占位

GitHub 派生新仓库 → `git clone` 到本地 → 把下表占位换成你的真实信息:

| 文件 | 必改字段 |
|---|---|
| `bimcanvas-plugin.json` | `name` / `version` / `displayName` / `description` / `mcpNamespace` 全改;`compatibility.bimcanvas` 按目标主版本调 semver range(默认 `^1.0.0`) |
| `.claude-plugin/plugin.json` | `name` / `description` / `version` 与上文保持一致(Phase 1 手动同步) |
| `BIMCANVAS.md` | 删掉 `## TODO` 标记,写你的 domain 提示词;**保留顶部「Plugin 边界(必读)」段** |
| `mcp_tools/example.py` | 改写 `register(builder)` 注册你的工具;**严格遵守注释里的两条硬约束**(见下方"安全模型") |
| `skills/example-skill/SKILL.md` | 重命名目录,改写 frontmatter 的 `description`(触发命中靠它) 与 `allowed-tools` |
| `agents/*.md` | 按需新增 SubAgent(可选,详见 `agents/README.md`) |
| `projectMount/manifest.json` | 按需声明项目级脚手架(可选,详见 `projectMount/README.md`) |
| `README.md` | **重写为你的 plugin 介绍**,删除本模板说明 |

### Step 2 — 本地沙盒测试(`.dev-home/`)

模板自带 `.dev-home/` 沙盒骨架,**不需要污染全局 `BIMCANVAS_HOME`**。把仓库软链到 `.dev-home/plugins/<your-plugin-id>/`,导出环境变量后启动 BIMCanvas:

```bash
# Linux / macOS
export BIMCANVAS_HOME="$(pwd)/.dev-home"

# Windows PowerShell
$env:BIMCANVAS_HOME = "$PWD\.dev-home"

# 启动 BIMCanvas (在 BIMCanvas 主仓库根)
cd <path-to-your-clone-of-BIMCanvas>
dotnet run --project BIMCanvas.Server
```

- BIMCanvas 以本仓库的 `.dev-home/` 作为运行时根
- 改任何 plugin 代码 → 重启 BIMCanvas → 立即生效
- Web 设置页 → 插件管理,应该看到你的 plugin 已安装,初始 `trustState=untrusted`
- 本地开发态可手动改 `.dev-home/plugins-state.json` 把 `trustState` 改 `trusted`,或在 UI 点 [信任并激活]

软链命令、`plugins-state.json` 模板、调试技巧详见 [`.dev-home/plugins/my-plugin/README.md`](./.dev-home/plugins/my-plugin/README.md)。

### Step 3 — 发布到 GitHub

本地测试通过后,推送公开仓库(Phase 1 全手动,三行命令):

```bash
git remote add origin https://github.com/<your-org>/<your-plugin-repo>.git
git add .
git commit -m "initial"
git push -u origin main
```

在你的 README 写一句:**"在 BIMCanvas Web 设置页 → [+ 安装新插件] → 粘贴 `<repo-url>` 即可安装"**。

Phase 2 视真实作者反馈再加 Web 端 [新建本地] / [一键校验] / [导出 zip] / GitHub OAuth 一键发布等高级功能。

---

## 安全模型(必读)

BIMCanvas 平台对 plugin 安装做了**严格的两阶段隔离**——这是为了避免"用户粘贴恶意 GitHub URL 就能在本机执行任意代码"的供应链 RCE 漏洞:

| 阶段 | 平台动作 | 是否执行 plugin Python 代码 |
|---|---|---|
| **安装(install)** | `StaticPluginValidator` 做纯文本静态校验(JSONSchema / 路径逃逸 / namespace 唯一性 / 目录纯净性) | ❌ 绝对不执行 |
| **信任(trust)** | 用户在 UI 点 [**信任并激活**] + 二次确认 → `ExecutablePluginProbe` 做一次 dry-run | ✅ 调一次 `register(builder)` |
| **运行(run)** | Server gate 拦截越权写:active plugin 只能写 `schemes/{activeSceneId}` / `references/{activeSceneId}` / `modules/{activeSceneId}`,越权一律 403 | ✅ 持续执行 |

**作为 plugin 作者,你只需要记住两件事**:

1. **`register(builder)` 必须是纯声明性的**——不读 `builder.context` 字段,不做 `isinstance` 断言,不在 register 体内做任何 I/O / 全局副作用。所有副作用必须挪到 tool handler 内。完整两条硬约束见 [`mcp_tools/example.py`](./mcp_tools/example.py) 顶部注释——违反会导致 `ExecutablePluginProbe` 失败,plugin 永远无法被信任。
2. **不要在 plugin 内试图伪造 trust 状态**(不写 `.bimcanvas/install.json` 之类)。trust 元数据存在平台外的 `<BIMCANVAS_HOME>/plugins-state.json`,plugin 目录不可触达;平台会忽略 plugin 内任何同名文件。

## 目录纯净纪律 ⚠️

**绝不**在仓库根添加以下文件——`StaticPluginValidator` 会在安装阶段直接拒绝整个 plugin:

- `CLAUDE.md`
- `settings.local.json`
- `.claude/` 目录
- `.bimcanvas/` 目录(试图伪造 trust 状态)

理由详见主仓库 [`docs/BYO-Plugin.md`](https://github.com/vibedrafting/bimcanvas/blob/main/docs/BYO-Plugin.md)。本仓库 `.gitignore` 已预禁这些路径,只要不主动绕过不会触发。

---

## 文档导航(BIMCanvas 主仓库)

| 文档 | 想知道什么 |
|---|---|
| [`docs/BYO-Plugin.md`](https://github.com/vibedrafting/bimcanvas/blob/main/docs/BYO-Plugin.md) | **完整开发者指南** —— register 硬约束、常见错误对照、调试技巧 |
| [`docs/plugin-architecture.md`](https://github.com/vibedrafting/bimcanvas/blob/main/docs/plugin-architecture.md) | 平台 + plugin 架构总图 |
| [`docs/plugin-manifest-schema.md`](https://github.com/vibedrafting/bimcanvas/blob/main/docs/plugin-manifest-schema.md) | `bimcanvas-plugin.json` 每个字段定义 |
| [`docs/plugin-lifecycle-states.md`](https://github.com/vibedrafting/bimcanvas/blob/main/docs/plugin-lifecycle-states.md) | 四态生命周期(installed / active / bound / launched) + trustState 转换 |
| [`docs/plugin-security-model.md`](https://github.com/vibedrafting/bimcanvas/blob/main/docs/plugin-security-model.md) | 安装为什么不执行代码 / 信任如何工作 |

## 参考实现

| Plugin | 仓库 | 状态 |
|---|---|---|
| `interior-layout` | [`vibedrafting/bimcanvas-plugin-interior-layout`](https://github.com/vibedrafting/bimcanvas-plugin-interior-layout) | 官方首个 reference plugin —— 住宅家具布置 |

## License

Apache-2.0,与 BIMCanvas 主仓库保持一致。你可以选用任何兼容 license,但建议同 license 以简化生态协作。
