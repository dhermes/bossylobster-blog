import * as axios from 'axios';
import * as fs from 'fs';
import * as https from 'https';
import * as process from 'process';
import * as tls from 'tls';

function makeOptions(opts: tls.SecureContextOptions): axios.AxiosRequestConfig {
  const pool = new https.Agent({ ...opts, maxSockets: 1 });
  return {
    httpsAgent: pool,
    validateStatus: (): boolean => {
      return true;
    },
    maxRedirects: 0,
  };
}

function getURL(argv: string[]): string {
  if (argv.length === 0) {
    throw new Error('No argv present');
  }
  return argv[argv.length - 1];
}

async function main() {
  const url = getURL(process.argv);
  console.log(`Using URL=${JSON.stringify(url)};`);
  // Try **without** specifying `ca`
  const optionsWithout = makeOptions({});
  try {
    const response = await axios.default.get(url, optionsWithout);
    console.log('Success when `ca` not included:');
    console.log(`  response.status: ${response.status}`);
  } catch (err) {
    console.log('Failure when `ca` not included:');
    console.log(`  error code:    ${err.code}`);
    console.log(`  error message: ${err.message}`);
  }
  // Try **with** specifying `ca`
  const customRootCA = await fs.promises.readFile(`${__dirname}/root-ca-cert.pem`);
  const optionsWith = makeOptions({ ca: [customRootCA] });
  try {
    const response = await axios.default.get(url, optionsWith);
    console.log('Success when `ca` included:');
    console.log(`  response.status: ${response.status}`);
  } catch (err) {
    console.log('Failure when `ca` included:');
    console.log(`  error code:    ${err.code}`);
    console.log(`  error message: ${err.message}`);
  }
}

if (require.main === module) {
  main().catch(console.error);
}
