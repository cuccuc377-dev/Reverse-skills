from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import IO
from typing import Optional

from mitmproxy import ctx
from mitmproxy import dns
from mitmproxy import flow
from mitmproxy import http
from mitmproxy import tcp
from mitmproxy import udp
from mitmproxy.tools.ai_common import dumps_json
from mitmproxy.tools.ai_common import flow_to_json


class AIJsonl:
    def __init__(self) -> None:
        self.out: IO[str] | None = None
        self.path: str | None = None

    def load(self, loader) -> None:
        loader.add_option(
            "ai_jsonl_outfile",
            Optional[str],
            "-",
            "Write AI-readable JSONL flows to this path. Use '-' for stdout.",
        )
        loader.add_option(
            "ai_body_limit",
            int,
            4096,
            "Maximum request/response body preview bytes per JSONL event.",
        )
        loader.add_option(
            "ai_include_headers",
            bool,
            True,
            "Include HTTP headers in AI JSONL events.",
        )
        loader.add_option(
            "ai_include_bodies",
            bool,
            True,
            "Include bounded body previews in AI JSONL events.",
        )
        loader.add_option(
            "ai_duration",
            Optional[int],
            None,
            "Automatically stop the proxy after this many seconds.",
        )

    def configure(self, updated) -> None:
        if "ai_jsonl_outfile" in updated:
            self._open_output()

    def running(self) -> None:
        self._open_output()
        if ctx.options.ai_duration:
            asyncio.create_task(self._stop_later(ctx.options.ai_duration))

    async def _stop_later(self, seconds: int) -> None:
        await asyncio.sleep(seconds)
        ctx.master.shutdown()

    def done(self) -> None:
        if self.out and self.out is not sys.stdout:
            self.out.close()
        self.out = None
        self.path = None

    def response(self, item: http.HTTPFlow) -> None:
        self.emit(item)

    def error(self, item: flow.Flow) -> None:
        self.emit(item)

    def websocket_end(self, item: http.HTTPFlow) -> None:
        self.emit(item)

    def tcp_end(self, item: tcp.TCPFlow) -> None:
        self.emit(item)

    def tcp_error(self, item: tcp.TCPFlow) -> None:
        self.emit(item)

    def udp_end(self, item: udp.UDPFlow) -> None:
        self.emit(item)

    def udp_error(self, item: udp.UDPFlow) -> None:
        self.emit(item)

    def dns_response(self, item: dns.DNSFlow) -> None:
        self.emit(item)

    def dns_error(self, item: dns.DNSFlow) -> None:
        self.emit(item)

    def emit(self, item: flow.Flow) -> None:
        if self.out is None:
            self._open_output()
        assert self.out is not None
        payload = flow_to_json(
            item,
            include_headers=ctx.options.ai_include_headers,
            include_bodies=ctx.options.ai_include_bodies,
            body_limit=ctx.options.ai_body_limit,
        )
        self.out.write(dumps_json(payload))
        self.out.write("\n")
        self.out.flush()

    def _open_output(self) -> None:
        path = ctx.options.ai_jsonl_outfile or "-"
        if self.out and self.path == path:
            return
        if self.out and self.out is not sys.stdout:
            self.out.close()
        self.path = path
        if path == "-":
            self.out = sys.stdout
            return
        target = Path(path).expanduser()
        target.parent.mkdir(parents=True, exist_ok=True)
        self.out = target.open("a", encoding="utf-8")


addons = [AIJsonl()]
