import requests	#needed for soup
import re			#needed for regex
import serial		#needed for arduino
import time
import random		
import sys
from bs4 import BeautifulSoup

def getSite():
	return requests.get("https://www.theguardian.com/us-news/ng-interactive/2020/nov/03/us-election-2020-live-results-donald-trump-joe-biden-who-won-presidential-republican-democrat")


#numbers from last update
seatsDems_old = 0
votesDems_old = 0
seatsReps_old = 0
votesReps_old = 0
updateNr = 0

arduino = serial.Serial('COM3', 9600)		#connect with arduino on port 3
time.sleep(2)							# ! to let arduino establish connection


#START
while 1:
	page = getSite()					#get html

	if page.status_code != 200:
		print("--Error connecting.--")
		time.sleep(120)
		page = getSite()

	else:
		print("--Connected!--")


	soup = BeautifulSoup(page.content, 'html.parser')
	seatsDems = int((soup.find('div', attrs={'class': 'ge-bar__count ge-bar__count--p color--D'})).get_text().replace('\r', '').replace('\n', ''))		#Get Seats Democrats
	votesDems = soup.findAll('div', attrs={'class': 'ge-bar__count--electoral'})[0]														#Get Votes Democrats

	seatsReps = int((soup.find('div', attrs={'class': 'ge-bar__count ge-bar__count--p color--R'})).get_text().replace('\r', '').replace('\n', ''))		#Get Seats Republicans
	votesReps = soup.findAll('div', attrs={'class': 'ge-bar__count--electoral'})[1]														#Get Votes Democrats

	votesDems = int(''.join(filter(str.isdigit, votesDems.get_text())))																#Extract digits from DVotes
	votesReps = int(''.join(filter(str.isdigit, votesReps.get_text())))																#Extract digits from RVotes


	print("Biden: "+str(seatsDems))
	print("Votes: "+str(votesDems))													
	print("Trump: "+str(seatsReps))
	print("Votes: "+str(votesReps))													

	#! arduino/serial can only really read one char at a time
	#b = byte encoded
	if ((seatsDems > seatsDems_old) or (seatsReps > seatsReps_old)):
		arduino.write(b'c')				#seats are changing
		time.sleep(15)

		if (seatsDems >= 270):
			arduino.write(b'B')			#Biden WINS
			time.sleep(15)

		elif (seatsReps >= 270):
			arduino.write(b'T')			#Trump WINS
			time.sleep(15)
		
		#---Seats & Votes---

	if (seatsDems > seatsReps):
		arduino.write(b'1')			#seats Dems are bigger

	elif (seatsReps > seatsDems):
		arduino.write(b'2')			#seats Reps are bigger


	if ((votesDems == votesDems_old) and (votesReps == votesReps_old)):
		arduino.write(b's')				#votes Dems stayed the same	

	if ((votesDems > votesDems_old) and (votesReps > votesReps_old)):
		arduino.write(b'x')				#votes Dems stayed the same	
		
	
	elif(votesDems > votesDems_old):
		arduino.write(b'b')			#votes Dems changed	

	elif(votesReps > votesReps_old):
		arduino.write(b'r')			#votes Reps changed


	#update last round
	seatsDems_old = seatsDems
	votesDems_old = votesDems
	seatsReps_old = seatsReps
	votesReps_old = votesReps

	updateNr += 1
	print("Update Nr.: "+str(updateNr))

	time.sleep(random.uniform(30.0,40.0))		#wait before new update


