# running notes

## lets get goin'

### start app from root directory

1. get your virtural environment movin' - make sure you're workin' with pyhton 3

```
(slackbot> master) slackbot $ source venv/bin/activate 
```

2. store your slack signing secret & creds into your virturual environment

```
(env)
(slackbot> master) slackbot $ source .env
```

missing `.env`? np, we got you.

- run `cp sample.env .env`
- edit `.env` to store values for `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`
  - you'll find these in your app configuration api.slack.com/apps/ 
  - `SLACK_BOT_TOKEN` can be found in **OAuth & Permissions > Bot User OAuth Access Token**
  - `SLACK_SIGNING_SECRET` can be found in **Basic Information > Signing Secret**
- then run `source .env` 

^^ do this prior to running `app.py` 

3. make sure you have your slack-related requirements 
```
(env)
(slackbot> master) slackbot $ pip3 install -r requirements.txt
```

4. launch time

```
(env)
(slackbot> master) slackbot $ python3 app.py 
 * Tip: There are .env files present. Do "pip install python-dotenv" to use them.
 * Serving Flask app "slackeventsapi.server" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:3000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Tip: There are .env files present. Do "pip install python-dotenv" to use them.
 * Debugger is active!
 * Debugger PIN: 316-912-199
```

### port forward with ngrok & update your slack api Request URL

1. in new tab, start ngrok 

```
./ngrok http 3000 
```

should return something like this:

```
ngrok by @inconshreveable                                                                                                                                                                                   (Ctrl+C to quit)
                                                                                                                                                                                                                            
Session Status                online                                                                                                                                                                                        
Account                       <your@email.com> (Plan: Free)                                                                                                                                                     
Update                        update available (version 2.3.29, Ctrl-U to update)                                                                                                                                           
Version                       2.3.27                                                                                                                                                                                        
Region                        United States (us)                                                                                                                                                                            
Web Interface                 http://127.0.0.1:4040                                                                                                                                                                         
Forwarding                    http://0041a9e0.ngrok.io -> http://localhost:3000                                                                                                                                             
Forwarding                    https://0041a9e0.ngrok.io -> http://localhost:3000                                                                                                                                            
                                                                                                                                                                                                                            
Connections                   ttl     opn     rt1     rt5     p50     p90                                                                                                                                                   
                              0       0       0.00    0.00    0.00    0.00  
```

you should only need to care about the `https` forwarding address:

```
Forwarding                    https://0041a9e0.ngrok.io -> http://localhost:3000                                                                                                                                            
```

2. update your slackbot Request URL 

head on over to api.slack.com/apps and open up your slack app

Event Supscriptions > change your Request URL to `https://<session_token>.ngrok.io/slack/events`

Once verified, make sure you click **Save Changes**
