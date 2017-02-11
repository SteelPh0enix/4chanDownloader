import basc_py4chan as chan
import os
import urllib.request


def check_if_board_exists(name):
    boards = chan.get_all_boards()
    for b in boards:
        if b.name == name:
            return True
    return False

def download_board(board):
    if not os.path.exists('4chan/{0}'.format(board.name)):
        os.makedirs("4chan/{0}".format(board.name))

    print("Board name: {0}\nBoard title: {1}\nPage count: {2}\nSafe for work: {3}".format(board.name, board.title, board.page_count, board.is_worksafe))
    thread_ids = board.get_all_thread_ids()
    for thread_id in thread_ids:
        thread = board.get_thread(thread_id)
        if not os.path.exists("4chan/{0}/{1}".format(board.name, thread_id)):
            os.makedirs("4chan/{0}/{1}".format(board.name, thread_id))
        print(" >Thread ID: {0}\n  >Thread topic: {1}".format(thread_id, thread.topic.text_comment[:50].encode('utf-8')))
        for post in thread.all_posts:
            if post.has_file:
                print("   -> Post ID: {0}\n    -> Content: {1}\n    -> File size: {2}".format(post.post_id, post.text_comment[:100].encode('utf-8'), post.file_size))
                urllib.request.urlretrieve(post.file_url, filename="4chan/{0}/{1}/{2}".format(board.name, thread_id, post.file_url[post.file_url.rindex('/'):]))

def main():
    sel = input("Enter /shortname/ (without //) of board to download, * to get all, or ? to show the list (or 'fuck' to exit): ")
    if sel == "?":
        print(chan.get_all_boards())
        main()
    elif sel == "*":
        boards = chan.get_all_boards()
        for b in boards:
            download_board(b)
    elif sel == "fuck":
        return
    else:
        if check_if_board_exists(sel):
            download_board(chan.Board(sel))
        else:
            print("Select an existing board you dumb fuck")
            main()

if __name__ == "__main__":
    main()
