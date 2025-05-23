import streamlit as st
import cv2
import json
from neo4j import GraphDatabase

# Neo4j connection
driver = GraphDatabase.driver("URI", auth=("user", "pwd"))

def save_conversation(tx, hostid, attendeeid, topic):
    result = tx.run("""
    MATCH (h:Host {hostid: $hostid}), (a:Attendee {attendeeid: $attendeeid})
    MERGE (h)-[r:HAD_CONVERSATION {topic: $topic}]->(a)
    RETURN h.hostid AS HostID, a.attendeeid AS AttendeeID, r.topic AS Topic
    """, hostid=hostid, attendeeid=attendeeid, topic=topic)
    return result.single()

# Streamlit UI
st.title("Graph Convo Tracker")

hostid = st.text_input("Enter Host ID")

if st.button("Scan QR"):
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    st.write("Scanning... Press 'Q' in camera window to quit")

    attendeeid = None
    attendee_name = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        cv2.imshow("Scan QR - Press Q to Quit", frame)

        if data:
            decoded = json.loads(data)
            attendeeid = decoded.get("attendeeid")
            attendee_name = decoded.get("name")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if attendeeid:
        st.success(f"Scanned Attendee: {attendee_name} (ID: {attendeeid})")
        topic = st.text_input("Enter conversation topic")

        if st.button("Save to Neo4j") and hostid and topic:
            st.write("Trying to save:", hostid, attendeeid, topic)  # 🔍 Debug line added here
            with driver.session() as session:
                record = session.write_transaction(save_conversation, hostid, attendeeid, topic)
            if record:
                st.success(f"Conversation saved! HostID: {record['HostID']}, AttendeeID: {record['AttendeeID']}, Topic: {record['Topic']}")
            else:
                st.error("Failed to save conversation. Please verify HostID and AttendeeID exist.")
    else:
        st.warning("No QR code detected.")
