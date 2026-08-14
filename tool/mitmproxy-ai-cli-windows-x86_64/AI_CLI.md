# mitmproxy AI CLI 使用说明

这个版本面向 AI 自动化使用，默认不打开交互 TUI，也不启动 Web GUI。

## 入口

- `mitmai capture`：启动无界面代理，实时输出 JSONL。
- `mitmai daemon`：启动无界面代理和本地控制 API，供后续 CLI 命令管理 flow。
- `mitmai inspect`：读取 `.mitm` 或 HAR 文件，导出 JSON/JSONL/summary。
- `mitmai flows`：列出、查看、修改、删除、恢复、杀死、复制、重放、导入、导出 flow。
- `mitmai commands`：列出或执行 mitmproxy 内部命令。
- `mitmai options`：读取、修改、保存运行时选项。
- `mitmai events` / `mitmai state`：读取事件日志和运行状态。
- `mitmai api`：调用任意本地控制 API 路径。
- `mitmdump`：保留 mitmproxy 原生无界面 CLI。
- `mitmproxy`：在本版本中等价于无界面 `capture` 入口。
- `mitmweb`：GUI 已禁用，只返回 JSON 提示。

## 实时抓包

```powershell
mitmai capture --listen-host 127.0.0.1 --listen-port 8080 --jsonl flows.jsonl --flow-file flows.mitm
```

常用参数：

- `--jsonl -`：输出到标准输出。
- `--jsonl flows.jsonl`：输出到 JSONL 文件。
- `--flow-file flows.mitm`：同时保存原生 mitmproxy flow 文件。
- `--body-limit 4096`：限制请求/响应 body 预览字节数。
- `--no-bodies`：只输出元数据和头部，不输出 body 预览。
- `--no-headers`：不输出 HTTP headers。
- `--duration 60`：60 秒后自动停止。
- `--set option=value`：透传 mitmproxy 选项。
- `-s addon.py`：加载额外 addon。

## 交互控制模式

启动 daemon：

```powershell
mitmai daemon --listen-port 8080 --control-port 8081 --token mitmai --flow-file flows.mitm --jsonl flows.jsonl
```

daemon 不会打开浏览器。后续命令通过本地控制 API 操作同一个运行实例：

```powershell
mitmai state --control http://127.0.0.1:8081 --token mitmai
```

```powershell
mitmai flows list --control http://127.0.0.1:8081 --token mitmai
```

```powershell
mitmai flows get <flow-id> --control http://127.0.0.1:8081 --token mitmai
```

```powershell
mitmai flows update <flow-id> --json '{"comment":"checked","marked":true}' --control http://127.0.0.1:8081 --token mitmai
```

```powershell
mitmai flows replay <flow-id> --control http://127.0.0.1:8081 --token mitmai
```

```powershell
mitmai flows dump -o selected.mitm --filter '~u api' --control http://127.0.0.1:8081 --token mitmai
```

```powershell
mitmai commands list --control http://127.0.0.1:8081 --token mitmai
```

```powershell
mitmai commands run replay.client.stop --control http://127.0.0.1:8081 --token mitmai
```

```powershell
mitmai options set ssl_insecure true --control http://127.0.0.1:8081 --token mitmai
```

`mitmai api` 可以访问所有后端 API：

```powershell
mitmai api GET /flows.json --control http://127.0.0.1:8081 --token mitmai
```

## 离线解析

```powershell
mitmai inspect -i flows.mitm --format jsonl -o flows.export.jsonl
```

```powershell
mitmai inspect -i flows.mitm --format summary
```

```powershell
mitmai inspect -i flows.mitm --format json --limit 20
```

## JSONL 输出结构

每行是一条 flow，字段稳定适合 AI 解析：

- `id`
- `type`
- `timestamp_start`
- `client`
- `server`
- `request`
- `response`
- `websocket`
- `tcp`
- `udp`
- `dns`
- `error`

body 字段只输出有限预览：

- `size`
- `sha256`
- `truncated`
- `encoding`
- `preview`

## 推荐 AI 工作流

1. 只需要采集时，用 `mitmai capture`。
2. 需要像人工 GUI 一样操作 flow 时，用 `mitmai daemon`。
3. 把客户端代理设置到 `127.0.0.1:8080`。
4. AI 优先读取 `flows.jsonl` 做快速分析。
5. 需要实时操作时，使用 `mitmai flows`、`mitmai commands`、`mitmai options`。
6. 需要重新导出时，用 `mitmai inspect -i flows.mitm`。

## 功能覆盖说明

`mitmai daemon` 使用 mitmproxy Web 后端的同一套 flow/view/command/option API，但不会打开 Web 页面。人工在 GUI 中常见的查看、筛选、编辑、删除、恢复、杀死、复制、重放、导入、导出、读取内容视图、执行命令、修改选项、读取事件日志和状态，都可以通过 CLI 完成。
