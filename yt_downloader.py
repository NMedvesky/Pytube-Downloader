from pytube import YouTube
from pytube import Stream
from pytube import Playlist
from pytube.cli import on_progress
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from rich.traceback import install
from rich.layout import Layout
from rich.panel import Panel
import time
import json
import os

# Installs error styling
install()


def download(url):
	""" Main download Function """

	# Define vars
	yt = YouTube(url, on_progress_callback=on_progress)
	ytname = yt.title
	streamdict = {}

	# Get download path
	with open("settings.json", "r") as f:
		jsondata = json.load(f)

	file_path = jsondata["path"]
	autoitag = jsondata["autoitag"]

	if file_path == "Videos\\Pytube_Downloads":
		file_path = str(f"{os.path.expanduser('~')}\\Videos\\Pytube_Downloads")

	if not autoitag:
		itaglist = []
		table0 = Table(title="[green]Backup Option (Video)")
		table1 = Table(title="[green]Download Options (Video)")
		table2 = Table(title="[green]Download Options (Audio)")

		# Add columns to download options table
		table0.add_column("[green]Itag", style="green")
		table0.add_column("[green]File Type", style="cyan")
		table0.add_column("[green]Res", style="green")
		table0.add_column("[green]FPS", style="cyan")
		table0.add_column("[green]Size KB", style="green")
		table0.add_column("[green]Audio Codec", style="cyan")
		table0.add_column("[green]Bitrate", style="green")

		# Add columns to download options table
		table1.add_column("[green]Itag", style="green")
		table1.add_column("[green]File Type", style="cyan")
		table1.add_column("[green]Res", style="green")
		table1.add_column("[green]FPS", style="cyan")
		table1.add_column("[green]Size KB", style="green")
		table1.add_column("[green]Audio Codec", style="cyan")
		table1.add_column("[green]Bitrate", style="green")

		# Add columns to download options table
		table2.add_column("[green]Itag", style="green")
		table2.add_column("[green]File Type", style="cyan")
		table2.add_column("[green]Abr", style="green")
		table2.add_column("[green]Size KB", style="green")
		table2.add_column("[green]Audio Codec", style="cyan")
		table2.add_column("[green]Bitrate", style="green")

		# Status message for getting video data
		print(f"[green]Getting metadata for '{ytname}'")

		stream1 = yt.streams.filter(progressive=True).get_highest_resolution()
		table0.add_row(str(f"[yellow]{stream1.itag}"), str(stream1.mime_type), str(stream1.resolution), str(stream1.fps), str(int(stream1._filesize/1024)), str(stream1.video_codec), str(stream1.bitrate))
		itaglist.append(str(stream1.itag))

		for stream in yt.streams.filter(adaptive=True):
			if stream.type == "video":
				fps = stream.fps
				res = stream.resolution
				codec = stream.video_codec

				table1.add_row(str(f"[yellow]{stream.itag}"), str(stream.mime_type), str(res), str(fps), str(int(stream._filesize/1024)), str(codec), str(stream.bitrate))
				itaglist.append(str(stream.itag))
			else:
				abr = stream.abr
				codec = stream.audio_codec

				table2.add_row(str(f"[yellow]{stream.itag}"), str(stream.mime_type), str(abr), str(int(stream._filesize/1024)), str(codec), str(stream.bitrate))
				itaglist.append(str(stream.itag))

		# Display download options and allows the user to choose one
		print(table0, table1, table2)
		itag = Prompt.ask("[green]Choose an Itag option", choices=itaglist)

		# Gets the stream object from the itag the user choose
		stream = yt.streams.get_by_itag(int(itag))
	else:
		table0 = Table(title="[green]Backup Option (Video)")

		# Add columns to download options table
		table0.add_column("[green]Itag", style="green")
		table0.add_column("[green]File Type", style="cyan")
		table0.add_column("[green]Res", style="green")
		table0.add_column("[green]FPS", style="cyan")
		table0.add_column("[green]Size KB", style="green")
		table0.add_column("[green]Audio Codec", style="cyan")
		table0.add_column("[green]Bitrate", style="green")

		stream = yt.streams.filter(progressive=True).get_highest_resolution()
		table0.add_row(str(f"[yellow]{stream.itag}"), str(stream.mime_type), str(stream.resolution), str(stream.fps), str(int(stream._filesize/1024)), str(stream.video_codec), str(stream.bitrate))

		print(table0)

	if stream.exists_at_path(file_path):
		print(f"\n[yellow]Video already downloaded at [blue]{file_path}\n")
	else:
		# Status message for when it starts to download the video
		print(f"[green]Downloading [cyan]'{ytname}' [green]at [blue]{file_path}\n")
		
		# Downloading the video
		start = time.time()
		stream.download(file_path)
		end = time.time()

		# Status message for when the download finishes
		print(f"\n[green]Finished downloading [cyan]'{ytname}' [green]in [purple]{end-start}s\n")


if __name__ == "__main__":
	print("[green]Loading...")
	
	# Start up message
	with open("ascii_art.txt") as f:
		print(f"[green]{f.read()}")
	print(f"[green]By Niko\n")

	default_settings = {"path": f"{os.path.expanduser('~')}\\Videos\\Pytube_Downloads", "autoitag": False}

	# Command line loop
	while True:
		cmd = Prompt.ask("[green]#admin-> ")
		if cmd.startswith("http"):
			# Downloads the youtube video from the url
			download(cmd)

		elif cmd.startswith("playlist"):
			# Download all videos from a playlist
			playlisturl = cmd.split(" ")
			playlist = Playlist(playlisturl[1])
			for url in playlist.video_urls:
				download(url)

		elif cmd.startswith("settings"):
			with open("settings.json", "r") as f:
				jsondata = json.load(f)

			print(f'\npath = "{jsondata["path"]}"')
			print(f'autoitag = {jsondata["autoitag"]}\n')

		elif cmd.startswith("setpath"):
			# Set download path for downloading videos
			pathsetting = cmd.split(" ", 1)
			with open("settings.json", "r") as f:
				jsondata = json.load(f)

			jsondata["path"] = pathsetting[1]

			with open("settings.json", "w") as f:
				json.dump(jsondata, f)

		elif cmd.startswith("autoitag"):
			# If true it will auto select backup option for downloads
			autoitag_setting = cmd.split(" ", 1)
			with open("settings.json", "r") as f:
				jsondata = json.load(f)

			if autoitag_setting[1] == "-true":
				autoitag_setting = True
			else:
				autoitag_setting = False

			jsondata["autoitag"] = autoitag_setting

			with open("settings.json", "w") as f:
				json.dump(jsondata, f)

		elif cmd.startswith("setdefault"):
			# Reset all settings
			with open("settings.json", "w") as f:
				json.dump(default_settings, f)

		else:
			print("\n[green]Enter a youtube video url to start downloading it or enter a command from the list")
			print("[cyan]playlist (playlisturl) -> Download all videos from a playlist")
			print("[green]settings -> Displays the current settings")
			print("[cyan]setpath (downloadpath) -> Set download path for downloading videos")
			print("[green]autoitag -true, -false -> If true it will auto select backup option for downloads")
			print("[cyan]setdefault -> Reset all settings\n")
