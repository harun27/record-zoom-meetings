import os, subprocess, time, csv, sys


def read_table():
	
	data = []
	if not os.path.isfile("Times.csv"):
		sys.exit("The File 'Times.csv' does not exist!")
	with open('Times.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			
			url = row['URL']
			hour_from, min_from = row['From'].split(":")
			hour_to, min_to = row['To'].split(":")
			dic = {'From': (int(hour_from), int(min_from)), 'To': (int(hour_to), int(min_to)), 'URL': url}
			print(dic)
			data.append(dic)
	
	return data


def check_time(times, reference):
	
	loctime = time.localtime()
	now_min = loctime.tm_min
	now_hour = loctime.tm_hour
	now = (now_hour, now_min)
	
	print("Time now: " + str(now))
	
	if all(s >= t for s, t in zip(now, times[reference])):
		return True
	else:
		return False
		
			
def open_meeting(zoom_url):
	print("Start obs ...")
	os.chdir("C:/Program Files/obs-studio/bin/64bit")
	obs = subprocess.Popen("obs64.exe --startrecording --minimize-to-tray")
	
	print("Start the meeting ...")
	chrome = subprocess.Popen("C:/Program Files/Google/Chrome/Application/chrome.exe --new-window " + zoom_url)
	time.sleep(5)
	subprocess.Popen.terminate(chrome)
	
	return obs


if __name__ == "__main__":
	print("Reading file")
	data = read_table()
	
	num_meetings = len(data)
	next_meeting = 0
	
	while(next_meeting < num_meetings):
		print("Proof the start of the meeting " + str(next_meeting))
		start = check_time(data[next_meeting], 'From')
		
		if start:
			print("starting meeting " + str(next_meeting))
			obs = open_meeting(data[next_meeting]['URL'])
			
			print("Proof the end of the meeting " + str(next_meeting))
			while(not check_time(data[next_meeting], 'To')):
				time.sleep(60)
			
			subprocess.Popen.terminate(obs)
			start = False
			next_meeting += 1
			
		time.sleep(60)










