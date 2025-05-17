import fs from 'fs'
import path from 'path'
import { execa } from 'execa'
import 'dotenv/config'

const root = process.cwd()
const winPy = path.join(root, '.venv', 'Scripts', 'python.exe')
const nixPy = path.join(root, '.venv', 'bin', 'python')

const pythonCmd = fs.existsSync(nixPy)
  ? nixPy
  : fs.existsSync(winPy)
    ? winPy
    : 'python'

const [, , ...rawArgs] = process.argv

console.log(`▶ running ${pythonCmd}`)

await execa(pythonCmd, ['-m','bot.core', ...rawArgs], {
  stdio: 'inherit',
  env: process.env
})
