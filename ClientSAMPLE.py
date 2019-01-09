# Handles the client UI/Logic for communicating with server
import psycopg2
import datetime

#First the logic must be built
conn = psycopg2.connect("dbname=chat user=postgres")
cur = conn.cursor()

# add a method to print out the previous messages in order with all labels as:
"""
    (19:21)Henry: Hey!
    (19:23)Client2: What's up?
    (01:23)OtherUser: Chimiya!
"""
username = str(input("Please select a username!"))
message = str(input("Your message(may not be above 150 characters):"))
sent = datetime.datetime.now()

# adding the data to the table
cur.execute("INSERT INTO history (username, message, sent) VALUES (%s, %s, %s)",
    (username, message, sent))

conn.commit()

cur.execute("SELECT * FROM history;")
cur.fetchone()
print(cur.fetchone())

cur.close()
conn.close()

#UI built around the Logic

#Logic/UI must communicate properly and be modular

#Connect with the server

#request/ listen to the server request
