import 'dotenv/config'
import { execa } from 'execa'

// no more venv path checks — rely on the activated venv
const pythonCmd = 'python'

const [, , ...rawArgs] = process.argv

await execa(pythonCmd, ['-m','bot.core', ...rawArgs], {
  stdio: 'inherit',
  env: process.env
})
