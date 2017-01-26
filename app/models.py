from py2neo import Graph, Node, Relationship, authenticate
from passlib.hash import bcrypt
from datetime import datetime
import queryService
import loadOntologyEntities, readOntology
import os
import uuid


#url = os.environ.get('http://localhost:7474')
#username = os.environ.get('NEO4J_USERNAME')
#password = os.environ.get('NEO4J_PASSWORD')

#if username and password:
    #authenticate(url.strip('http://'), username, password)

graph = Graph('http://localhost:7474/db/data/')

#graph = Graph("http://emboRecTest:TIlvepIFyx5GEyWwsA2l@emborectest.sb04.stations.graphenedb.com:24789/db/data/")
class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("OnlineMusicAccount", "username", self.username)
        return user

    def register(self, password, group, age):
        if not self.find():
            user = Node("OnlineMusicAccount", username=self.username, password=bcrypt.encrypt(password))

            graph.create(user)

            OMA = graph.find_one("OnlineMusicAccount", "description", "OnlineMusicAccount" )
            affRel = Relationship(user, "rdf:type", OMA)

            affiliationNode = Node("Affiliation", age=age, affiliation=group)
            graph.create(affiliationNode)
            affRel = Relationship(user, "schema:affiliation", affiliationNode)
            graph.create(affRel)

            nameNode = Node("OnlineMusicAccountName", username=self.username)
            graph.create(nameNode)
            nameRel = Relationship(user, "foaf:name", nameNode)
            graph.create(nameRel)

            dateNode = Node("Date", date=date())
            graph.create(dateNode)
            dateRel = Relationship(user, "dcterms:created", dateNode)
            graph.create(dateRel)

            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False


    #def like_post(self, post_id):
        #user = self.find()
        #post = graph.find_one("Post", "id", post_id)
        #graph.create_unique(Relationship(user, "LIKED", post))

    def get_recent_posts(self):
        query = """
        MATCH ((n)-[:wasAssociatedWith]-> (user:OnlineMusicAccount))
        WHERE user.username = {username}
        RETURN user.username AS username, n
        """
        return graph.cypher.execute(query, username=self.username)

#----------------ACTIONS---FREESOUND------------------------------------------------------------------------------------
    #-----------------SEARCH ACTIONS -----------------------------------------------------------------------------------
    def TextSearch(self, query):
        user = self.find()

        search = Node(
            "Action",
            id=str(uuid.uuid4()),
            timestamp=timestamp(),
            date=date(),
            description="Text Search Freesound",
            provider = "Freesound",
            actionDesc="SearchAction",
            hasInputMessage=query,
            hasMethod="GET",
            hasAddress="URITemplate",
            hasOutputMessage="mo:MusicalBuildingBlock",
            query=query,
        )
        #search=graph.merge_one("TextSearch","query",query)
        rel = Relationship(search, "wasAssociatedWith", user)
        graph.create(rel)

        test, test2 = queryService.query(query)
        return test

    #----------------UPLOAD ACTION -------------------------------------------------------------------------------------


    def UploadFile(self, task, permition, oldFileName, newFileName):
        user = self.find()

        upload = Node(
            "Action",
            id=str(uuid.uuid4()),
            timestamp=timestamp(),
            date=date(),
            description="Upload File Freesound",
            actionDesc="UploadAction",
            hasInputMessage="query",
            hasMethod="POST",
            hasAddress="URITemplate",
            hasOutputMessage="dictionary",
        )
        #search=graph.merge_one("TextSearch","query",query)
        rel = Relationship(upload, "wasAssociatedWith", user)
        graph.create(rel)

        audiofile = Node (
            "mo:AudioFile",
            id=str(uuid.uuid4()),
            timestamp=timestamp(),
            date=date(),
            description="File Freesound",
            duration= " ",
            filesize = " ",
            hasAddress = " ",
            name = newFileName,
        )
        rel = Relationship(audiofile, "wasGeneratedBy", upload)
        graph.create(rel)

        #----------this is Licence trigering action---------------------------------------------------------------------

        createLicenceNodes(task, permition, user, audiofile, upload)

        #------------this action also triggers encoding action----------------------------------------------------------

        encoding = Node(
            "Action",
            id=str(uuid.uuid4()),
            description="Encoding File Freesound",
            actionDesc="EncodingAction",
            hasAudioEncodingFormat = " ",
            sample_rate = " ",
            channels = " ",
            bitrate = " ",
            bitsPerSample = " "
        )

        rel = Relationship(audiofile, "wasGeneratedBy", encoding)
        graph.create(rel)

    #------------TAGGING ACTION-----------------------------------------------------------------------------------------

    def TagFile(self, listOfTags,audiofile):
        user = self.find()

        tagging = Node(
            "Action",
            id=str(uuid.uuid4()),
            timestamp=timestamp(),
            date=date(),
            description="Tag Freesound file",
            actionDesc="muto:Tagging",
            hasCreator = user,
            hasTag = listOfTags,
            note = " ",
            taggedResource = audiofile

        )

        rel = Relationship(tagging, "muto:hasCreator", user)
        graph.create(rel)


#--------------ACTIONS---JAMENDO----------------------------------------------------------------------------------------

    def searchJamendo(self, stateO):
        user = self.find()

        search = Node(
            "Action",
            id=str(uuid.uuid4()),
            timestamp=timestamp(),
            date=date(),
            description="Search Jamendo",
            actionDesc="SearchAction",
            hasInputMessage=stateO,
            hasMethod="GET",
            hasAddress="URITemplate",
            hasOutputMessage="mo:MusicalWork",
            query=stateO,
        )
        #search=graph.merge_one("SearchJamendo","description",stateO)
        rel = Relationship(search, "wasAssociatedWith", user)
        graph.create(rel)

        test, test2 = queryService.query(stateO)
        return test2

#-----------------------------------------------------------------------------------------------------------------------

    def get_roles(self, role):
        user = self.find()
        test, test2 = queryService.query(role)
        return test, test2


    def get_events(self, event):
        user = self.find()
        test, test2 = queryService.complexQuery(event)
        return test, test2


    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (you:OnlineMusicAccount)<-[:wasAssociatedWith]-(n)
              (they:OnlineMusicAccount)<-[:wasAssociatedWith]-(n)
        WHERE you.username = {username} AND you <> they
        RETURN they.username AS similar_user
        """

        return graph.cypher.execute(query, username=self.username)

    def get_other_users(self):
        # Find three users who are most similar to the logged-in user
        # based on the searches
        query = """
        MATCH (user:OnlineMusicAccount)
        WHERE user.username <> {username}
        RETURN user.username AS similar_user
        """

        return graph.cypher.execute(query, username=self.username)

    def get_other_users2(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (they:OnlineMusicAccount)<-[:wasAssociatedWith]-(n)-[:wasAssociatedWith]->(you:OnlineMusicAccount {username: {username} })
        WHERE they<>you
        RETURN they.username AS users, COUNT(n) AS entities
        ORDER BY entities DESC
        """
        return graph.cypher.execute(query, username=self.username)


    #def get_commonality_of_user(self, other):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        #query = """
        #MATCH (they:OnlineMusicAccount {username: {they} })
        #MATCH (you:OnlineMusicAccount {username: {you} })
        #OPTIONAL MATCH (they)-[:CREATED]->(n)<-[:CREATED]-(you)
        #RETURN COUNT(n) AS entities, n as entity, they as user
        #"""

        #return graph.cypher.execute(query, they=other.username, you=self.username)

    def add_node(self, stateCreateR, stateCreateO, file, newSound):
        print(stateCreateR, stateCreateO, file, newSound)
        g = readOntology.writeRDF(self.username, stateCreateR, stateCreateO, file, newSound)
        return g

def get_todays_recent_posts():
    query = """
    MATCH (user:OnlineMusicAccount)<-[:wasAssociatedWith]-(n)
    WHERE n.date = {today}
    RETURN user.username AS username, n
    ORDER BY n.timestamp DESC LIMIT 5
    """

    return graph.cypher.execute(query, today=date())

def fill_activities():
    query = """
            MATCH (user:OnlineMusicAccount)<-[:wasAssociatedWith]-(n)
            RETURN n.description
            """
    return graph.cypher.execute(query)

def fill_objects():
        query = """
        MATCH (n:OBJECT) RETURN n.description
        """
        return graph.cypher.execute(query)

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')

def createLicenceNodes (task, permition, user, audiofile):

    ipActionNode = Node("ac:IPAction", date=" ", description = task)
    graph.create(ipActionNode)

    licenceOwner = Node("mvco:Creator", date=" ")
    graph.create(licenceOwner)

    permitionNode = Node("mvco:Permition", date=" ", description = permition)
    graph.create(permitionNode)

    issuedByRel = Relationship(permitionNode, "mvco:issuedBy", licenceOwner)
    graph.create(issuedByRel)

    permRel = Relationship(permitionNode, "mvco:permitsAction", ipActionNode)
    graph.create(permRel)

    actedOverRel = Relationship(ipActionNode, "mvco:actedOver", audiofile)
    graph.create(actedOverRel)

    actedByRel = Relationship(ipActionNode, "mvco:actedBy", user)
    graph.create(actedByRel)