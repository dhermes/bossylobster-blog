const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  msg = [
    `req.ip: ${JSON.stringify(req.ip)}`,
    `req.xff: ${JSON.stringify(req.get('x-forwarded-for'))}`,
    '',
  ].join('\n')
  res.send(msg)
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
