from pytube import YouTube

# link to download, test link for now
link = input("Enter YouTube link: ")

try:
    yt = YouTube(link)
except: # exceptions
    print("Error")

# filter
mp4 = yt.streams.filter(only_audio=True, file_extension='mp4')

try:
    mp4[0].download(filename = yt.title + '.mp4', output_path= 'C:/Users/user/Music')
except:
    print("Download Error")