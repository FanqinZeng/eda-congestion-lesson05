import {writeFileSync} from 'node:fs';
import {compute,PRESETS} from '../site/assets/engine.mjs';
const data={presets:PRESETS,results:{}};
for(const [name,instance] of Object.entries(PRESETS))data.results[name]={path:compute(instance),upstream:compute(instance,{mode:'upstream'})};
writeFileSync(new URL('../video/data.json',import.meta.url),JSON.stringify(data,null,2)+'\n');
writeFileSync(new URL('../site/downloads/examples.json',import.meta.url),JSON.stringify(PRESETS,null,2)+'\n');
console.log('Exported authored engine traces and fixtures');
