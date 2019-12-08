import sqlite3
import win32net
import win32netcon
import os

#print the details of the windows user's account(s)
def printUserProfile(dbFile):
	conn =sqlite3.connect(dbFile)
	c = conn.cursor()
	c.execute("SELECT fullname, skypename, emails, phone_mobile, gender, birthday, city, country FROM Accounts;")
	print('[*] -- Priting Accounts --')
	for row in c:
		print('[*] -- Account --')
		print('[+] User: ' + str(row[0]))
		print('[+] Username: ' + str(row[1]))
		print('[+] Email: ' + str(row[2]))
		print('[+] Mobile: ' + str(row[3]))
		print('[+] Gender: ' + str(row[4]))
		print('[+] Birthday: ' + str(row[5]))
		print('[+] City: ' + str(row[6]))
		print('[+] Country: ' + str(row[7]))

#print the contacts of the user
def printContacts(dbFile):
	conn =sqlite3.connect(dbFile)
	c = conn.cursor()
	c.execute("SELECT fullname, skypename, emails, phone_mobile, gender, birthday, city, country FROM Contacts;")
	print('[*] -- Printing Contacts --')
	for row in c:
		print('[*] -- Contact --')
		print('[+] User: ' + str(row[0]))
		print('[+] Username: ' + str(row[1]))
		print('[+] Email: ' + str(row[2]))
		print('[+] Gender: ' + str(row[3]))
		print('[+] Birthday: ' + str(row[4]))
		print('[+] City: ' + str(row[5]))
		print('[+] Country: ' + str(row[6]))

#print the call log
def printCallLog(dbFile):
	conn =sqlite3.connect(dbFile)
	c = conn.cursor()
	c.execute("SELECT datetime(begin_timestamp,'unixepoch'), identity FROM calls, conversations WHERE calls.conv_dbid == conversations.id;")
	print('[*] -- Printing Calls --')
	for row in c:
		print('[+] Time: ' + str(row[0]) + ' | Partner: ' + str(row[1]))

#print any chat logs
def printMessages(dbFile):
	conn =sqlite3.connect(dbFile)
	c = conn.cursor()
	c.execute("SELECT datetime(timestamp,'unixepoch'), dialog_partner, author, body_xml FROM Messages;")
	print('[*] -- Printing Messages --')
	for row in c:
		try:
			if 'partlist' not in str(row[3]):
				if str(row[1]) != str(row[2]):
					msgDirection = 'To' + str(row[1]) + ':'
				else:
					msgDirection = 'From' + str(row[2]) + ':'
				print('Time: ' + str(row[0]) + ' ' + msgDirection + str(row[23]))
		except:
			pass

#list all the windows users to iterate through for skype dbs
#returns a list of _USER_INFO_0 structure
def listUsers():
    user_list = []
    resume_handle = 0
    while True:
    	#Params: server (none is local pc), level (detail level), filter type, pointer for continuing user search
        result = win32net.NetUserEnum(None, 0, win32netcon.FILTER_NORMAL_ACCOUNT, resume_handle)
        user_list += [user['name'] for user in result[0]]
        resume_handle = result[2]
        if not resume_handle:
            break
    return user_list


def main():
	usersToCheck = listUsers()

	print(usersToCheck)

	for account in usersToCheck:
		skypePath = "C:\\Users\\" + account + "\\Appdata\\Roaming\\Skype\\"

		if os.path.exists(skypePath):
			skypeDb = skypePath + "main.db"

			printUserProfile(skypeDb)

			printContacts(skypeDb)

			printCallLog(skypeDb)

			printMessages(skypeDb)
			'''
			#TODO WRITE RESULTS TO SEPARATE FILES #
			# one file per output type #
			
			output = method_call()
			file = open("sample.txt","w")
			file.write(output)
			file.close()'''

if __name__ == "__main__":
	main()