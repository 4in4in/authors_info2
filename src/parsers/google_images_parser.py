
import os
from base64 import b64decode
from bs4 import BeautifulSoup
from src.utils.face_detector import FaceDetector

class ImageInfo:

    def __init__(self, src_str, url):
        self.url = url
        self.img_str = self.get_b64_img_str(src_str)
        self.extension = self.get_img_extension(src_str)
        self.img_bytes = b64decode(self.img_str)
        self.has_face = FaceDetector.is_image_contains_face(self.img_bytes)

    def get_b64_img_str(self, src_str):
        header_end_pos = src_str.find(',') + 1
        img_str = src_str[ header_end_pos : ]
        return img_str

    def get_img_extension(self, src_str):
        extension_start = src_str.find('/') + 1
        extension_end = src_str.find(';')
        extension = src_str[ extension_start : extension_end ]
        return extension

class GoogleImagesParser:

    @classmethod
    def get_images(cls, html_data):
        if not html_data:
            return
        html_doc = BeautifulSoup(html_data, features='html.parser')
        img_tags = html_doc.findAll('img', { 'jsname': True, 'src': True })
        image_infos = []
        for img_tag in img_tags[:20]: # потому что после 20-го тега содержимого изображеня в нём нет
            url = img_tag.parent.parent.parent.find('a', { 'href': True, 'target': '_blank' })['href']
            image_infos.append(ImageInfo(img_tag['src'], url))

        return image_infos

if __name__ == '__main__':
    with open('./test_files/test3.html', 'r') as f:
        html_doc = f.read()

    imgs_info = GoogleImagesParser.get_images(html_doc)
            