from pelican import signals
from pelican.readers import BaseReader
from urllib import parse as urlparse
from pathlib import Path
import glob
import requests
import json
import bs4
import re
import os

import logging

logger = logging.getLogger(__name__)

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
            # 'template': "patreon_article",
            'slug': getPatreonSlug(json_data),
            'tags': getPatreonTags(json_data),
            'data': json_data,
        })

        # TODO post_file

        if summary := json_data.get('teaser_text'):
            metadata['summary'] = summary

        try:
            content_html = json_data['content']
        except KeyError:
            logger.error(f"{filename!r}: content missing!")
            content_html = "<pre>Content missing</pre>"

        parent_dir = os.path.split(filename)[0]

        if image_gallery := json_data.get("images"):
            metadata['image_gallery'] = []
            for image in image_gallery:
                file_name = image['file_name']
                globstr = os.path.join(parent_dir, f"{json_data['id']}_*_{file_name}")
                try:
                    local_image = os.path.split(glob.glob(globstr)[0])[1]
                    metadata['image_gallery'].append(local_image)
                except IndexError:
                    logger.error(f"Could not find image file by glob {globstr!r}!")
                    raise

                content_html += "<a href='{attach}%s'></a>" % local_image

        # TODO preprocess images
        soup_doc = bs4.BeautifulSoup(content_html, 'html.parser')

        # known_files = [filename]

        # # zzzzzzzip em up
        # parent_dir = os.path.split(filename)[0]
        media_ids = [img['data-media-id'] for img in soup_doc.select('img[data-media-id]')]
        child_images = [
            os.path.split(path)[1] for path in 
            glob.glob(os.path.join(parent_dir, f"{json_data['id']}_*.*"))
            if re.match(r'.*_\d+_\d+\..{3,4}$', path) and not path.endswith("json")
            and not os.path.split(path)[1] in metadata.get('image_gallery', [])
        ]

        if not len(media_ids) == len(child_images):
            logger.debug(media_ids)
            logger.debug(child_images)
            raise AssertionError("Media ID length mismatch (view debug!)")

        for img in soup_doc.select('img[data-media-id]'):
            media_id = img['data-media-id']
            try:
                img['src'] = "{attach}" + child_images[media_ids.index(media_id)]
            except IndexError:
                logger.error(f"Could not find media_id {media_id!r} in media ids!")
                raise

        content_html = str(soup_doc)

        parsed_metadata = {
            key: self.process_metadata(key, value)
            for key, value in metadata.items()
        }

        return content_html, parsed_metadata

# This is how pelican works.
def add_reader(readers):
    for fe in FILE_EXTENSIONS:
        readers.reader_classes[fe] = MarkdeepReader

def register():
    signals.readers_init.connect(add_reader)