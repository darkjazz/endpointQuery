import urllib, httplib2, os, sys

if sys.version_info.major == 3:
	import urllib.parse

QUERY_BASE_DIR = "./"


class SparqlHttpConnection:
	def __init__(self, uri, port, qrydir):
		self.uri = uri
		if port != 80:
			self.uri += ":" + str(port)
		self.dir = qrydir

	def executeQuery(self, queryname, params=None, dataset=None, queryType='query'):
		if queryname == None: 
			return {"error": "no queryname provided"}
		
		query = Query(queryname, params, self.dir)

		if dataset != None and dataset != "":
			dataset = '/' + dataset + '/' + queryType
		else:
			dataset = '/' + queryType

		response, content = httplib2.Http().request(self.uri+dataset+'?'+query.encoded() + '&output=json')

		if response.status == 200:
			return content
		else:
			return response

	def listAvailableQueries(self):
		for filename in os.listdir(QUERY_BASE_DIR + self.dir):
			print(filename)

#	def writeToCache(self, queryname, params, dataset, data):
#		if self.cache.key
#			self.cache[queryname].append

class Query:
	def __init__(self, name, params=None, dir=""):
		self.name = name
		self.params = params
		if dir != "":
			self.dir = dir + "/"
		else:
			self.dir = ""
		self.load()
		self.addParameters()

	def load(self):
		tmp = open(QUERY_BASE_DIR + self.dir + self.name + '.rq', 'r')
		self.value = tmp.read()
		tmp.close()

	def addParameters(self):
		if self.params != None:
			for key, val in self.params.items():
				self.value = self.value.replace(key, str(val))

	def encoded(self):
		if sys.version_info.major == 3:
			return urllib.parse.urlencode({"query": self.value})
		else:
			return urllib.urlencode({"query": self.value})

	def encodedUpdate(self):
		if sys.version_info.major == 3:
			return urllib.parse.urlencode({"update": self.value})
		else:
			return urllib.urlencode({"update": self.value})