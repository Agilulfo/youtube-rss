# youtube-rss
Get rss feeds for your youtube subscriptions

The script in this repository uses the [youtube api](https://developers.google.com/youtube/v3) to retrieve the list of youtube channels you are subscribed to.
it generates an `.opml` file that you can use to import the feeds in a RSS reader application

### opml format

it's a XML file that for some reasons seems to be the standard way to import and export rss feeds between applications.

[specs here](https://opml.org/spec2.opml)

Both [feeder](https://f-droid.org/en/packages/com.nononsenseapps.feeder/) and [Tunderbird](https://www.thunderbird.net)support this format to import and export feeds.

### how does it work

Each youtube channel has an id associated with it.
you can build the url for the feed corresponding to that channel by simply using this format:
`https://www.youtube.com/feeds/videos.xml?channel_id=<ID_HERE>`

 if open a channel page with your browser you can inspect the page and if you look for rss you should be able to find urls like this.

 Fortunately Google provides an api client for [youtube](https://developers.google.com/youtube/v3)that allows to retrieve the [list of youtube channels a user is subscribed to](https://developers.google.com/youtube/v3/docs/subscriptions/list)

### using the script

Youtube API uses [OAuth 2.0](https://developers.google.com/youtube/v3/guides/authentication) authentication.

This means that you cannot directly use your google credentials to call the API.

You can instead authorise an application to retrieve some information for you by granting limited rights.

If you want to use the script you must generate and export some credentials following the instructions provided in [here](https://developers.google.com/youtube/v3/getting-started).

The script expect a file named `client_secret.json`in the same directory of the script.

Remember to also add the google user for which you want to export the subscriptions as a tester.

When you run the script, it will open the browser and ask you to grant the permission to the application to get read access to you youtube data.

If you accept, the script will continue retrieving all the channels you are subscribed to and generating the opml file.

I've used [uv](https://github.com/astral-sh/uv) to run this project.

If you have it installed, to run the script it should be sufficient to run

```
uv run youtube-rss.py
```
