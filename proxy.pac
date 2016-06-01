function FindProxyForURL(url,host) {
var me=myIpAddress();
var resolved_ip = dnsResolve(host);
if (host == "127.0.0.1") {return "DIRECT";}
if (host == "localhost") {return "DIRECT";}
if (isPlainHostName(host)) {return "DIRECT";}
if (host == "bpg.fm.intil.com") {return "PROXY iceadmin.ice.intil.com:811";}
if (host == "bpg-in.fm.intil.com") {return "PROXY iceadmin.ice.intil.com:811";}
}

