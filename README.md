# running notes

`sample.env` - when someone else clones this repo, they can run `cp sample.env .env`, then edit `.env` to store values for `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`, then run `source .env` prior to running `app.py` 

```
(slackbot> master) pycon-2019 marhays $ ls -la
total 25048
drwxr-xr-x  11 marhays  120010775       352 May 13 19:20 .
drwxr-xr-x   9 marhays  120010775       288 May  2 13:01 ..
-rw-r--r--   1 marhays  120010775       144 May 13 18:47 .env
drwxr-xr-x  15 marhays  120010775       480 May 13 19:29 .git
-rw-r--r--   1 marhays  120010775      1203 May 13 19:20 .gitignore
-rw-r--r--@  1 marhays  120010775  12793718 May  2 13:10 Pycon 2019 Workshop.pdf
-rw-r--r--   1 marhays  120010775        10 May 13 19:19 README.md
-rw-r--r--   1 marhays  120010775      1705 May  2 13:02 README.rst
-rw-r--r--   1 marhays  120010775      2334 May 13 18:58 app.py
-rw-r--r--   1 marhays  120010775        41 May  2 13:02 requirements.txt
-rw-r--r--   1 marhays  120010775        97 May 13 18:44 sample.env
```