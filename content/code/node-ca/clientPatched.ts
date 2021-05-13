import * as axios from 'axios';
import * as caAppend from 'ca-append';
import * as fs from 'fs';
import * as https from 'https';
import * as process from 'process';

caAppend.monkeyPatch();

function makeOptions(opts: caAppend.SecureContextOptions): axios.AxiosRequestConfig {
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
  // Try **without** specifying `caAppend`
  const optionsWithout = makeOptions({});
  try {
    const response = await axios.default.get(url, optionsWithout);
    console.log('Success when `ca` / `caAppend` not included:');
    console.log(`  response.status: ${response.status}`);
  } catch (err) {
    console.log('Failure when `ca` / `caAppend` not included:');
    console.log(`  error code:    ${err.code}`);
    console.log(`  error message: ${err.message}`);
  }
  // Try **with** specifying `ca`
  const customRootCA = await fs.promises.readFile(`${__dirname}/root-ca-cert.pem`);
  try {
    const optionsWithCA = makeOptions({ ca: [customRootCA] });
    const response = await axios.default.get(url, optionsWithCA);
    console.log('Success when `ca` included:');
    console.log(`  response.status: ${response.status}`);
  } catch (err) {
    console.log('Failure when `ca` included:');
    console.log(`  error code:    ${err.code}`);
    console.log(`  error message: ${err.message}`);
  }
  // Try **with** specifying `caAppend`
  const optionsWithCAAppend = makeOptions({ caAppend: [customRootCA] });
  try {
    const response = await axios.default.get(url, optionsWithCAAppend);
    console.log('Success when `caAppend` included:');
    console.log(`  response.status: ${response.status}`);
  } catch (err) {
    console.log('Failure when `caAppend` included:');
    console.log(`  error code:    ${err.code}`);
    console.log(`  error message: ${err.message}`);
  }
}

if (require.main === module) {
  main().catch(console.error);
}
