const fs = require('fs');
// usage: node scripts/verify-pack.js <unpacked-package-dir> <engine-tree>
//   e.g. node scripts/verify-pack.js D:/tmp/purge_work/verify17/package D:/tmp/purge_work/eng110
const pkgDir = process.argv[2] || 'D:/tmp/purge_work/verify17/package';
const engTree = process.argv[3] || 'D:/tmp/purge_work/eng110';
const core = require(pkgDir + '/lib/core.js');
(async () => {
  const tree = 'D:/tmp/purge_work/run5_g17_verify';
  fs.rmSync(tree, { recursive: true, force: true });
  fs.cpSync(engTree, tree, { recursive: true });
  const aiBase = tree + '/node_modules/@deepseek-ai';
  const rep = await core.applyPatches(aiBase, core.ALL_PATCHES, { preserveClientBundles: false, forApply: true });
  const tally = {};
  for (const r of rep) tally[r.status] = (tally[r.status] || 0) + 1;
  console.log('tally', JSON.stringify(tally));
  const f = tree + '/node_modules/@deepseek-ai/dsh-api-session-controller/lib/index.js';
  const t = fs.readFileSync(f, 'utf8');
  const m = t.match(/case "steer":[\s\S]{0,340}?break;/);
  console.log('STEER:'); console.log(m ? m[0] : 'NOT FOUND');
  console.log('marker86', (t.match(/\[dsh-purge-86\] queue steer/g) || []).length, 'steer(msg)', (t.match(/agent\.steer\(message\);/g) || []).length);
  let marks = 0;
  const walk = d => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = d + '/' + e.name; if (e.isDirectory()) walk(p); else if (e.name.endsWith('.js')) { marks += (fs.readFileSync(p, 'utf8').match(/dsh-purge-\d+/g) || []).length; } } };
  walk(aiBase);
  console.log('total markers', marks);
  const pkg = JSON.parse(fs.readFileSync(pkgDir + '/package.json', 'utf8'));
  console.log('pkg', pkg.version, '|', pkg.dsh.install.tarball);
})().catch(e => { console.error('ERR', e && e.stack || e); process.exit(1); });