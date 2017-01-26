from py2neo import Graph, Node, Relationship, authenticate


graph = Graph('http://localhost:7474/db/data/')

ThingNode = Node("Thing", description= "Thing")

#--------------AGENT ACTION TOP-----------------------------------------------------------------------------------------

AgentNode = Node("Agent", description= "Agent")
relAgent = Relationship(AgentNode, "rdf:type", ThingNode)

AgentNodeOMA = Node("Agent", description= "OnlineMusicAccount")
relAgentOMA = Relationship(AgentNodeOMA, "rdf:type", AgentNode)

ActionNode = Node("Action", description= "Action")
relAction = Relationship(ActionNode, "rdf:type", ThingNode)

ActionNodeIP = Node("Action", description= "IPAction")
ActionNodeProd = Node("Action", description= "ProductionAction")
ActionNodeWebSer = Node("Action", description= "WebServiceAction")

relActionIP = Relationship(ActionNodeIP, "rdf:type", ActionNode)
relActionProd = Relationship(ActionNodeProd, "rdf:type", ActionNode)
relActionWebSer = Relationship(ActionNodeWebSer, "rdf:type", ActionNode)

graph.create(ThingNode, AgentNode, ActionNode , ActionNodeIP, ActionNodeProd, ActionNodeWebSer, AgentNodeOMA)
graph.create(relAgent, relAction, relActionIP,relActionProd, relActionWebSer, relAgentOMA)

#-------------ACTIONS---------------------------------------------------------------------------------------------------

ActionNodeTagging = Node("Action", description= "muto:Tagging")
ActionNodeRating = Node("Action", description= "schema:Rating")
ActionNodeSearch = Node("Action", description= "SearchAction")
ActionNodeUpload = Node("Action", description= "UploadAction")
ActionNodeComment = Node("Action", description= "WriteCommentAction")

relActionTagging = Relationship(ActionNodeTagging, "rdf:type", ActionNodeWebSer)
relActionRating = Relationship(ActionNodeRating, "rdf:type", ActionNodeWebSer)
relActionSearch = Relationship(ActionNodeSearch, "rdf:type", ActionNodeWebSer)
relActionUpload = Relationship(ActionNodeUpload, "rdf:type", ActionNodeWebSer)
relActionComment = Relationship(ActionNodeComment, "rdf:type", ActionNodeWebSer)

graph.create(ActionNodeTagging, ActionNodeRating, ActionNodeSearch, ActionNodeUpload, ActionNodeComment)
graph.create(relActionTagging, relActionRating, relActionSearch, relActionUpload, relActionComment)


#-------------WEB RESOURCE----------------------------------------------------------------------------------------------

WebResourceNode = Node("WebResource", description= "WebResource")
graph.create(WebResourceNode)
relWebResource = Relationship(WebResourceNode, "rdf:type", ThingNode)

WebResourceNodeComment = Node("WebResource", description= "Comment")
WebResourceNodeCollection = Node("WebResource", description= "edm:Collection")
WebResourceNodePost = Node("WebResource", description= "ForumPost")
WebResourceNodeAudioFile = Node("WebResource", description= "mo:AudioFile")
WebResourceNodeTag = Node("WebResource", description= "muto:Tag")

relWebResourceComment = Relationship(WebResourceNodeComment, "rdf:type", WebResourceNode)
relWebResourceCollection = Relationship(WebResourceNodeCollection, "rdf:type", WebResourceNode)
relWebResourcePost = Relationship(WebResourceNodePost, "rdf:type", WebResourceNode)
relWebResourceAudioFile = Relationship(WebResourceNodeAudioFile, "rdf:type", WebResourceNode)
relWebResourceTag = Relationship(WebResourceNodeTag, "rdf:type", WebResourceNode)

graph.create(WebResourceNodeComment, WebResourceNodeCollection, WebResourceNodePost, WebResourceNodeAudioFile, WebResourceNodeTag)
graph.create(relWebResourceComment, relWebResourceCollection, relWebResourcePost, relWebResourceAudioFile, relWebResourceTag, relWebResource)