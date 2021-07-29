
import aiofiles
import os

class FileWriter:

    @classmethod
    def create_folder_if_not_exist(cls, path):
        if not os.path.isdir(path):
            os.mkdir(path)

    @classmethod
    def save_image(cls, img_bytes, name, extension, path):
        cls.create_folder_if_not_exist(path)
        path_to_save = f'{path}/{name}.{extension}'
        with open(path_to_save, 'wb') as f:
            f.write(img_bytes)
        return path_to_save

    @classmethod
    def save_info(cls, info_text, name, path):
        cls.create_folder_if_not_exist(path)
        with open(f'{path}/{name}.txt', 'w') as f:
            f.write(info_text)

    @classmethod
    async def save_info_async(cls, info_text, name, path):
        cls.create_folder_if_not_exist(path)
        async with aiofiles.open(f'{path}/{name}.txt', 'w') as f:
            await f.write(info_text)