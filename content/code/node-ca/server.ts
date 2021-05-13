import * as fs from 'fs';
import * as https from 'https';
import * as process from 'process';

function getPort(argv: string[]): number {
  if (argv.length === 0) {
    throw new Error('No argv present');
  }
  const lastArg = argv[argv.length - 1];
  const port = parseInt(lastArg);
  if (port.toString() !== lastArg) {
    throw new Error(`Could not convert port argument to integer: ${JSON.stringify(lastArg)}`);
  }
  return port;
}

function main() {
  const port = getPort(process.argv);
  const options = {
    key: fs.readFileSync(`${__dirname}/localhost-key.pem`),
    cert: fs.readFileSync(`${__dirname}/localhost-cert.pem`),
  };
  https
    .createServer(options, (_req, res) => {
      res.writeHead(200);
      res.end('hello world\n');
    })
    .listen(port);

  console.log(`Running TLS server on localhost:${port}`);
}

if (require.main === module) {
  main();
}
