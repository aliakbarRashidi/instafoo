'''
https://medium.com/labcodes/graph-databases-talking-about-your-data-relationships-with-python-b438c689dc89

'''

from py2neo import Graph, Node, Relationship

g = Graph("http://neo4j:test@localhost:7474/TestDatabase/data/")

def create_node(user):
    user_name = user['user_name']
    user_id = user['user_id']
    tx = g.begin()
    user = Node("User", user_name=user_name, user_id=user_id)
    tx.create(user)
    tx.commit()
    return user

def create_relationship(user1,user2,relationship):
    assert relationship in ["FOLLOWS","FOLLOWED_BY"]
    tx = g.begin()
    rel = Relationship(user1, relationship, user2)
    tx.create(rel)
    tx.commit()

'''
selector = NodeSelector(g)
john = selector.select("User", name="John").first()

john_friends = g.match(start_node=john, rel_type="FRIENDS_WITH")

for friend_relationship in john_friends:
    friend = friend_relationship.end_node()
    print(friend)
'''