import 'dotenv/config';
import { execa }   from 'execa';
import prompts     from 'prompts';
import fs          from 'fs';
import path        from 'path';

(async () => {
  let [, , ...rawArgs] = process.argv;

  if (rawArgs.length === 0) {
    const resp = await prompts([
      { type: 'text',   name: 'symbol',   message: 'Ticker symbol?' },
      { type: 'select', name: 'interval', message: 'Interval?',
        choices: [
          { title: '1 minute',  value: 'm1'  },
          { title: '5 minutes', value: 'm5'  },
          { title: '15 mins',   value: 'm15' },
          { title: '30 mins',   value: 'm30' },
          { title: '1 hour',     value: 'h1'  },
          { title: '1 day',      value: 'd1'  },
        ]
      }
    ]);
    rawArgs = [`--symbol=${resp.symbol}`, `--interval=${resp.interval}`];
  }

  // 3) Locate the venv Python (Windows vs. Linux), fallback to python
  const root     = process.cwd();
  const winPy    = path.join(root, '.venv', 'Scripts', 'python.exe');
  const nixPy    = path.join(root, '.venv', 'bin',     'python');
  const pythonCmd = fs.existsSync(winPy)
    ? winPy
    : fs.existsSync(nixPy)
      ? nixPy
      : 'python';

  console.log(`▶ running ${pythonCmd} -m bot.core ${rawArgs.join(' ')}`);

  await execa(pythonCmd, ['-m', 'bot.core', ...rawArgs], {
    stdio: 'inherit',
    env:   process.env
  });
})();
