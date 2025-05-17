import 'dotenv/config';           // loads WEBULL_USER/PASS from .env
import express from 'express';
import { execa } from 'execa';

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/backtest', async (req, res) => {
  const symbol   = (req.query.symbol   || 'SOFI').toUpperCase();
  const interval = req.query.interval || 'm30';

  try {
    const { stdout } = await execa(
      'python',
      ['-m', 'bot.core', `--symbol=${symbol}`, `--interval=${interval}`],
      { env: process.env }
    );

    res.type('text/plain').send(stdout);

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.shortMessage || err.message });
  }
});

app.listen(PORT, () => {
  console.log(`API listening at http://localhost:${PORT}`);
});
