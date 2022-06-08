import json
from urllib.parse import urlencode
from urllib.request import urlopen


root_url = 'https://api.isic-archive.com/api/v2/'
image_url = root_url + 'images/search/'


def download_isic_images(out_dir, offset=0, limit=float('inf'), dx=None, batch_size=50):
    params = {'limit': batch_size,
              'offset': offset,
              'query': 'diagnosis:"%s"' % dx}
    images_url = image_url + '?' + urlencode(params)
    images_url = images_url.replace('+', '%20')

    images = json.load(urlopen(images_url))
    images_url = images['next']
    images = images['results']
    image_num = offset
    count = 0
    while images:
        if count >= limit:
            break
        for img in images:
            if count >= limit:
                break
            image_num += 1
            name = img['isic_id']
            download_image(img, out_dir, name)
            count += 1
        params['offset'] += batch_size
        images = json.load(urlopen(images_url))
        images_url = images['next']
        images = images['results']
    return image_num


def download_image(metadata, out_dir, name):
    img_path = "%s/%s.jpg" % (out_dir, name)
    # Download Image
    download_url = metadata['urls']['full']
    img = urlopen(download_url)
    with open(img_path, 'wb') as f:
        f.write(img.read())
