from neo4j import GraphDatabase

#neo4j connection credentials
uri = "neo4j+s://98d6804e.databases.neo4j.io"
user = "RSiliveru"
password = "Bamberguni123@"

#create the driver 
driver= GraphDatabase.driver(uri, auth=(user,password))

# Test connection with query
def test_connection(c):
    result = c.run("RETURN 'Connection Successful!' AS message")
    for record in result:
        print(record["message"])


#event node creation 
# def create_event(tx, eventid, date, topic ):
#     tx.run("""
#         CREATE (:Event {eventid: null, date: null, topic: null})
#     """)


#attendee node creation
# def create_attendee(tx, attendee_id,name):
#     tx.run("""
#     CREATE (:Attendee {attendee_id:null , name:null})
#     """)

#Host node creation
# def create_host(tx, host_id,name):
#     tx.run("""
#     CREATE (:Host {host_id:null, name:null})
#     """)

#create Conversation node
# def create_conversation(tx,topic,note,date,event):
#     tx.run("""
#     CREATE (:Conversation{topic:null, note:null, date:null, event:null})
#     """)




with driver.session() as session:
    session.read_transaction(test_connection)
    #session.write_transaction(create_event,  None, None, None)
    #session.write_transaction(create_attendee, None, None)
    #session.write_transaction(create_host,None, None)
    #session.write_transaction(create_conversation, None, None, None,None)



driver.close()