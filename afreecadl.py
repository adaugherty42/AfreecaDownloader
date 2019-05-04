import wget
import requests
import ffmpeg
import time
import os
import sys
import re
import xml.etree.ElementTree as ET
import urllib
import urllib.request as urllib2

class afreecaVideo:
    def __init__(self, url_base, duration):
        self.url_base = url_base
        self.duration = duration

file_ext = ".ts"

info_url = "http://afbbs.afreecatv.com:8080/api/video/get_video_info.php?"

def download_chunklist(video):
	count = (video.duration // 3)
	failed_downloads = []
	num_fails = 0
	global file_ext

	for i in range(0, count+1):
		if not os.path.isfile("video/" + str(i) + file_ext):
			try:
				print("Downloading chunk " + str(i) + "/" + str(count) + "...")
				wget.download(video.url_base + str(i) + file_ext, "video/" + str(i) + file_ext);
				print("\nDone\n")
			except urllib.error.HTTPError as e:
				failed_downloads.append(i)
				print(e)

	#Retry failed chunks up to five more times
	while (failed_downloads):
		for i in failed_downloads:
			try:
				wget.download(video.url_base + str(i) + file_ext, "video/" + str(i) + file_ext);
				failed_downloads.remove(i)
				num_fails = 0
			except urllib.error.HTTPError as e:
				print(e)
				num_fails += 1
				if (num_fails == 5):
					print("Timed out five times in a row, try again later...")
					sys.exit()

def write_chunklist_file(video):
	global file_ext
	count = (video.duration // 3)

	print("Writing chunklist file...\n")
	chunklist = open("video/chunklist.txt", "a")
	for i in range(0, count+1):
		chunklist.write("file \'" + str(i) + file_ext + "\'\n")
	chunklist.close()
	print("Done\n")

def concat_video(output_file_name):
	print("Concatenating files together...\n")

	if not os.path.isfile(output_file_name):
		(
		ffmpeg
		.input("video/chunklist.txt", format="concat", safe=0)
		.output(output_file_name, c="copy")
		.run()
		)

	print("Done\n\nJob Done!!")

def clean_up(video):
	global file_ext
	count = (video.duration // 3)

	for i in range(0, count+1):
		os.remove("video/" + str(i) + file_ext)
	os.remove("video/chunklist.txt")

def parseXML(xmlfile):
	root = ET.parse(urllib2.urlopen(xmlfile)).getroot()
	video_list = []

	for i in root.findall("./track/video/file"):
	    url_base = (grab_url_base(i.text))
	    duration = int(i.attrib['duration'])
	    video_list.append(afreecaVideo(url_base, duration))

	return video_list

def grab_url_base(url):
	page = urllib2.urlopen(url).read().decode('utf-8')
	url_base = re.search(r"original\"\n(.+)m3u8", page).group(1) + "_"
	return url_base

def grab_video_info(url):
	page = urllib2.urlopen(url).read().decode('utf-8')
	video_id = re.search(r"name=\"nTitleNo\" value=\"([0-9]+)", page).group(1)
	station_id = re.search(r"name=\"nStationNo\" value=\"([0-9]+)", page).group(1)
	bbs_id = re.search(r"name=\"nBbsNo\" value=\"([0-9]+)", page).group(1)

	global info_url
	info_url += ("nTitleNo=" + str(video_id) + 
	            "&nStationNo=" + str(station_id) +
	            "&nBbsNo=" + str(bbs_id))

	return parseXML(info_url)

def main():
	address = sys.argv[1]
	player = sys.argv[2]
	date = sys.argv[3]
	hour = sys.argv[4]

	video_list = grab_video_info(address)
	video = video_list[int(hour)-1]

	download_chunklist(video)
	write_chunklist_file(video)
	
	output_file_name = "video/" + player + "_" + date + "_" + hour + ".mp4"
	concat_video(output_file_name)

	clean_up(video)


if __name__ == '__main__':
	main()