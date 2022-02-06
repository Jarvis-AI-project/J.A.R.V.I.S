shut_check = input('Do you want to shut down the computer after download? (y/n) : ')
csv_file_name = str(input('Enter the csv file name: ')) + str('.csv')

# function to download video
def VideoDownloader(url_input, video_name, video_path):
    import youtube_dl
    ydl_opts = {
        'nopart': True,
        'format': 'bestvideo+bestaudio/best', # download best quality of video and audio available
        'outtmpl': video_path+'/'+video_name # output file name
    }
    url = str(url_input)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url]) # download video from url input and save it in the same directory as the script


# function to read csv file and append the title and url to a list
urls = []
def ReadCSV(file_name):
    import csv
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # edit the video name to remove any special characters
            row[0] = row[0].replace(': ', '')
            row[0] = row[0].replace('||', 'II')

            # if pw_check == 'y':
            if '.mp4' in row[1]:
                # edit the video url to paste master.m3u8
                video_link_initial = row[1]
                j=''
                for i in  range(75):
                    j+=video_link_initial[i]

                video_link_final = j + 'master.m3u8'
                row[1] = video_link_final
            urls.append(row)
    csv_file.close() # close the csv file

ReadCSV(csv_file_name)

# shuting down the computer after download
def shut_down(n):
    if shut_check == 'y':
        # showing user that the computer will shut down in n seconds
        import time
        print(f'Shutting down in {n} sec...') # computer will shut down in 5 min after download.
        time.sleep(n)

        # shut down the remote computer
        try:
            import sys
            sys.path.insert(0, 'V:\\J.A.R.V.I.S\\features')
            import command_remotly.command_server as command_server
            command_server.send_command('shutdown')
            time.sleep(2)
            if command_server.reply == 'shutting down sir':
                print('NAS is shutting down...')
            time.sleep(5)
            
        except:
            print('Error: Shutting down the computer failed.')

        # shut down the main computer
        import os
        os.system('shutdown -s -t 0')

# main function
def main():
    for task in urls:
        if '.mp4' in task[1]:               # for pw protected videos
            video_name = task[0] + '.mp4'
        else:
            video_name = task[0]
        video_link = task[1]
        video_path = task[2]
        print('-'*500) # print a line
        print('New Video: ' + video_name)
        print('New Video Link: ' + video_link)
        print('New Video Path: ' + video_path)
        print('Downloading...')
        print('-'*500) # print a line
        
        VideoDownloader(video_link, video_name, video_path)
    
    # shuting down the computer after download
    shut_down(300)

# calling main function
main()
print('All videos downloaded!')

# using multiprocessing to download videos in parallel
# from multiprocessing import Process
# if __name__ == '__main__':
#     process_list = []
#     for task in urls:
#         video_name = task[0] + '.mp4'
#         video_link = task[1]
#         video_path = task[2]
#         process = Process(target=VideoDownloader, args=(video_link, video_name, video_path))
#         process_list.append(process)
#         process.start()
#     for process in process_list:
#         process.join()
# code completed..... :) :) :)