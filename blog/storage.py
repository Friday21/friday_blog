# coding:utf-8
from __future__ import unicode_literals, absolute_import

import hashlib
import random
from io import BytesIO

from django.core.files.storage import Storage
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from PIL import Image, ImageSequence


class BlogStorage(Storage):

    def _get_filename(self, name):
        md5 = hashlib.md5()
        md5.update(name.encode('utf-8'))
        random_str = str(random.randint(1000, 9999))
        return settings.MEDIA_PREFIX + md5.hexdigest() + random_str

    def _save(self, name, content):
        filename = self._get_filename(name)
        im = Image.open(BytesIO(content.read()))
        extension = im.format
        filename = filename+'.'+extension
        if extension.upper() in 'GIF':
            frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
            frames[0].save(filename, extension, append_images=frames[1:], duraton=40, save_all=True)
            return filename.split('/')[-1]
        elif isinstance(content, ImageFieldFile) and content.field.name == 'icon':
            x, y = im.size
            if x > 200 and y > 200:
                im = im.resize((200, 200), Image.ANTIALIAS)
            else:
                m = min(x, y)
                im = im.resize((m, m), Image.ANTIALIAS)
        elif isinstance(content, ImageFieldFile) and content.field.name == 'image':
            x, y = im.size
            if y > 800:
                x_s = x/(y/800.0)
                y_s = 800
            else:
                y_s = y/(x/800.0)
                x_s = 800
            im = im.resize((int(x_s), int(y_s)), Image.ANTIALIAS)
        im.save(filename, extension, quality=80)
        return filename.split('/')[-1]

    def exists(self, name):
        pass

    def delete(self, name):
        pass

    def listdir(self, path):
        pass

    def size(self, name):
        pass

    def url(self, name):
        return settings.MEDIA_URL + name
