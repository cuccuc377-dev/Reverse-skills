export const VIEWPORT_WIDTH_MIN = 320;
export const VIEWPORT_WIDTH_MAX = 3840;
export const VIEWPORT_HEIGHT_MIN = 240;
export const VIEWPORT_HEIGHT_MAX = 2160;

export interface ViewportSize {
  width: number;
  height: number;
}

export function isViewportWithinBounds(width: number, height: number): boolean {
  return (
    Number.isInteger(width) &&
    Number.isInteger(height) &&
    width >= VIEWPORT_WIDTH_MIN &&
    width <= VIEWPORT_WIDTH_MAX &&
    height >= VIEWPORT_HEIGHT_MIN &&
    height <= VIEWPORT_HEIGHT_MAX
  );
}

export function parseViewportString(raw: string | undefined): ViewportSize | undefined {
  if (!raw) return undefined;

  const match = raw.trim().match(/^(\d+)x(\d+)$/);
  if (!match) return undefined;

  const width = Number.parseInt(match[1], 10);
  const height = Number.parseInt(match[2], 10);

  return isViewportWithinBounds(width, height) ? { width, height } : undefined;
}
