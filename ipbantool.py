import os, urllib2
ips = os.popen('cut -d" " -f1 /var/log/nginx/access.log | sort | uniq').read()
ips = ips.split("\n")[:-1]

key = "your-key"

for ip in ips:
    url = "https://www.abuseipdb.com/check/"+ip+"/json?key="+key+"&days=20000";
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                  'Accept-Encoding': 'none',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Connection': 'keep-alive'}

    req = urllib2.Request(url, headers=hdr)

    try:
            page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
            print e.fp.read()

    content = page.read()

    if (content != "[]"):
        os.system("fail2ban-client set nginx-http-auth banip "+ip);
        os.system("fail2ban-client set sshd-ddos banip "+ip);
        os.system("fail2ban-client set sshd banip "+ip);


