# .dev-home/plugins/my-plugin/

本目录是 plugin 作者的**开发态沙盒入口**,模拟用户最终安装后的状态。

## 推荐工作流(软链方式)

把本 plugin 项目根软链到本目录,后续改代码即时生效:

### Linux / macOS

```bash
# 在 plugin 项目根执行
rm -rf .dev-home/plugins/my-plugin
ln -s "$(pwd)" .dev-home/plugins/my-plugin
```

### Windows PowerShell(管理员)

```powershell
# 在 plugin 项目根执行
Remove-Item -Recurse -Force .\.dev-home\plugins\my-plugin
New-Item -ItemType SymbolicLink -Path ".\.dev-home\plugins\my-plugin" -Target $PWD
```

## 替代方案(复制,不推荐)

如果环境不支持软链,可以复制 plugin 内容:

```bash
cp -r ./bimcanvas-plugin.json ./.claude-plugin ./BIMCANVAS.md ./agents ./skills ./mcp_tools ./projectMount .dev-home/plugins/my-plugin/
# 注:mcp_tools/ 目录下文件名 stem 必须 = plugin name (这里是 my-plugin),否则 namespace 推断出错
```

但复制方式每次改代码都要重新拷贝,不建议日常开发使用。

## 启动 BIMCanvas

```bash
# Linux / macOS
export BIMCANVAS_HOME="$(pwd)/.dev-home"

# Windows PowerShell
$env:BIMCANVAS_HOME = "$PWD\.dev-home"

cd <path-to-BIMCanvas>
dotnet run --project BIMCanvas.Server
```

## 标记为本地 trusted(绕过 GitHub install 流程)

本地开发态,你已经看过自己写的代码,可以手动把 plugin 标记为 trusted(主真理源 §2.3 「3.2 本地开发与测试」):

1. BIMCanvas 启动后,会在 `.dev-home/plugins-state.json` 中自动写入 `my-plugin` 条目,初始 `trustState=untrusted`
2. 在 Web 设置页点 `[信任并激活]`(沙盒里这一步是允许的,因为是本地代码)
3. 或者手动编辑 `.dev-home/plugins-state.json`:

```json
{
  "my-plugin": {
    "trustState": "trusted",
    "installedAt": "2026-05-17T00:00:00+08:00",
    "trustedAt": "2026-05-17T00:00:00+08:00",
    "sourceKind": "local",
    "installedVersion": "0.1.0",
    "manifestChecksum": "sha256:..."
  }
}
```

`sourceKind: "local"` 会在 UI 上标记为「复现性较弱」 —— 因为没有 GitHub URL 与
resolvedCommit,接收方无法重建相同环境。**只在你自己机器上有效**,不要把该状态推到
公开 plugin repo。

## 测试 plugin 工作

启动后,在 Web 顶栏看到 active plugin 切换为 `my-plugin`,然后在 chat 中:

```
echo hello world
```

应该触发 `example-skill`,调用 `mcp__my-plugin__example`,回显:

```
[my-plugin] hello world
(plugin_id=my-plugin, scene_id=None, server_url=http://...)
```

如果失败,检查:

- `mcp_tools/<filename>.py` 文件名 stem 是否就是你的 plugin name(v3.3.2 D8:namespace 从文件名推断,模板默认 `mcp_tools/my-plugin.py` → namespace=`my-plugin`)
- `mcp_tools/my-plugin.py` 是否真的暴露了 `register(builder)` 函数
- `bimcanvas-plugin.json` 的 `tools.allow` 是否含 `mcp__my-plugin__example`(v3.3.2 fallback 模型:active 时完全接管,工具必须显式列在 allow 里)
- `.dev-home/plugins/my-plugin/` 软链是否真的指向 plugin 项目根

更多调试技巧见 `BIMCanvas/docs/BYO-Plugin.md` §8 常见错误对照表。
