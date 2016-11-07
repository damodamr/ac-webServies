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
        user = graph.find_one("User", "username", self.username)
        return user

    def register(self, password, group, age):
        if not self.find():
            user = Node("User", username=self.username, password=bcrypt.encrypt(password))
            groupNode = Node("Group",age = age, group = group )
            graph.create(user)
            graph.create(groupNode)
            rel = Relationship(user, "isA", groupNode)
            graph.create(rel)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False


    def like_post(self, post_id):
        user = self.find()
        post = graph.find_one("Post", "id", post_id)
        graph.create_unique(Relationship(user, "LIKED", post))

    def get_recent_posts(self):
        query = """
        MATCH (user:User)-[:searchedFor]->(n)
        WHERE user.username = {username}
        RETURN user.username AS username, n
        """

        return graph.cypher.execute(query, username=self.username)

    def get_statesR(self, stateR):
        user = self.find()

        search = Node(
            "Search",
            id=str(uuid.uuid4()),
            description=stateR,
            timestamp=timestamp(),
            date=date(),
        )
        search=graph.merge_one("SearchFreebase","description",stateR)
        rel = Relationship(user, "searchedFor", search)
        graph.create(rel)

        test, test2 = queryService.query(stateR)
        return test

    def get_statesO(self, stateO):
        user = self.find()

        search = Node(
            "Search",
            id=str(uuid.uuid4()),
            description=stateO,
            timestamp=timestamp(),
            date=date(),
        )
        search=graph.merge_one("SearchJamendo","description",stateO)
        rel = Relationship(user, "searchedFor", search)
        graph.create(rel)

        test, test2 = queryService.query(stateO)
        return test2

    def get_roles(self, role):
        user = self.find()
        test, test2 = queryService.query(role)
        return test, test2


    def get_events(self, event):
        user = self.find()
        test, test2, test3 = queryService.complexQuery(event)
        return test, test2, test3


    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (you:User)-[:searchedFor]->(n)
              (they:User)-[:searchedFor]->(n)
        WHERE you.username = {username} AND you <> they
        RETURN they.username AS similar_user
        """

        return graph.cypher.execute(query, username=self.username)

    def get_other_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (user:User)
        WHERE user.username <> {username}
        RETURN user.username AS similar_user
        """

        return graph.cypher.execute(query, username=self.username)

    def get_other_users2(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (they:User)-[:searchedFor]->(n)<-[:searchedFor]-(you:User {username: {username} })
        WHERE they<>you
        RETURN they.username AS users, COUNT(n) AS entities
        ORDER BY entities DESC
        """
        return graph.cypher.execute(query, username=self.username)


    def get_commonality_of_user(self, other):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = """
        MATCH (they:User {username: {they} })
        MATCH (you:User {username: {you} })
        OPTIONAL MATCH (they)-[:CREATED]->(n)<-[:CREATED]-(you)
        RETURN COUNT(n) AS entities, n as entity, they as user
        """

        return graph.cypher.execute(query, they=other.username, you=self.username)

    def add_node(self, stateCreateR, stateCreateO, file, newSound):
        print(stateCreateR, stateCreateO, file, newSound)
        g = readOntology.writeRDF(self.username, stateCreateR, stateCreateO, file, newSound)
        return g

def get_todays_recent_posts():
    query = """
    MATCH (user:User)-[:searchedFor]->(n)
    WHERE n.date = {today}
    RETURN user.username AS username, n
    ORDER BY n.timestamp DESC LIMIT 5
    """

    return graph.cypher.execute(query, today=date())

#def fill_states():

        #moSub, moPred, moObj = loadOntologyEntities.query()

        #return moSub

#def fill_roles():

        #moSub, moPred, moObj = loadOntologyEntities.query()

        #return moPred

#def fill_events():

        #moSub, moPred, moObj = loadOntologyEntities.query()

        #return moObj


def fill_activities():
    query = """
            MATCH (user:User)-[:searchedFor]->(n)
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


