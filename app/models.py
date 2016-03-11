from py2neo import Graph, Node, Relationship, authenticate
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

#url = os.environ.get('http://emboRecTest:TIlvepIFyx5GEyWwsA2l@emborectest.sb04.stations.graphenedb.com:24789', 'http://localhost:7474')
#username = os.environ.get('NEO4J_USERNAME')
#password = os.environ.get('NEO4J_PASSWORD')

#if username and password:
    #authenticate(url.strip('http://'), username, password)

#graph = Graph(url + '/db/data/')
graph = Graph("http://emboRecTest:TIlvepIFyx5GEyWwsA2l@emborectest.sb04.stations.graphenedb.com:24789/db/data/")
class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def register(self, password):
        if not self.find():
            user = Node("User", username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, tags, text):
        user = self.find()
        post = Node(
            "Post",
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date(),

        )
        rel = Relationship(user, "PUBLISHED", post)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for t in set(tags):
            tag = graph.merge_one("Tag", "name", t)
            rel = Relationship(tag, "TAGGED", post)
            graph.create(rel)

    def add_node(self, stateCreateR, stateCreateO, roleCreate, eventCreate, activityCreate, objectCreate):
        user = self.find()

        event = Node(
            "EVENT",
            id=str(uuid.uuid4()),
            description=eventCreate,
            timestamp=timestamp(),
            date=date(),
        )
        event=graph.merge_one("EVENT","description",eventCreate)
        rel = Relationship(user, "CREATED", event)
        graph.create(rel)

        stateR = Node(
            "STATE",
            id=str(uuid.uuid4()),
            description=stateCreateR,
            timestamp=timestamp(),
            date=date(),
        )
        stateR=graph.merge_one("STATE","description",stateCreateR)
        rel = Relationship(user, "CREATED", stateR)
        graph.create(rel)

        stateO = Node(
            "STATE",
            id=str(uuid.uuid4()),
            description=stateCreateO,
            timestamp=timestamp(),
            date=date(),
        )
        stateO=graph.merge_one("STATE","description",stateCreateO)
        rel = Relationship(user, "CREATED", stateO)
        graph.create(rel)

        role = Node(
            "ROLE",
            id=str(uuid.uuid4()),
            description=roleCreate,
            timestamp=timestamp(),
            date=date(),
        )
        role=graph.merge_one("ROLE","description",roleCreate)
        rel = Relationship(user, "CREATED", role)
        graph.create(rel)

        activity = Node(
            "ACTIVITY",
            id=str(uuid.uuid4()),
            description=activityCreate,
            timestamp=timestamp(),
            date=date(),
        )
        activity=graph.merge_one("ACTIVITY","description",activityCreate)
        rel = Relationship(user, "CREATED", activity)
        graph.create(rel)

        object = Node(
            "OBJECT",
            id=str(uuid.uuid4()),
            description=objectCreate,
            timestamp=timestamp(),
            date=date(),
        )
        object=graph.merge_one("OBJECT","description",objectCreate)
        rel = Relationship(user, "CREATED", object)
        graph.create(rel)

        rel2=Relationship(activity, "TEMPORALPARTOF", event)
        graph.create(rel2)
        rel2=Relationship(activity, "TEMPORALPARTOF", stateR)
        graph.create(rel2)
        rel2=Relationship(activity, "TEMPORALPARTOF", stateO)
        graph.create(rel2)
        rel2=Relationship(activity, "TEMPORALPARTOF", role)
        graph.create(rel2)
        rel2=Relationship(activity, "TEMPORALPARTOF", object)
        graph.create(rel2)

        rel3=Relationship(event, "CREATES", stateR)
        graph.create(rel3)
        rel3=Relationship(event, "CREATES", stateO)
        graph.create(rel3)

        rel4=Relationship(stateR, "TEMPORALPARTOF", role)
        graph.create(rel4)
        rel4=Relationship(stateO, "TEMPORALPARTOF", object)
        graph.create(rel4)

    def like_post(self, post_id):
        user = self.find()
        post = graph.find_one("Post", "id", post_id)
        graph.create_unique(Relationship(user, "LIKED", post))

    def get_recent_posts(self):
        query = """
        MATCH (user:User)-[:CREATED]->(n)
        WHERE user.username = {username}
        RETURN user.username AS username, n
        """

        return graph.cypher.execute(query, username=self.username)

    def get_statesR(self, stateR):
        user = self.find()
        query = """
        MATCH ((p {description:"%s"})-[:TEMPORALPARTOF]-> (a)) RETURN  a
        """ %stateR
        query2 = """
        MATCH ((p {description:"%s"})<-[:CREATES]- (a)) RETURN  a
        """ %stateR
        return graph.cypher.execute(query, username=self.username), graph.cypher.execute(query2, username=self.username)

    def get_statesO(self, stateO):
        user = self.find()
        query = """
        MATCH ((p {description:"%s"})-[:TEMPORALPARTOF]-> (a)) RETURN  a
        """ %stateO
        query2 = """
        MATCH ((p {description:"%s"})<-[:CREATES]- (a)) RETURN  a
        """ %stateO
        return graph.cypher.execute(query, username=self.username), graph.cypher.execute(query2, username=self.username)

    def get_events(self, event):
        user = self.find()
        query = """
        MATCH ((p {description:"%s"})-[:CREATES]-> (a)) RETURN  a
        """ %event
        query2 = """
        MATCH ((p {description:"%s"})-[:TEMPORALPARTOF]-> (a)) RETURN  a
        """ %event
        return graph.cypher.execute(query, username=self.username), graph.cypher.execute(query2, username=self.username)

    def get_roles(self, role):
        user = self.find()
        query = """
        MATCH ((p {description:"%s"})-[:TEMPORALPARTOF]-> (a)) RETURN  a
        """ %role
        query2 = """
        MATCH ((p {description:"%s"})<-[:TEMPORALPARTOF]- (a)) RETURN  a
        """ %role
        return graph.cypher.execute(query, username=self.username), graph.cypher.execute(query2, username=self.username)

    def get_objects(self, object):
        user = self.find()
        query = """
        MATCH ((p {description:"%s"})<-[:TEMPORALPARTOF]- (a)) RETURN  a
        """ %object
        query2 = """
        MATCH ((p {description:"%s"})-[:TEMPORALPARTOF]-> (a)) RETURN  a
        """ %object
        return graph.cypher.execute(query, username=self.username), graph.cypher.execute(query2, username=self.username)

    def get_activities(self, activity):
        user = self.find()
        query = """
        MATCH ((a)-[:TEMPORALPARTOF]->(p {description:"%s"})) RETURN  a
        """ %activity
        return graph.cypher.execute(query, username=self.username)

    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags, COUNT(DISTINCT tag) AS len
        ORDER BY len DESC LIMIT 3
        RETURN they.username AS similar_user, tags
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
        MATCH (they:User)
        MATCH (you:User {username: {username} })
        WHERE they<>you
        OPTIONAL MATCH (they)-[:CREATED]->(n)<-[:CREATED]-(you)
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

def get_todays_recent_posts():
    query = """
    MATCH (user:User)-[:CREATED]->(activity:ACTIVITY)
    WHERE activity.date = {today}
    RETURN user.username AS username, activity
    ORDER BY activity.timestamp DESC LIMIT 5
    """

    return graph.cypher.execute(query, today=date())

def fill_states():
        query = """
        MATCH (n:STATE) RETURN n.description
        """
        return graph.cypher.execute(query)

def fill_roles():
        query = """
        MATCH (n:ROLE) RETURN n.description
        """
        return graph.cypher.execute(query)

def fill_events():
        query = """
        MATCH (n:EVENT) RETURN n.description
        """
        return graph.cypher.execute(query)

def fill_activities():
        query = """
        MATCH (n:ACTIVITY) RETURN n.description
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