// index.js  – hard‑wire the virtual‑env python if it exists
import fs from 'node:fs';
import path from 'node:path';
import { execa } from 'execa';
import 'dotenv/config';

const repoRoot = process.cwd();
const venvPy   = path.join(repoRoot, '.venv', 'Scripts', 'python.exe');

// prefer .venv\Scripts\python.exe if the file exists
const pythonCmd = fs.existsSync(venvPy) ? venvPy : 'python';

const [, , ...rawArgs] = process.argv;
console.log(`▶ launching ${pythonCmd} -m bot.core ${rawArgs.join(' ')}`);

await execa(
  pythonCmd,
  ['-m', 'bot.core', ...rawArgs],
  { stdio: 'inherit', env: process.env }
);