// Playwright loader: the cloud image ships it globally at /opt/node22; fall back to a normal install.
try { module.exports = require('/opt/node22/lib/node_modules/playwright'); }
catch (e) { module.exports = require('playwright'); }
