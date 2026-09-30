import {existsSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
const python=process.env.HOMOLOGY_PYTHON||(existsSync('.venv/bin/python')?'.venv/bin/python':'python');
const result=spawnSync(python,process.argv.slice(2),{stdio:'inherit'});
if(result.error){console.error('Python unavailable. Follow the README setup.');process.exit(1)}
process.exit(result.status??1);
