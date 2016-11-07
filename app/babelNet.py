import urllib2
import urllib
import json
import gzip

from StringIO import StringIO

service_url = 'https://babelnet.io/v4/getSenses'

word = 'London'
lang = 'EN'
key  = 'd511cd60-dd10-4130-a56b-0a9fe6e0b0d4'

params = {
	'word' : word,
	'lang' : lang,
	'key'  : key
}

url = service_url + '?' + urllib.urlencode(params)
request = urllib2.Request(url)
request.add_header('Accept-encoding', 'gzip')
response = urllib2.urlopen(request)

if response.info().get('Content-Encoding') == 'gzip':
	buf = StringIO( response.read())
	f = gzip.GzipFile(fileobj=buf)
	data = json.loads(f.read())

	# retrieving BabelSense data
	for result in data:
		lemma = result.get('lemma')
		language = result.get('language')
		source = result.get('source')
		print language.encode('utf-8') \
			+"\t"+ str(lemma.encode('utf-8')) \
            +"\t" + str(lemma.encode('utf-8')) \
            +"\t"+ str(source.encode('utf-8'))