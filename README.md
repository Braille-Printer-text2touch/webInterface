# Web Interface

The web interface component of the Braille printer project.

## How to Run

After cloning and `cd`-ing (["cd-ing?" A poem on verbification](https://files.mastodon.online/media_attachments/files/114/341/433/826/157/729/original/23c081c45573738d.jpeg)) into the cloned directory,

```bash
$ python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
sudo python3 app.py
```

## Pages

There are two pages for the web interface:

- home, at `/`
- admin, at `/admin`

Home is the main user landing page and the place for users to submit their documents. Admin is a page that shows status information about the printer.

## Structure

`app.py` is a Flask app that acts as the web interface to the Braille printer. It communicates to the printer both through a named pipe on the system and through the abstractions offered in `DriverCommunicator.py`, which itself speaks through the OS via POSIX message queues.
