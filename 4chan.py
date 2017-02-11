import basc_py4chan as chanapi
import requests
import argparse
import sys
import os

class Downloader:
    def __init__(self):
        self.boards_list = chanapi.get_all_boards()

    def run(self):
        self.verify_boards()
        if len(self.board) == 0:
            print("No existing boards selected, you fucking idiot!")
            sys.exit(2)
        elif self.board[0] == '*':
            self.boards = chanapi.get_all_boards()
        else:
            self.boards = chanapi.get_boards(self.board)

        if self.thread_id != None:
            self.download_threads(self.boards[0])
        else:
            self.download_boards()

    def board_exists(self, board_name):
        for board in self.boards_list:
            if board.name == board_name:
                return True
        return False

    def thread_exists(self, thread_id):
        return self.board[0].thread_exists(thread_id)

    def verify_boards(self):
        if self.board[0] == '*':
            return

        for f in self.board:
            if not self.board_exists(f):
                self.board.remove(f)

    def download_threads(self, board):
        for tid in self.thread_id:
            print(" >Thread #{0} at /{1}/:".format(tid, board.name))
            if (board.thread_exists(tid)):
                t = board.get_thread(tid)
                t.expand()
                thread_files = t.files()
                thread_files_sum = sum(1 for _ in thread_files)
                fnum = 1
                print(" =>Closed/sticky/archived?: {0}/{1}/{2}\n =>Bumplimit/imagelimit hit: {3}/{4}\n =>Posts: {5}\n =>Files: {6}\n =>Topic: {7}".format(
                t.closed, t.sticky, t.archived, t.bumplimit, t.imagelimit, len(t.all_posts), thread_files_sum, t.topic.text_comment[:50].encode('utf-8')
                ))

                for thread_file in t.files():
                    print("{0}/{1}".format(fnum, thread_files_sum))
                    self.download_image(thread_file, "{0}/{1}/{2}".format(self.directory, board.name, tid))
                    fnum += 1
            else:
                print(" =>Thread is 404 (don't exists or got deleted)")
            print("")

    def download_boards(self):
        for b in self.boards:
            self.thread_id = b.get_all_thread_ids()
            self.download_threads(b)

    def download_image(self, url, path):
        file_name = url.split('/')[-1]
        imgpath = "{0}/{1}".format(path, file_name)
        if not os.path.exists(path):
            os.makedirs(path)

        print("Downloading image {0}".format(file_name))
        response = requests.get(url, stream=True)
        size = int(response.headers.get('content-length'))

        if os.path.isfile(imgpath) and os.path.getsize(imgpath) == size:
            print("File is already downloaded!")
            return

        f = open(imgpath, "wb")
        if (size is None):
            f.write(response.content)
        else:
            dl = 0
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / size)
                sys.stdout.write("\r[{0}{1}]".format('=' * done, ' ' * (50-done)))
                sys.stdout.flush()
            print("")

parser = argparse.ArgumentParser(description="Download pics from your favourite fucking boards (or threads). Enter board names, or one board name and threads ID's.", epilog="op is a faggot")
parser.add_argument('-d', '--directory', default="4chan", help="directory or path in which pics will be saved (default: 4chan)")
parser.add_argument('-b', '--board', help="board(s) short name(s) from where pictures will be downloaded (* means all boards, enter multiple with spaces)", nargs='+')
parser.add_argument('-t', '--thread_id', help="thread ID's from where pics will be downloaded (you can enter multiple with spaces)", nargs='+')

dl = Downloader()
args = parser.parse_args(namespace=dl)
if dl.board == None:
    print("You must enter at least one board, faggot!")
    sys.exit(1)
dl.run()
