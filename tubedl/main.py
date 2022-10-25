from bottle import run, request, get, post, template, route, static_file
import youtube_dl
import os.path


# Serve up the static files (CSS and images)
@route('/static/<style.css>')
def server_static(filepath):
    return static_file(filepath, root='./static/')


# Site header
header = '''
        <link href="https://fonts.googleapis.com/css?family=Roboto|Oswald" rel="stylesheet">
        <link href="/static/style.css" rel="stylesheet">
        <div class="main">

        <h1>SGATE YouTube Video Downloader <img src="/static/dl.png"></h1>

        '''


# Web root
@get('/')
def main_page():
    pwd = os.path.dirname(os.path.abspath(__file__))
    print (pwd)
    drive_path = os.path.join(pwd, 'static', 'videos')
    print (drive_path)
    directorylist = os.listdir(drive_path)

    page = '''
                <b>Paste a YouTube URL:</b><br>
                <input id="url" type="url" name="url" form="mainform"><br>
                <form id="mainform" method="POST">
                <button id="submit" class="submit" type="submit">Submit</button>
                </form>
                <p><b>Recent Downloads:</b></p>
                <div class="list">
                '''

    for item in directorylist:
        listing = template('''
                <p><a href="/static/videos/{{item}}">{{item}}</a></p>
                ''', item=item)

        page += listing

    page += "</div>"
    page = header + page

    return page


# Page to post to
@post('/')
def process_request():
    url_to_convert = request.POST.get('url')

    print ("URL received:", url_to_convert)

    if ("youtube" not in url_to_convert) and ("youtu.be" not in url_to_convert):
        downloadresponse = "<p>No download performed.</p>"
        postresponse = '''
                    <b>Bad URL or processing error.</b><br>Please make sure the URL points to a YouTube video.
                    <p><a href="/"><button id="back" class="back" type="button">Back</button></a></p>
                    '''
    else:

        ydl_opts = {'username': 'techsupport@sgate.k12.mi.us', 'password': 'gibIe3a2e',
                    'download-archive': './static/videos/', 'format':'mp4'}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:

            result = ydl.extract_info(url_to_convert, download=False)

            if 'entries' in result:
                # Can be a playlist or a list of videos
                video = result['entries'][0]
                video_title = video['title']

            else:
                # Just a video
                video = result
                video_title = video['title']

            print (video)
            print (video_title)

            folder1 = "static"
            folder2 = "videos"

            fullpath = os.path.join(folder1, folder2)
            fullname = os.path.join(folder1, folder2, video_title + ".mp4")

            print (fullname)

            if not os.path.isfile(fullname):
                downloadresponse = "<p>Video not on server yet, downloaded just now.</p>"
                os.chdir("./static/videos/")
                ydl.download([url_to_convert])
                os.chdir("./../../")
            else:
                downloadresponse = "<p>Video already on server, serving it from local cache.</p>"

            postresponse = template('''
                        <p><b>Provided URL:</b> {{url}}</p>
                        <p>Saved File: <a href="{{savefile}}">{{filename}}</a></p>
                        <p>Right-click the above link and select "Save Link As" to download the file.</p>
                        <p><a href="/"><button id="back" class="back" type="button">Back</button></a></p>
                        ''', url=url_to_convert, savefile=fullname, filename=video_title)

    page = header + downloadresponse + postresponse
    return page

# Local testing
# run(server='cherrypy', host='localhost', port=1337)

# Live
run(server='cherrypy', host='wiki.sgate.k12.mi.us', port=1337)
