# 4chanDownloader
Simple command-line tool for downloading pics from 4chan boards/threads.

#### Based on Python 3.6, requires:
- this shit to work: https://pypi.python.org/pypi/BASC-py4chan/0.6.3 (pip install basc-py4chan)
- and requests library: http://docs.python-requests.org/en/master/ (pip install requests)

## Usage:
`python 4chan.py [-d directory (default: 4chan)] [-b board(s)] [-t thread(s)]`

### Examples:
Download fucking everything to default directory:
`python 4chan.py -b *`

Download all /b/ files to default directory
`python 4chan.py -b b`

Download all /b/, /v/ and /s4s/ files to folder called bullshit
`python 4chan.py -d bullshit -b b v s4s`

Download threads with ID 2137, 420 and 69 from board /s4s/ to default directory
`python 4chan.py -b s4s -t 2137 420 69`

You can download selected threads from only one board at time (only 1st board will be used with thread ID's, use script multiple times to download selected threads from selected boards).
Use -b * to download every file from every board
