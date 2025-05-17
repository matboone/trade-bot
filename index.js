import 'dotenv/config'
import { execa }    from 'execa'
import prompts      from 'prompts'

(async () => {
  let [, , ...rawArgs] = process.argv

  if (rawArgs.length === 0) {
    const resp = await prompts([
      { type: 'text',   name: 'symbol',   message: 'Ticker symbol?' },
      { type: 'select', name: 'interval',
        message: 'Choose an interval',
        choices: [
          { title: '1 minute',  value: 'm1' },
          { title: '5 minutes', value: 'm5' },
          { title: '15 minutes',value: 'm15' },
          { title: '30 minutes',value: 'm30' },
          { title: '1 hour',    value: 'h1' },
          { title: '1 day',     value: 'd1' },
        ]
      }
    ])
    rawArgs = [`--symbol=${resp.symbol}`, `--interval=${resp.interval}`]
  }

  await execa('python', ['-m','bot.core', ...rawArgs], {
    stdio: 'inherit',
    env: process.env
  })
})()
