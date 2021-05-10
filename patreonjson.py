from pelican import signals
from pelican.readers import BaseReader
from pathlib import Path
from urllib import parse as urlparse
import requests
import json
import os

FILE_EXTENSIONS = ['json']

def getPatreonCampaign(json_data):
    u = urlparse.urlparse(json_data['pledge_url'])
    return urlparse.parse_qs(u.query)['c'][0]

def getPatreonSlug(json_data, subpath="posts/"):
    patreon_url = json_data['patreon_url']
    return patreon_url[patreon_url.find(subpath) + len(subpath):]

def getPatreonTags(json_data):

    if "post_tags" in json_data:
        return json_data["post_tags"]
    else:
        tags_filepath = Path(f"extra_metadata")
        tags_filepath /= f"{json_data['id']}.json"
        try:
            with open(tags_filepath, "r", encoding="utf-8") as fp:
                extra_metadata = json.load(fp)
            return extra_metadata["post_tags"]
        except (FileNotFoundError, json.JSONDecodeError):
            raise

    # Finally we have tags_json




# <style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style>
# <script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>

# Create a new reader class, inheriting from the pelican.reader.BaseReader
class MarkdeepReader(BaseReader):
    enabled = True  # Yeah, you probably want that :-)

    # The list of file extensions you want this reader to match with.
    # If multiple readers were to use the same extension, the latest will
    # win (so the one you're defining here, most probably).
    file_extensions = FILE_EXTENSIONS

    # You need to have a read method, which takes a filename and returns
    # some content and the associated metadata.
    def read(self, filename):
        with open(filename, "r", encoding="utf-8") as fp:
            full_body = fp.read()

        __, plainname = os.path.split(filename)

        json_data = json.loads(full_body)

        metadata = {
            key: json_data[key]
            for key in ('title', 'date', 'category')
        }

        metadata.update({
            'author': json_data['creator']['full_name'],
            'template': "patreon_article",
            'slug': getPatreonSlug(json_data),
            'tags': getPatreonTags(json_data),
            'data': json_data,
        })

        if summary := json_data.get('teaser_text'):
            metadata['summary'] = summary

        parsed_metadata = {
            key: self.process_metadata(key, value)
            for key, value in metadata.items()
        }

        content_html = json_data['content']

        # TODO preprocess images

        return content_html, parsed_metadata

# This is how pelican works.
def add_reader(readers):
    for fe in FILE_EXTENSIONS:
        readers.reader_classes[fe] = MarkdeepReader

def register():
    signals.readers_init.connect(add_reader)