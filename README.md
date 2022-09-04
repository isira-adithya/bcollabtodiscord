## Burp Collaborator to Discord
This tool will poll a Burp Collaborator domain's client interactions and will notify those interactions to the user through Discord Webhooks.

## Requirements
This script requires the `requests` library - https://pypi.org/project/requests/.
Install it by running `pip install requests`.

## Setup
- Install Wireshark
- Start capturing the data packets from your network adapter
- Start Burpsuite
- Visit `Project Options` -> `Misc` and then tick the `Poll over unencrypted HTTP` option
- ![](https://i.imgur.com/PLNTkQu.png)
- Open the Burp Collaborator and click `Copy to clipboard` then click `Poll now`
- ![](https://i.imgur.com/1ssZ1nX.png)
- Make sure to notedown the collaborator domain somewhere or just add the domain to the value of `cdomain` in `./settings.json`
- Now, check the wireshark and filter the HTTP packets
- Find, HTTP request(s) to `http://polling.oastify.com/burpresults` or `https://polling.burpcollaborator.net/burpresults` *(Old versions of burpsuite will use this one)*
- Extract the `Collaborator URL` and the `BIID` from the HTTP request as shown below.
- ![](https://i.imgur.com/73mm0XS.png)
- Paste the value of `Collaborator URL` in `polling-endpoint` key in `./settings.json`
- Paste the value of `BIID` in `biid` key in `./settings.json`
- Now, create a discord server and create a new text channel.
- Under channel settings, goto `Integrations` and create a new webhook.
- ![](https://i.imgur.com/CHZp20u.png)
- Now copy the webhook URL and then paste the webhook URL inside the `dWebhook` key in `./settings.json`
- Finally, your `./settings.json` should be completed and the script is ready to be executed. 

## Executing
You can execute the script by running `python3 main.py`.
When running the script first time, you will receive a test HTTP request to the collaborator from the script.
![](https://i.imgur.com/gUd3X6w.png)

## Templates
You can customize your discord message templates by editing `txt` files under the `templates` folder.