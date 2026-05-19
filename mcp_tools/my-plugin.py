"""My Plugin MCP 工具入口 — 示范 register(builder) 范式。

平台在启动 Agent 子进程时, 通过 importlib 加载本文件并调 register(builder);
builder 是 bimcanvas_plugin_sdk.McpServerBuilder 实例 (或 ExecutablePluginProbe
阶段的 _FakeBuilder, 见下方 ⚠️ 硬约束)。

参考文档:
- docs/BYO-Plugin.md §4 — Plugin 作者必读, register 函数体内两条硬约束
- docs/plugin-security-model.md §3 — ExecutablePluginProbe 内部机制
- bimcanvas_plugin_sdk/{builder,context}.py — SDK 公开 API
"""

from bimcanvas_plugin_sdk import McpServerBuilder


def register(builder: McpServerBuilder) -> None:
    """入口契约: 每个 plugin 的 mcp_tools/<entry>.py 必须暴露 def register(builder) -> None。

    ⚠️ 硬约束 1:register 函数体内严禁访问 builder.context 任何字段做条件注册。
       理由:ExecutablePluginProbe 在 trust 阶段做 dry-run 时, 传入最小占位
       PluginContext (空字符串 / None / 占位 logger / session=None);若 register
       体内读 context 字段会拿到占位值, 条件分支走错。
       正确做法:register 只声明工具元数据;context 字段读取必须在工具 handler
       内进行 (运行时 SDK 注入真实 context)。

    ⚠️ 硬约束 2:register 函数体内严禁 isinstance(builder, McpServerBuilder)。
       理由:ExecutablePluginProbe 当前用 _FakeBuilder 做 dry-run, fake builder
       不是 McpServerBuilder 子类。Plugin 作者必须接受 builder 是 duck-typed
       协议对象。

    详细解释见 docs/BYO-Plugin.md §4。
    """

    # ✅ 正确:闭包捕获 context, 但只在 handler 内读字段
    ctx = builder.context

    @builder.tool(
        "example",
        "示范工具: 回显 text 参数, 附带当前 active_plugin_id 与 scene_id 验证 PluginContext 注入。",
        {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "要原样回显的内容"},
            },
            "required": ["text"],
            "additionalProperties": False,
        },
    )
    async def example(args: dict) -> dict:
        text = args.get("text", "")

        # ✅ 正确:在 handler 内读 ctx 字段 (运行时是真实 PluginContext)
        return {
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"[my-plugin] {text}\n"
                        f"(plugin_id={ctx.active_plugin_id}, "
                        f"scene_id={ctx.active_scene_id}, "
                        f"server_url={ctx.server_url})"
                    ),
                }
            ]
        }

    # ────────────────────────────────────────────────────────────────────
    # 反例 (绝对不要这么写) — 仅用于教学, 把以下代码删除
    # ────────────────────────────────────────────────────────────────────
    #
    # ❌ 反例 1: 在 register 体内读 ctx 字段做条件注册
    # if ctx.active_scene_id == "interior-layout-1":      # probe 阶段 = None
    #     @builder.tool("scene_specific_tool", ...)        # 永远不会注册
    #     async def f(args): ...
    #
    # ❌ 反例 2: 在 register 体内做 isinstance 断言
    # assert isinstance(builder, McpServerBuilder)         # probe 阶段 = AssertionError
    #
    # ❌ 反例 3: 在 register 体内做副作用 (网络请求 / 文件 I/O / 全局状态修改)
    # urllib.request.urlopen("https://...")                # probe 阶段在 Server 进程内执行
    # global_state["loaded"] = True                        # 全局状态污染
    #
    # 所有副作用必须挪到 handler 函数体内, 运行时才执行。
    # ────────────────────────────────────────────────────────────────────
