#Logic to be used between UI and server.
#ALL FUNCTIONS HANDLING DATA IS PASSED THROUGH THESE FUNCTIONS
import datetime
import psycopg2
import re

#connecting to the server.
conn = psycopg2.connect("dbname=chat user=postgres")
cur = conn.cursor()

#function for checking if parameters passed are valid.
#should return True or False to ClientUIX.py for determing next action.
def LoginCheck(username, password):
    #converting parameters into string and executing PSQL
    cur.execute("""
        SELECT username, password FROM users
        WHERE username = %s AND password = %s;
        """, (username, password))

    #checking the returned value of table and then using an
    # if statement to check if passed parameters matches with returned values.
    row = cur.fetchone()
    if row == (username, password):
        #return true to open chatroom
        #return username to have a display name to attach to messages
        return True, username
    else:
        return False

#function for signing in a new username/password into db
def Signup(username, password, password2):
    if password != password2:
        return False
    else:
        userCheck = cur.execute("""
                            SELECT username from users
                            WHERE username = %s
                            """, (username,))
        userVerify = cur.fetchone()
        #checking if the username exist
        if userVerify is None:
            #code for comitting new username and password to db
            cur.execute("""
                        INSERT INTO users (username, password)
                        VALUES (%s, %s)
                        """, (username, password))
            conn.commit()
            return True
        else:
            return False

#function for passing a message into the database
def ChatInsert(username, message):
    sent = datetime.datetime.now()

    #insert the parameters into the history table
    #in the following order : username, message, sent
    cur.execute("""
        INSERT INTO history (username, message, sent)
        VALUES (%s, %s, %s)
        """,(username, message, sent))

    conn.commit()

#function for return the string of the chat history
def ChatUpdate():
    #getting the most recent message today and formatting it for execute()
    currentData = str(datetime.datetime.now().date())

    message = cur.execute("""
        SELECT username, message, DATE(sent) FROM history
        WHERE username = username
        AND message = message
        AND DATE(sent) = %s
        ORDER BY sent DESC
        LIMIT 1;
    """, (currentData, ))

    #converting the returned username, message and date into a displayable list to return
    unformattedData = str(cur.fetchone())

    patternUser = r"('\w+')"
    formattedUser = re.search(patternUser, unformattedData)
    if formattedUser == None:
        cleanUser = "Bot" # if no string is returned then make a fake user to display msg
    else:
        cleanUser = formattedUser.group(0).replace("'", "")

    patternMessage = r"('\w+'), (\w)"
    formattedMessage = re.search(patternMessage, unformattedData)
    if formattedMessage == None:
        cleanMessage = "             "
        print("if statement went off: ",cleanMessage)
    else:
        cleanMessage = str(formattedMessage.group(1).replace("'", ""))


    patternDate = r"((\w+), (\w+), (\w+))"
    formattedDate = re.search(patternDate, unformattedData)
    cleanDate = formattedDate.group(0).replace(",", "/").replace(" ", "")

    #the format of the message [date] username: message
    cleanedResponsed = ('[' + cleanDate + '] ' + cleanUser + ': ' + cleanMessage)
    return cleanedResponsed
