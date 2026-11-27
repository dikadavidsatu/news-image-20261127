// main.ts — the hand-off program for the 27 November 2026 edition of
// "The World Today — One Image Edition", entered in make.fun's
// news-image-20261127 ("Sum up 27 November's world news in one image").
//
// The picture is already finished before this program ever runs:
// entry.png, sitting beside this file, is a 1024x1024 broadsheet front
// page that packs a whole day of wire news — 33 stories — into a
// single frame. The lead reports Washington's plan for fresh tariffs
// aimed at 14 trading partners; the second story covers the drone
// strike in Kuwait that killed two Italian technicians; the rest of
// the day fills the columns below them. render.py drew the page
// offline, ahead of time, because the grading sandbox gives this
// program no network, no fonts and no Python — and mounts the
// repository read-only besides.
//
// So delivery is the only job left, and this program keeps it as
// plain as possible: straight-line, fully synchronous code, nothing
// but node:fs sync calls and a SHA-256 from node:crypto.
//
//   * The PNG is located (beside this script first, then the working
//     directory, then /bot) and read into memory exactly once. Its
//     byte length and SHA-256 are the reference every later check
//     compares against.
//   * The destination folder is $MAKEFUN_OUTPUT_DIR when that is set
//     to something non-empty, otherwise /output when it exists,
//     otherwise an "output" folder under the working directory.
//   * The in-memory bytes are written to <folder>/entry.png TWICE.
//     After each write the landed file is read back and checked —
//     same length, same hash — so the copy the grader eventually
//     opens is the second write, already proven identical. A torn
//     first write can never be what gets judged.
//   * Nothing is written anywhere else. The repository stays
//     untouched, which matters because it may be read-only.
//
// Any failure along the way throws, is caught at the bottom, and
// ends the process with exit code 1: a broken delivery must be loud,
// never a quietly corrupted front page.

import { createHash } from "node:crypto";
import {
  existsSync,
  mkdirSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PAGE_FILE = "entry.png";

/** Hex SHA-256 fingerprint of a buffer. */
function fingerprint(bytes: Buffer): string {
  return createHash("sha256").update(bytes).digest("hex");
}

/**
 * Where the committed page lives. The script's own directory is the
 * normal case; the working directory and /bot are the fallbacks for
 * harnesses that invoke the program from somewhere else.
 */
function locatePage(): string {
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  const candidates = [
    join(scriptDir, PAGE_FILE),
    join(process.cwd(), PAGE_FILE),
    join("/bot", PAGE_FILE),
  ];
  for (const candidate of candidates) {
    if (existsSync(candidate)) return candidate;
  }
  throw new Error(
    `entry.png not found; tried ${candidates.join(", ")}`,
  );
}

/** The folder the harness wants the page delivered into. */
function outputFolder(): string {
  const fromEnv = process.env.MAKEFUN_OUTPUT_DIR;
  if (fromEnv && fromEnv.trim().length > 0) return resolve(fromEnv);
  if (existsSync("/output")) return "/output";
  return resolve(process.cwd(), "output");
}

/**
 * Write the page bytes to the target, then read the file back and
 * prove it is the same page: identical length and identical SHA-256.
 */
function writeAndProve(
  pageBytes: Buffer,
  pageHash: string,
  target: string,
  passName: string,
): void {
  writeFileSync(target, pageBytes);
  const landed = readFileSync(target);
  if (landed.length !== pageBytes.length) {
    throw new Error(
      `${passName}: wrote ${pageBytes.length} bytes but read back ` +
        `${landed.length}`,
    );
  }
  if (fingerprint(landed) !== pageHash) {
    throw new Error(`${passName}: landed bytes hash differently`);
  }
}

function deliver(): void {
  const sourcePath = locatePage();
  const pageBytes = readFileSync(sourcePath);
  const pageHash = fingerprint(pageBytes);

  const folder = outputFolder();
  mkdirSync(folder, { recursive: true });
  const target = join(folder, PAGE_FILE);

  // Never deliver on top of the committed page itself: if the output
  // folder somehow resolves to the repository, writing there would
  // destroy the very artifact being verified. Refuse instead.
  if (resolve(target) === resolve(sourcePath)) {
    throw new Error(
      `output path ${target} is the committed page; refusing to overwrite it`,
    );
  }

  // Two complete writes from the same in-memory buffer, each one
  // verified after it lands; the second verified write is final.
  writeAndProve(pageBytes, pageHash, target, "first write");
  writeAndProve(pageBytes, pageHash, target, "second write");

  console.log(
    `delivered entry.png -> ${target} ` +
      `(${pageBytes.length} bytes, sha256 ${pageHash}, verified twice)`,
  );
}

try {
  deliver();
} catch (err) {
  console.error(
    `delivery failed: ${err instanceof Error ? err.message : String(err)}`,
  );
  process.exit(1);
}
