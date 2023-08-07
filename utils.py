import os
import random

from config import Config


def getting_a_photo():
    """Получение случайного фото."""
    files = os.listdir(Config.PEOPLE_FOLDER)
    images = [file for file in files]
    images = random.choice(images)
    image_final = os.path.join(Config.PEOPLE_FOLDER, images)
    return image_final
