import assert from 'node:assert/strict';
import http from 'node:http';
import next from 'next';
const app=next({dev:false});await app.prepare();
const server=http.createServer(app.getRequestHandler());
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
try{
 const base='http://127.0.0.1:'+server.address().port;
 const res=await fetch(base);assert.equal(res.status,200);const html=await res.text();assert.ok(html.includes('SecondOrder Homology'));assert.ok(html.includes('导出报告'));
 const data=await fetch(base+'/data/demo.json');assert.equal(data.status,200);const report=await data.json();assert.equal(report.symbols.length,30);assert.equal(report.source.kind,'synthetic');
 console.log('Production HTTP QA: HTML and complete research report return 200.');
}finally{await new Promise(resolve=>server.close(resolve));await app.close();}
