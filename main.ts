// main.ts — delivery program for "The World Today — One Image Edition",
// the make.fun entry for news-image-20261127 ("Sum up 27 November's
// world news in one image").
//
// What the grader runs is this file. The artwork itself — a 1024x1024
// broadsheet front page carrying 33 stories from Thursday 27 November
// 2026 — is committed beside it as entry.png, rendered offline by
// render.py from the researched headlines in headlines.json. Rendering
// is deliberately NOT done here: the grading sandbox mounts this
// repository read-only and offers no network, fonts package or Python,
// so the only safe job left at run time is delivery.
//
// Delivery contract:
//   1. Find the committed entry.png (next to this file; the working
//      directory is the fallback).
//   2. Resolve the output folder: $MAKEFUN_OUTPUT_DIR when the harness
//      sets it, else /output when that exists, else ./output.
//   3. Copy the image into that folder TWICE, and after each copy read
//      the landed file back and verify it byte-for-byte against the
//      committed original (length + SHA-256). The second, verified copy
//      is the file the harness grades, so a torn or truncated first
//      write can never be what gets judged.
//   4. Write NOTHING anywhere else — in particular, never into the
//      repository, which may be mounted read-only.
//
// The program is deterministic: same repository in, same bytes out,
// no clocks, no randomness, no network. It exits non-zero if any
// verification fails, rather than delivering a corrupted front page.

import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { copyFile, mkdir, readFile, stat } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const IMAGE_NAME = "entry.png";

/** SHA-256 of a buffer, hex-encoded — the fingerprint we verify with. */
function sha256(bytes: Buffer): string {
  return createHash("sha256").update(bytes).digest("hex");
}

/**
 * Locate the committed entry.png. The canonical home is the directory
 * containing this file (the repository root); if the harness copied
 * the program elsewhere, fall back to the working directory.
 */
function findSourceImage(): string {
  const here = dirname(fileURLToPath(import.meta.url));
  const beside = join(here, IMAGE_NAME);
  if (existsSync(beside)) return beside;
  const inCwd = join(process.cwd(), IMAGE_NAME);
  if (existsSync(inCwd)) return inCwd;
  throw new Error(
    `cannot find ${IMAGE_NAME}: looked in ${here} and ${process.cwd()}`,
  );
}

/**
 * Resolve the output folder exactly as the harness contract states:
 * MAKEFUN_OUTPUT_DIR first, then /output, then ./output relative to
 * the working directory.
 */
function resolveOutputDir(): string {
  const fromEnv = process.env.MAKEFUN_OUTPUT_DIR;
  if (fromEnv && fromEnv.trim().length > 0) return resolve(fromEnv);
  if (existsSync("/output")) return "/output";
  return resolve(process.cwd(), "output");
}

/**
 * Copy source -> target once, then prove the landed file is the same
 * bytes as the source: equal length and equal SHA-256. Throws on any
 * mismatch so main() can fail the run loudly.
 */
async function copyAndVerify(
  source: string,
  target: string,
  expectedHash: string,
  expectedSize: number,
  passLabel: string,
): Promise<void> {
  await copyFile(source, target);
  const landed = await readFile(target);
  const landedInfo = await stat(target);
  if (landed.length !== expectedSize || landedInfo.size !== expectedSize) {
    throw new Error(
      `${passLabel}: size mismatch — expected ${expectedSize} bytes, ` +
        `landed ${landed.length}`,
    );
  }
  const landedHash = sha256(landed);
  if (landedHash !== expectedHash) {
    throw new Error(
      `${passLabel}: sha256 mismatch — expected ${expectedHash}, ` +
        `landed ${landedHash}`,
    );
  }
  console.log(`${passLabel}: verified ${target} (${landed.length} bytes)`);
}

async function main(): Promise<void> {
  const source = findSourceImage();
  const original = await readFile(source);
  const fingerprint = sha256(original);

  const outDir = resolveOutputDir();
  await mkdir(outDir, { recursive: true });
  const target = join(outDir, IMAGE_NAME);

  console.log(`source: ${source}`);
  console.log(`image:  ${original.length} bytes, sha256 ${fingerprint}`);
  console.log(`output: ${target}`);

  // Two full copies, each verified after it lands. The harness reads
  // the file only after this program exits, so what it grades is the
  // second, proven-identical copy.
  await copyAndVerify(source, target, fingerprint, original.length, "copy 1/2");
  await copyAndVerify(source, target, fingerprint, original.length, "copy 2/2");

  // Belt and braces: re-read the committed source one last time. If
  // its fingerprint moved during the run, the copies above may have
  // raced a changing file — fail rather than grade a moving target.
  const sourceNow = await readFile(source);
  if (sha256(sourceNow) !== fingerprint) {
    throw new Error("source entry.png changed during delivery; aborting");
  }

  console.log(
    `delivery complete: entry.png is in place, byte-identical ` +
      `(sha256 ${fingerprint})`,
  );
}

main().catch((err: unknown) => {
  console.error("delivery failed:", err instanceof Error ? err.message : err);
  process.exit(1);
});
