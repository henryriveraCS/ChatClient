# ChatClient
This is a VERY messy attempt at hardcoding a makeshift chat client. It has a few... "features" but I'll work on it as I improve my regular expression understanding!

In order to get this piece of art working you'll have to have a local PostgreSQL server running and have two tables running within it.
One would have to be named "users" and the other "history".

Users hold the username and password of each respective user.
History holds all the information of an entered message at any given time alongside the user that sent it.

At the moment there is no method to create the table from the UI/Logic part however I will be implementing it as soon as I can.

Some bugs I've found are:
  - Messages longer than one word or with punctuation (i.e : !@#$%^&*,) will not display properly or at all.
  - If there exist no history for the chat in any new day (no one has pushed a message since the day started) then the program doesn't handle the problem efficiently.
  - No way to automatically create new tables from the UI.
  - Half the programs broken.
 
 
I will be working on this throughout the winter of 2019 so bare with me and feel free to comment/commit changes!
