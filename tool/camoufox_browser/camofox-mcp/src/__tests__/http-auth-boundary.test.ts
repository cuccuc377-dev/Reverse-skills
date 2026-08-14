import { afterEach, describe, expect, it, vi } from "vitest";

import { once } from "node:events";
import type { Server } from "node:http";
import type { AddressInfo } from "node:net";

const createServerMock = vi.hoisted(() => vi.fn());

vi.mock("../server.js", () => ({
  createServer: createServerMock
}));

import { loadConfig } from "../config.js";
import { createMcpHttpApp } from "../http.js";

const servers: Server[] = [];

afterEach(async () => {
  createServerMock.mockReset();
  await Promise.all(
    servers.splice(0).map(
      (server) =>
        new Promise<void>((resolve, reject) => {
          server.close((error) => {
            if (error) {
              reject(error);
              return;
            }
            resolve();
          });
        })
    )
  );
});

async function listen(app: ReturnType<typeof createMcpHttpApp>): Promise<string> {
  const server = app.listen(0, "127.0.0.1");
  servers.push(server);
  await once(server, "listening");
  const address = server.address() as AddressInfo;
  return `http://127.0.0.1:${address.port}`;
}

describe("http auth boundary", () => {
  it("rejects unauthenticated MCP requests before creating a tool server", async () => {
    const config = loadConfig([], {
      CAMOFOX_TRANSPORT: "http",
      CAMOFOX_API_KEY: "server-side-browser-secret",
      CAMOFOX_HTTP_API_KEY: "0123456789abcdef0123456789abcdef"
    } as NodeJS.ProcessEnv);
    const baseUrl = await listen(createMcpHttpApp(config));

    const response = await fetch(`${baseUrl}/mcp`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/list", params: {} })
    });

    expect(response.status).toBe(401);
    expect(createServerMock).not.toHaveBeenCalled();
  });
});
