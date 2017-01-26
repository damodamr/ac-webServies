from py2neo import Graph, Node, Relationship
graph = Graph()

def createGraph(verb , subject, object, pbroles, ann0, ann1):
    print "creation  " + str(ann0),str(ann1)
    verbNode = Node("Action", description=verb + " Action")
    role0 = "unknown"
    role1 = "unknown"
    #if not ann0: ann0 = "unknown"
    #if not ann1: ann1 = "unknown"
    if not pbroles:
        pbroles = "unknown"
    else:
        role0 = pbroles[0]
        role1 = pbroles[1]

    if (subject != 0):
        subjectNode = Node ("Subject", description = str(subject), linkeddata = str(ann0))
        #action = graph.merge_one("Action", "description", pbverb + "Action")
        agentRelation = (verbNode, role0, subjectNode)
        graph.create(agentRelation)

    if (object != 0):
        objectNode = Node("Object", description=str(object), linkeddata = str(ann1))
        #action = graph.merge_one("Action", "description", pbverb + "Action")
        objectRelation = (verbNode, role1, objectNode)
        graph.create(objectRelation)