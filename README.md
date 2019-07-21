# pastebin-monitor-and-alert
A pastebin monitor and alerter using the scraping API.

Alerts are sent using [pushover](https://pushover.net/) directly to your mobile device, you can set the [priority](https://pushover.net/api#priority) level of the alerts all the way up to EMERGENCY if you want to make sure you don't miss them.

original by [Mike Wilks](https://github.com/mikewilks), see his version on [github](https://github.com/mikewilks/simple-pastebin-monitor). He wrote about this in his [blog](http://www.mikewilks.com/home/who-has-your-data)

Pastebin Monitor and Alert is a small Python script that replicates and and extends Pastebin alerts. It makes use of the [Pastebin Scraping API](https://pastebin.com/api_scraping_faq). You'll need a Pastebin PRO account to work with the Scraping API, because it allows you to whitelist the IP address where the script is running from.

The script can take three parameters, but definitions can also be done from within the script:
1. The name and location of the file containing the keywords to check (default is ./keywords.txt)
2. The directory to save the pastes into (default is ./FOUND)
3. Whether to check for the pastebin message that your IP is not authorized or not (default is true)

The script will check Pastebin for pastes every minute and compare their text against the supplied keywords. When there is a match the text of the paste is saved to the output directory (in a directory with the name of the matched keyword). This is an improvement over the built in Pastebin alerts which only saves a link which means you miss removed pastes if you don't click the link before they are taken down.

Running the script can be done in a [screen](https://linux.die.net/man/1/screen) or [tmux](https://linux.die.net/man/1/tmux) so you can keep it running unattended. The machine where you run needs to be have its IP whitelisted in your Pastebin PRO [account](https://pastebin.com/pro?help=1). 

Pre-requisites are Python 2 or 3, Requests, a Pastebin PRO account and an internet connection.
