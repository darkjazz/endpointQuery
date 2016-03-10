import httplib, urllib, httplib2, os
from urllib import quote

QUERY_BASE_DIR = "/usr/local/etc/sparql/"

class SparqlEndpoint:
	def __init__(self, uri, port=80, dir=""):
		self.uri = uri
		self.port = port
		if dir != "":
			self.dir = dir + "/"
		self.cache = {}

	def executeQuery(self, queryname, params=None, dataset=None):
		if queryname == None: 
			return {"error": "no queryname provided"}
		
		query = Query(queryname, params, self.dir)

		if dataset != None and dataset != "":
			dataset =  "/" + dataset + "/query"
		else:
			dataset = "/query"

		self.headers = {
			"Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/sparql-results+json"
        }
        
		self.connection = httplib.HTTPConnection(self.uri, self.port)
		self.connection.request("POST", dataset, query.encoded(), self.headers)
		self.response = self.connection.getresponse()
		self.data = self.response.read()
		self.connection.close()
		return self.data

	def update(self, queryname, params=None, dataset=None):
		if queryname == None: 
			return {"error": "no queryname provided"}
		
		query = Query(queryname, params, self.dir)

		if dataset != None and dataset != "":
			dataset =  "/" + dataset + "/update"
		else:
			dataset = "/update"		

		self.headers = {
			"Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/sparql-results+json"
        }

		self.connection = httplib.HTTPConnection(self.uri, self.port)
		self.connection.request("POST", dataset, query.encodedUpdate(), self.headers)
		self.response = self.connection.getresponse()
		self.data = self.response.read()
		self.connection.close()
		return self.data

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
			print filename

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
			for key, val in self.params.iteritems():
				self.value = self.value.replace(key, str(val))

	def encoded(self):
		return urllib.urlencode({"query": self.value})

	def encodedUpdate(self):
		return urllib.urlencode({"update": self.value})
