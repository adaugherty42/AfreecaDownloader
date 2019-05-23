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
import json
import datetime
import logging
import subprocess

class afreecaVideo:
    def __init__(self, url_base, num_chunks):
    	self.url_base = url_base
    	self.num_chunks = num_chunks

file_ext = ".ts"

info_url = "http://afbbs.afreecatv.com:8080/api/video/get_video_info.php?"

def download_chunklist(video):
	failed_downloads = []
	num_fails = 0
	global file_ext

	for i in range(0, video.num_chunks):
		if not os.path.isfile("video/" + str(i) + file_ext):
			try:
				logging.info("Downloading chunk " + str(i) + "/" + str(video.num_chunks-1) + "...")
				wget.download(video.url_base + str(i) + file_ext, "video/" + str(i) + file_ext, bar=None);
				logging.info("Done\n")
			except urllib.error.HTTPError as e:
				failed_downloads.append(i)
				logging.info(e)

	if (failed_downloads):
		logging.info("\nRetrying failed downloads...\n")

	#Retry failed chunks up to five more times
	while (failed_downloads):
		for i in failed_downloads:
			try:
				logging.info("Retrying chunk " + str(i) + "/" + str(video.num_chunks-1) + "...")
				wget.download(video.url_base + str(i) + file_ext, "video/" + str(i) + file_ext, bar=None);
				failed_downloads.remove(i)
				num_fails = 0
			except urllib.error.HTTPError as e:
				logging.info(e)
				logging.info("")
				num_fails += 1
				if (num_fails == 5):
					logging.info("\nTimed out five times in a row, try again later...")
					sys.exit()

def write_chunklist_file(video):
	global file_ext

	logging.info("Writing chunklist file...\n")
	chunklist = open("video/chunklist.txt", "a")
	for i in range(0, video.num_chunks):
		chunklist.write("file \'" + str(i) + file_ext + "\'\n")
	chunklist.close()
	logging.info("Done\n")

def concat_video(output_file_name):
	logging.info("Concatenating files together...\n")

	if not os.path.isfile(output_file_name):
		(
		ffmpeg
		.input("video/chunklist.txt", format="concat", safe=0)
		.output(output_file_name, c="copy")
		.run()
		)

	logging.info("Done\n\nJob Done!!")

def clean_up(video):
	global file_ext

	for i in range(0, video.num_chunks):
		os.remove("video/" + str(i) + file_ext)
	os.remove("video/chunklist.txt")

def parseXML(xmlfile):
	root = ET.parse(urllib2.urlopen(xmlfile)).getroot()
	video_list = []

	for i in root.findall("./track/video/file"):
	    url_base = (grab_url_base(i.text))
	    #duration = int(i.attrib['duration'])
	    num_chunks = grab_num_chunks(url_base[:-1] + "m3u8")
	    video_list.append(afreecaVideo(url_base, num_chunks))

	return video_list

def grab_url_base(url):
	page = urllib2.urlopen(url).read().decode('utf-8')
	url_base = re.search(r"original\"\n(.+)m3u8", page).group(1) + "_"
	return url_base

def grab_num_chunks(url):
	page = urllib2.urlopen(url)
	lines = len(page.readlines())
	return (lines - 5) // 2

def grab_video_info(url):
	page = urllib2.urlopen(url).read().decode('utf-8')
	video_id = re.search(r"name=\"nTitleNo\" value=\"([0-9]+)", page).group(1)
	station_id = re.search(r"name=\"nStationNo\" value=\"([0-9]+)", page).group(1)
	bbs_id = re.search(r"name=\"nBbsNo\" value=\"([0-9]+)", page).group(1)
	streamer = re.search(r"szBjId=([0-9a-zA-Z]+)&", page).group(1)
	date = datetime.datetime.strptime(
		re.search(r"<span>(\d{2,4}[/-]\d{1,2}[/-]\d{1,2}) ", page).group(1),
		"%Y-%m-%d")

	global info_url
	info_url += ("nTitleNo=" + str(video_id) + 
	            "&nStationNo=" + str(station_id) +
	            "&nBbsNo=" + str(bbs_id))

	return (parseXML(info_url), streamer, date)

def get_streamer_list(nickname_as_key):
	streamers = {}

	response = requests.get('https://bwstreams.appspot.com/streams.json')
	data = json.loads(response.text)

	if (nickname_as_key):
		for i in data['streams'].keys():
			streamers[data['streams'][i]['nickname'].capitalize()] = i[8:]
	else:
		for i in data['streams'].keys():
			streamers[i[8:]] = data['streams'][i]['nickname'].capitalize()

	return streamers

def download_video(video):
	download_chunklist(video)
	write_chunklist_file(video)

	output_file_name = "video/" + player + "_" + date + "_" + hour + ".mp4"
	concat_video(output_file_name)

	clean_up(video)

def main():
	address = sys.argv[1]
	player = sys.argv[2]
	date = sys.argv[3]
	hour = sys.argv[4]

	video_list, streamer, date = grab_video_info(address)
	video = video_list[int(hour)-1]
	logging.info(streamer)
	logging.info(date)

	download_chunklist(video)
	write_chunklist_file(video)
	
	output_file_name = "video/" + player + "_" + date + "_" + hour + ".mp4"
	concat_video(output_file_name)

	clean_up(video)


if __name__ == '__main__':
	main()