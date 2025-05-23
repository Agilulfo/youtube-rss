# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import datetime

import xml.etree.ElementTree as ET

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def authorize():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )

    credentials = flow.run_local_server()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    return youtube


def get_subscriptions(youtube):
    subscriptions = []

    next_page = append_subscriptions(youtube, subscriptions)

    while next_page:
        next_page = append_subscriptions(youtube, subscriptions, next_page)

    return subscriptions


def append_subscriptions(youtube, subscriptions, page=None):
    request = youtube.subscriptions().list(
        part="snippet", maxResults=50, mine=True, pageToken=page, order="alphabetical"
    )

    response = request.execute()

    for channel in response["items"]:
        subscriptions.append(
            {
                "title": channel["snippet"]["title"],
                "id": channel["snippet"]["resourceId"]["channelId"],
            }
        )
    return response.get("nextPageToken")


def timestamp():
    now = datetime.datetime.now(datetime.UTC)
    return now.strftime("%Y%m%d_%H%M%S")


def write_opml(subscriptions):
    opml = ET.Element("opml")
    opml.set("version", "1.1")
    ET.SubElement(opml, "head")
    body = ET.SubElement(opml, "body")

    for item in subscriptions:
        outline = ET.SubElement(body, "outline")
        outline.set("type", "rss")
        outline.set("text", item["title"])
        outline.set("title", item["title"])
        outline.set(
            "xmlUrl",
            f"https://www.youtube.com/feeds/videos.xml?channel_id={item['id']}",
        )

    tree = ET.ElementTree(opml)
    ET.indent(tree, space="\t")
    tree.write(f"yt_{timestamp()}.opml", xml_declaration=True)


def main():
    # get authorize client
    youtube = authorize()

    subscriptions = get_subscriptions(youtube)
    write_opml(subscriptions)


if __name__ == "__main__":
    main()
