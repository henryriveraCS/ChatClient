# UI for the chat using Tkinter
import tkinter as tk
from time import sleep
from tkinter import scrolledtext as sc

from ClientLogic import LoginCheck, ChatInsert, ChatUpdate, Signup

#global variables for returning a string/username
userLogin = None
chatlog = ChatUpdate()

class LoginScreen(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def SignButton(self):
        #destroying window to create a new one
        self.destroy()

        #opening new window for signing up
        app3 = SigningUp()
        app3.master.title('Sign Up Page')
        app3.master.geometry('400x250')
        app3.master.mainloop()

    #function to check if the passed information is valid
    def LoginButton(self):
        #getting the values in entry
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        #performing logic to check if username/password are valid and returning boolean
        status = LoginCheck(username, password)
        if status == (True, username):
            #setting global to username for display and then destroying login window
            global userLogin
            userLogin = username
            self.destroy()

            #opening chat room
            app2 = ChatRoom()
            app2.master.title('Chatroom')
            app2.master.geometry('350x250')
            app2.mainloop()

        else:
            #label warning user of invalid login
            self.InvalidLabel = tk.Label(self,
                                         text='Invalid Login! Try again.',
                                         fg = 'red')

            self.InvalidLabel.grid(row=2, column=1)


    def createWidgets(self):
        #username and password label/entries
        self.usernameLabel = tk.Label(self, text='Username: ')
        self.usernameEntry = tk.Entry(self)

        self.passwordLabel = tk.Label(self, text='Password: ')
        self.passwordEntry = tk.Entry(self, show='*')

        #placing everything in the LoginScreen Frame
        self.usernameLabel.grid(row=0, column=0)
        self.usernameEntry.grid(row=0, column=1)

        self.passwordLabel.grid(row=1, column=0)
        self.passwordEntry.grid(row=1, column=1)


        #creating variables to pass on the inputted
        #data from Entry into LoginCheck()

        #login and quit buttons
        self.logButton = tk.Button(self,
                                   text='Login',
                                   command=lambda: self.LoginButton(),
                                   highlightbackground='green')

        self.quitButton = tk.Button(self,
                                    text='Quit',
                                    command=self.quit,
                                    highlightbackground='red')

        self.SignUpButton = tk.Button(self,
                                      text='Sign Up',
                                      command=lambda: self.SignButton(),
                                      highlightbackground='yellow')

        self.logButton.grid(row=0, column=2,
            stick=tk.E)
        self.SignUpButton.grid(row=0, column=3)
        self.quitButton.grid(row=1, column=2,
            stick=tk.E)

class SigningUp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def ToLogin(self):
        self.destroy()

        app4 =  LoginScreen()
        app4.master.title('Login')
        app4.master.geometry('400x250')
        app4.mainloop()

    def SignButton(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        password1 = self.password1Entry.get()
        result = Signup(username, password, password1)

        if result == True:
            self.passedInfo = tk.Label(self, text='Successfully created user!')
            self.passedInfo.grid(row=4, column=1)
        else:
            self.failedInfo = tk.Label(self, text='Something went wrong.')
            self.failedInfo.grid(row=4, column=1)

    def createWidgets(self):
        self.Logo = tk.Label(self, text='Welcome!')
        self.usernameLabel = tk.Label(self,text='Username: ')
        self.passwordLabel = tk.Label(self, text='Password: ')
        self.password1Label = tk.Label(self, text='Re-enter Password: ')

        self.usernameEntry = tk.Entry(self)
        self.passwordEntry = tk.Entry(self, show='*')
        self.password1Entry = tk.Entry(self, show='*')

        self.submitButton = tk.Button(self,
                                      command=lambda: self.SignButton(),
                                      text='Sign up',
                                      fg='green')
        self.toLoginButton = tk.Button(self,
                                       command= lambda: self.ToLogin(),
                                       text='To Login',
                                       fg='green')

        self.Logo.grid(row=0, column=1)
        self.usernameLabel.grid(row=1, column=0)
        self.passwordLabel.grid(row=2, column=0)
        self.password1Entry.grid(row=3, column=0)
        self.usernameEntry.grid(row=1, column=1)
        self.passwordEntry.grid(row=2, column=1)
        self.password1Entry.grid(row=3, column=1)
        self.submitButton.grid(row=2, column=2)
        self.toLoginButton.grid(row=3, column=2)

class ChatRoom(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def SendButton(self):
        #getting message from message entry to send
        message = self.messageEntry.get()

        #calling function to insert username, message and timestamp into db
        ChatInsert(userLogin, message)

    def Refresh(self):
        chatlog = ChatUpdate()
        #destroy the current message box and replace it immediately to update it
        self.history.destroy()
        self.history = tk.Message(self,
                                  text=chatlog,
                                  bg = 'black',
                                  fg = 'white',
                                  width = 1000)
        self.history['font'] = ('consolas', '12')
        self.history.grid(row=1, column=0)

    def createWidgets(self):
        #variable which will change the value of text inside message
        chatlog = ChatUpdate()

        #Chat history
        self.history = tk.Message(self,
                                  text=chatlog,
                                  bg = 'black',
                                  fg = 'white',
                                  width = 1000)
        self.history['font'] = ('consolas', '12')
        self.history.grid(row=1, column=0)

        #message entry, display name and "send" button
        self.messageEntry = tk.Entry(self)
        self.displayName = tk.Label(self,
                                    text='Your logged in as: %s' % userLogin)
        self.sendButton = tk.Button(self,
                                    command = lambda: self.SendButton(),
                                    text='Send',
                                    fg='blue')
        self.refreshButton = tk.Button(self,
                                       command = lambda: self.Refresh(),
                                       text='Refresh',
                                       fg='green')


        self.messageEntry.grid(row=2, column=0)
        self.displayName.grid(row=0, column=0)
        self.sendButton.grid(row=2, column=1)
        self.refreshButton.grid(row=3, column=1)

app = LoginScreen()
app.master.title('Login')
app.master.geometry('400x250')
app.mainloop()
