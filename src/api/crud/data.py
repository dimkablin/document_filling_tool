"""File for working with data"""

import os
import fitz
import warnings
import pandas as pd
from pathlib import Path
from typing import List

import src.env as env
from src.api.utils.utils import create_dir, check_extension

class Data:
    """Class for working with data"""
    def __init__(self):
        pass

    @staticmethod
    def create_excel_from_json(json_data):
        """Create excel from json data"""
        df_list = []
        for idx, inner_list in enumerate(json_data, start=1):
            data = []
            for entry in inner_list:
                row = {}
                for key, value in entry.items():
                    content = value.get('content', '')
                    row[key] = content
                data.append(row)
            df = pd.DataFrame(data)
            df_list.append(df)

        path = "./data/"
        path = os.path.join(path, 'output.xlsx')

        with pd.ExcelWriter(path) as writer:
            for idx, df in enumerate(df_list, start=1):
                df.to_excel(writer, sheet_name=f'Лист{idx}', index=False)

        # Return the file path and temporary directory
        return path
    
    @staticmethod
    def pdf_to_images(file_path: str, save_path: str, dpi: int = 72*3) -> List[str]:
        """Convert pdf to images"""
        paths = []

        for page in fitz.open(file_path):
            image = page.get_pixmap(matrix=fitz.Matrix(dpi/72.0, dpi/72.0))

            # Save the image as PNG
            image_path = os.path.join(
                save_path,
                f"page_{page.number}.png"
            )
            image.save(image_path)
            paths.append("/api/files" + image_path[10:])

        return paths

    @staticmethod
    def upload_files(chunk_id, files) -> List[str]:
        """Upload images to the server"""
        paths = []
        save_path = os.path.join(env.DATA_PATH, str(chunk_id))
        create_dir(save_path)

        for file in files:
            filename = file.filename.split('/')[-1]

            # разрешим загрузку файлов пдф и изображений
            if not check_extension(filename, env.FILE_EXTENSIONS | env.IMAGE_EXTENSIONS):
                warnings.warn("File extension is not supported.")
                continue

            file_path = os.path.join(save_path, filename)

            # сохраним файл в save_path
            with open(file_path, "wb") as wb_f:
                wb_f.write(file.file.read())
                paths.append("/api/files" + file_path[10:])

            # если файл пдф, то конвертируем его в изображения
            if check_extension(filename, env.FILE_EXTENSIONS):
                # выгрузим сканы в папку save_path
                i_save_path = os.path.join(save_path, filename)[:-4]
                create_dir(i_save_path)

                result = Data.pdf_to_images(file_path, i_save_path)
                paths += result

        return paths
    
    @staticmethod
    def get_chunk_id() -> int:
        """Convert pdf to images"""

        directory = env.DATA_PATH
        folders = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

        return len(folders) + 1
    
    @staticmethod
    def remove_file(file_path):
        """ Delete file by path to image
            "/api/files/2/0/page_0.png"
                2 - chunk_id
                0 - pdf_name
                page_0.png - pdf page
        """
        path_parts = file_path.split('/')
        file_name = path_parts[-1]#page_0.png
        file_folder = path_parts[-2]#0
        chunk_id = path_parts[-3]#2
        base_dir = env.DATA_PATH#"./src/data"

        image = os.path.join(base_dir, chunk_id, file_folder, file_name)
        image_folder = os.path.join(base_dir, chunk_id, file_folder)
        chunk_folder = os.path.join(base_dir, chunk_id)

        #Если файл существует, то удалим его
        if os.path.isfile(image):
            os.remove(image)
        else:
            #Если файла нет, то проверим есть ли пдф с таким именем
            pdf_file = os.path.join(base_dir, chunk_id, file_folder + ".pdf")
            #Удалим если такой pdf есть
            if os.path.isfile(pdf_file):
                os.remove(pdf_file)

        #Если файлов в каталоге pdf_name больше нет - удалим каталог
        if os.path.isdir(image_folder):
            if not os.listdir(image_folder):
                os.rmdir(image_folder)

        #Если файлов в каталоге chunk_id больше нет - удалим каталог
        if os.path.isdir(chunk_folder):
            if not os.listdir(chunk_folder):
                os.rmdir(chunk_folder)
