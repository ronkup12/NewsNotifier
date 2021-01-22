# NewsNotifier
 ### A night project: WhatsApp Bot that sends to it's subscribers the recent top story of Ynet (https://www.ynet.co.il/).  
<br/>
WhatsApp Bot API used in this project is Twilio.

Port forwarding used in this project was ngrok.\
The local server is served with Flask (not for production).


<br/>
Usage:
<br/>
In windows, run ngrok like this:

```
    ngrok.exe http <LOCAL_PORT>
```

The output will look something like this:

    ngrok by @inconshreveable                                          (Ctrl+C to quit)
    Session Status                online
    Account                       <email> (Plan: Free)                      ngrok.exe start dev
    Version                       2.3.35
    Region                        United States (us)
    Web Interface                 http://127.0.0.1:4040
    Forwarding                    http://c72272b7b722.ngrok.io -> http://localhost:8080
    Forwarding                    https://c72272b7b722.ngrok.io -> http://localhost:8080
    Connections                   ttl     opn     rt1     rt5     p50     p90          
                                  0       0       0.00    0.00    0.00    0.00         


Copy the url ngrok provides (https://c72272b7b722.ngrok.io) and paste it with a '/bot' suffix in 'When a message comes in' box in this page: https://www.twilio.com/console/sms/whatsapp/sandbox. 

Save and run your python file:

    python news_notifier.py
