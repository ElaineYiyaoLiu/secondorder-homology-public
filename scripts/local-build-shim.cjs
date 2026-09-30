// Local sandbox workaround only. Not invoked by the Vercel build command.
const v8=require('node:v8');
const original=process.memoryUsage.bind(process);
const fallback=()=>{const h=v8.getHeapStatistics();return {rss:h.total_heap_size+128*1024*1024,heapTotal:h.total_heap_size,heapUsed:h.used_heap_size,external:h.external_memory,arrayBuffers:0};};
process.memoryUsage=()=>{try{return original()}catch(error){if(error?.code!=='ENOENT')throw error;return fallback()}};
process.memoryUsage.rss=()=>process.memoryUsage().rss;
