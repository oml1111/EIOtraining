(function(){var n={cedexis:!1,constellationPerfMap:!0,constellationDNSTiming:!1,constellationResolverLatency:!1,resourceTimings:!1,allowHTTPS:!1},k=function(){var a="performance"in window&&"undefined"!=typeof window.performance&&"undefined"!=typeof window.performance.getEntriesByType,b=null;a&&(b=window.performance.getEntriesByType("resource"));b=a&&b instanceof Array&&0<b.length;return{perfTimingsSupported:a&&b,notRunRecently:-1==document.cookie.indexOf("fastlyPerf="),isHTTP:"http:"==window.location.protocol}}(),
w={},m=document.getElementsByTagName("script"),h=0;for(;h<m.length;h++){var p=m[h].hasAttribute("src"),x=m[h].getAttribute("src");if(p&&null!==x.match(/\/fastly\.js\?/)&&(p=x.split("?"),2==p.length&&""!==p[1])){m=p[1].split("&");for(h=0;h<m.length;h++)p=m[h].split("="),"undefined"!==typeof p[1]?w[decodeURIComponent(p[0])]=decodeURIComponent(p[1]):w[decodeURIComponent(p[0])]=p[1];break}}var m=function(a,b){return function(){try{return b.apply(this,arguments)}catch(c){"KnownError"==c.name?(new Image).src=
"//www.fastly-analytics.com/beacon?issue&where="+a+"&kind="+c.kind:(new Image).src="//www.fastly-analytics.com/beacon?error&where="+a+"&message="+encodeURIComponent(c.message)}}},s=function(){for(var a=(new Date).getTime(),b=0;8>b;b++)a+="abcdefghijklmnopqrstuvwxyz0123456789".charAt(Math.floor(36*Math.random()));return a+"-perfmap"}(),v=function(a){return 0===a.requestStart?{}:{domainLookupTime:Math.round(a.domainLookupEnd-a.domainLookupStart),timeToFirstByte:Math.round(a.responseStart-a.requestStart),
downloadTime:a.domainLookupEnd-a.domainLookupStart+(a.connectEnd-a.connectStart)+(a.responseEnd-a.requestStart)}},A=function(){n.cedexis&&function(a,c){var f=function(){var f=c.createElement("script");f.type="text/javascript";void 0!==f.setAttribute&&f.setAttribute("async","async");f.src="//"+("https:"===a.location.protocol?"s3.amazonaws.com/cdx-radar/":"radar.cedexis.com/")+"01-10587-radar10.min.js";c.body.appendChild(f)};"complete"==document.readyState?f():a.addEventListener?a.addEventListener("load",
f,!1):a.attachEvent&&a.attachEvent("onload",f)}(window,document);if("undefined"!=typeof w.cb)try{window[w.cb]()}catch(a){}},h=m("initPerfmap",function(){if(n.constellationPerfMap&&k.notRunRecently&&(k.isHTTP||n.allowHTTPS)){var a=new Date;a.setMinutes(a.getMinutes()+15);document.cookie="fastlyPerf=timeout; Expires="+a.toUTCString()+"; Path=/;";y("//"+s+".u.fastly-analytics.com/perfmapconfig.js?jsonp=FASTLY.setupPerfmap")}else B()}),g,p=m("setupPerfmap",function(a){g=a;if("undefined"!=typeof g.domains)for(a=
0;a<g.domains.length;a++)y("//"+g.domains[a].hostname+"/popname.js?jsonp=FASTLY.setPopName&unique="+s)}),x=m("setPopName",function(a){for(var b=!1,c=0;c<g.domains.length;c++){var f=g.domains[c];a.hostname===f.hostname?f.popname=a.popname:"undefined"==typeof f.popname&&(b=!0)}!b&&"undefined"!=typeof g.pops&&C()}),C=m("perfmapPop",function(){if(k.perfTimingsSupported)for(var a=g.pops.length,b=0;b<a;b++){var c=g.pops[b];if("undefined"===typeof c.url){c.url="//"+c.hostname+"/test_object.svg?unique="+
s+"&popId="+c.popId;a=new Image;a.onload=C;a.onerror=C;a.src=c.url;return}}I()}),I=m("perfmapDone",function(){var a={geoip:{},popLatency:{},popAssignments:{}},b="?id="+s;if("undefined"!=typeof g.geo_ip)for(var c in g.geo_ip)g.geo_ip.hasOwnProperty(c)&&(b+="&"+c+"="+encodeURIComponent(g.geo_ip[c]),a.geoip[c]=g.geo_ip[c]);if(k.perfTimingsSupported){var f=window.performance.getEntriesByType("resource");for(c=0;c<f.length;c++){var e=f[c];if(0<e.responseStart){var d=e.name.match("/test_object.svg\\?unique="+
s+"&popId=(.*)");d&&1<=d.length&&(d=d[1],e=v(e).timeToFirstByte,b+="&"+d+"="+e,a.popLatency[d]=e)}}}b+="&customerId=webpagetest";if("undefined"!=typeof g.domains){f=g.domains;for(c=0;c<f.length;c++)e=f[c],"undefined"!=typeof e.popname&&(b+="&"+e.type+"="+e.popname,a.popAssignments[e.type]=e.popname)}b+="&https="+(k.isHTTP?"0":"1");b+="&t1="+encodeURIComponent(new Date);try{var r=Intl.DateTimeFormat().resolvedOptions().timeZone;"undefined"!=typeof r&&(b+="&t2="+r)}catch(h){}z(["//"+s+".u.fastly-analytics.com/generate_204",
"//www.fastly-analytics.com/beacon"+(b+"&v=3.8")],B);q.results.perfmap=a}),u=function(){return Math.floor(1E10*Math.random())},J=function(a,b,c){a=String(a);return a.length>=b?a:Array(b-a.length+1).join(c)+a},D=function(){if(!k.perfTimingsSupported||!k.notRunRecently||!n.constellationResolverLatency||!k.isHTTP&&!n.allowHTTPS)A();else{var a="//"+u()+".rand.fastly-analytics.com/test_object.svg",b=function(){for(var b=window.performance.getEntriesByType("resource"),c,d,r,h=b.length-1;0<h;h--){var g=
b[h];parsedEntry=v(g);g.name.match(/\/\/cacheme1-d.fastly-analytics.com\/test_object.svg/)?c=parsedEntry.domainLookupTime:g.name.match(/\/\/cacheme2-d.fastly-analytics.com\/test_object.svg/)?d=parsedEntry.domainLookupTime:-1!==g.name.indexOf(a)&&(r=parsedEntry.domainLookupTime);if("undefined"!=typeof c&&"undefined"!=typeof d&&"undefined"!=typeof r)break}q.results.resolverDistance={cacheme1:c,cacheme2:d,nocache:r};z(["//www.fastly-analytics.com/beacon-d?id="+s+"&cacheme1="+c+"&cacheme2="+d+"&nocache="+
r+"&nonce="+u()+"&v=3.8"],A)},c=function(){G(["//cacheme1-d.fastly-analytics.com/test_object.svg?"+u(),"//cacheme2-d.fastly-analytics.com/test_object.svg?"+u()],b)};z([a],function(){for(var b=window.performance.getEntriesByType("resource"),e=!0,d=b.length-1;0<=d;d--){var r=b[d];if(0<r.name.indexOf(a)&&0<v(r).domainLookupTime){e=!1;break}}if(e)A();else{b=[];for(d=0;10>d;d++)b.push("//"+J(d+1,2,"0")+"-d.fastly-analytics.com/test_object.svg?"+u());z(b,c)}})}},E=[],F=function(a){return E.push(a)-1},H=
function(a){if(0<a--){var b=F(H(a)),c,f,e=F(function(a){f=a.popname;a=window.performance.getEntriesByType("resource");for(var d,e,l=a.length-1;0<l;l--){var g=a[l],h=v(g);g.name.match(/:\/\/.*?\.beacon\.fastlydns\.net\//)?d=h.domainLookupTime:g.name.match(/:\/\/.*?\.rand\.fastly-analytics\.com\//)&&(e=h.domainLookupTime);if("undefined"!=typeof d&&"undefined"!=typeof e)break}0===d&&0===e||"number"!=typeof d||"number"!=typeof e?D():(a=new Image,a.onload=a.onerror=q["globalCallback"+b],a.src="//www.fastly-analytics.com/beacon-astral?id="+
s+"&dy="+e+"&dypop="+f+"&as="+d+"&aspop="+c+"&v=3.8&nonce="+u(),q.results.dnsTimings=q.results.dnsTimings||[],q.results.dnsTimings.push({dyTime:e,dyPopName:f,asTime:d,asPopName:c}))}),d=F(function(a){c=a.popname;a=u()+".rand.fastly-analytics.com";y("//"+a+"/popname.js?jsonp=FASTLY.globalCallback"+e)});return function(){var a=u()+".beacon.fastlydns.net";y("//"+a+"/popname.js?jsonp=FASTLY.globalCallback"+d)}}return D},B;B=n.constellationDNSTiming&&k.perfTimingsSupported&&(k.isHTTP||n.allowHTTPS)&&k.notRunRecently?
H(3):D;var z=function(a,b){for(var c=a.length,f=function(){c--;0===c&&b()},e=0;e<a.length;e++){var d=new Image;d.onload=d.onerror=f;d.src=a[e]}},G=function(a,b){if(0<a.length){var c=a.shift(),f=new Image;f.onload=f.onerror=function(){G(a,b)};f.src=c}else b()},y=function(a){var b=document.createElement("script");b.type="text/javascript";b.async=!0;b.src=a;a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(b,a)};(function(a){"complete"==document.readyState?a():window.addEventListener?
window.addEventListener("load",a,!1):window.attachEvent&&window.attachEvent("onload",a)})(h);n.resourceTimings&&function(){var a=n.resdomains,b,c=[],f=[],e=document.createElement("a"),d=function(){b=!0;if(a&&0<a.length&&(b=!1,a&&0<a.length))for(var l=0,d=a.length;l<d;l++){var e=a[l];0===e.indexOf("*.")&&a.push("^"+e.replace(/^\*\./,"")+"$");a[l]="^"+e.replace(/\./g,"\\.").replace(/^\*\\\./,".*\\.")+"$"}t=performance.timing;t.name=document.location.href;t.duration=t.responseEnd-(0<t.redirectStart?
t.redirectStart:t.fetchStart);t.startTime=t.navigationStart;l=performance.getEntriesByType("resource");d=0;for(e=l.length;d<e;d++){var k=l[d];0!==k.requestStart&&g(k.name)&&(c.push(k),f.push(v(k).downloadTime))}g(window.location.href)&&(t=performance.timing,c.push(t),f.push(v(t).downloadTime));l="//www.fastly-analytics.com/restiming?v=3.8&cid=webpagetest&nav="+h(performance.timing,!1,!0);f.sort(p);for(var d=f[4],e=[],m=k=0;k<c.length;k++){var q=c[k],n=v(q).downloadTime,n=5>m&&n>=d&&0<n,m=m+(n?1:0);
e.push(h(q,n))}l+="&res="+e.join(",");2E3<l.length&&(l=l.substr(0,2E3),l=l.substr(0,l.lastIndexOf(",")));(new Image).src=l},g=function(c){if(b)return!0;e.href=c;c=e.hostname;for(var d=0;d<a.length;d++)if(c.match(a[d]))return!0;return!1},h=function(a,b,c){var d=Math.round(a.redirectEnd-a.redirectStart),e=Math.round(a.domainLookupEnd-a.domainLookupStart),f=Math.round(a.connectEnd-a.connectStart),g=a.secureConnectionStart?Math.round(a.connectEnd-a.secureConnectionStart):"",h=Math.round(a.responseStart-
a.requestStart),k=Math.round(a.responseEnd-a.responseStart),m=Math.round(a.duration);c="f"+Math.round(a.fetchStart)+"u"+m+(d?"r"+d:"")+(e?"d"+e:"")+(f?"n"+f:"")+(g?"s"+g:"")+(h?"t"+h:"")+(k?"c"+k:"")+(c&&a.loadEventStart?"p"+(a.loadEventStart-a.fetchStart):"");b&&(c+=encodeURIComponent(a.name).substr(0,200));return c},p=function(a,b){return b-a};a&&k.perfTimingsSupported&&("complete"==document.readyState?d():window.addEventListener?window.addEventListener("load",d,!1):window.attachEvent&&window.attachEvent("onload",
d))}();var q=window.FASTLY=window.FASTLY||{};q.setupPerfmap=p;q.setPopName=x;for(h=0;h<E.length;h++)q["globalCallback"+h]=E[h];q.results={caps:k};q.version=3.8})();