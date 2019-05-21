# running notes


from root directory
```
(slackbot> master) slackbot marhays $ source venv/bin/activate
(env) 
(slackbot> master) slackbot marhays $ source .env
(env)
(slackbot> master) slackbot marhays $ pip3 install -r requirements.txt 


```


`sample.env` - when someone else clones this repo, they can run `cp sample.env .env`, then edit `.env` to store values for `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`, then run `source .env` prior to running `app.py` 

```
(slackbot> master) slackbot marhays $ ls -la
total 84200
drwxr-xr-x  14 marhays  120010775       448 May 15 19:48 .
drwxr-xr-x   8 marhays  120010775       256 May 15 19:49 ..
-rw-r--r--@  1 marhays  120010775      6148 May 15 19:45 .DS_Store
-rw-r--r--   1 marhays  120010775       144 May 13 18:47 .env
drwxr-xr-x  15 marhays  120010775       480 May 15 19:50 .git
-rw-r--r--   1 marhays  120010775      1226 May 15 19:48 .gitignore
-rw-r--r--@  1 marhays  120010775  12793718 May  2 13:10 Pycon 2019 Workshop.pdf
-rw-r--r--   1 marhays  120010775      1036 May 13 19:29 README.md
-rw-r--r--   1 marhays  120010775      1705 May  2 13:02 README.rst
-rw-r--r--   1 marhays  120010775      2358 May 13 19:44 app.py
-rwxr-xr-x@  1 marhays  120010775  30276260 Apr 24 01:05 ngrok
-rw-r--r--   1 marhays  120010775        41 May  2 13:02 requirements.txt
-rw-r--r--   1 marhays  120010775        97 May 13 18:44 sample.env
drwxr-xr-x   5 marhays  120010775       160 May 15 19:45 venv
```