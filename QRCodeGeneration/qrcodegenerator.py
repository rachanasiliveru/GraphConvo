import qrcode
import os
import json
from neo4j import GraphDatabase 

#connection details
uri = "neo4j+s://98d6804e.databases.neo4j.io"
user = "RSiliveru"
password = "Bamberguni123@"

driver = GraphDatabase.driver(uri,auth=(user,password))

#QR in directory 
outputdir="GeneratedQRCodes"
os.makedirs(outputdir, exist_ok=True)

def get_attendees(tx):
    query= """ MATCH (a:Attendee) return a.attendeeid as ID, a.name as Name """
    return tx.run(query).data()


def get_hosts(tx):
    query= """ MATCH (h:Host) return h.hostid as Host_ID, h.name as Host_Name"""
    return tx.run(query).data()

def generatedQRcodes():
    with driver.session() as session:


        attendees = session.read_transaction(get_attendees)
        for attendee in attendees:
            data = {
                "attendeeid": attendee["ID"],
                "name": attendee["Name"]
            }


            qr_data = json.dumps(data)
            qr = qrcode.make(qr_data)

            # Saving QR image
            clean_id = attendee["ID"].strip()  # Remove any leading/trailing spaces or newlines
            filename = os.path.join(outputdir, f"Attendee_{clean_id}.png")
            qr.save(filename)
            print(f"QR code saved: {filename}")


            #QR gen for Host
        hosts=session.read_transaction(get_hosts)
        for host in hosts:
            data = {
                "hostid":host["Host_ID"],
                "name":host["Host_Name"]
            }

            qr_data=json.dumps(data)
            qr=qrcode.make(qr_data)

             # Saving QR image
            clean_id = host["Host_ID"].strip()  # Remove any leading/trailing spaces or newlines
            filename = os.path.join(outputdir, f"Host_{clean_id}.png")
            qr.save(filename)
            print(f"QR code saved: {filename}")




# Run the function
generatedQRcodes()
driver.close()














