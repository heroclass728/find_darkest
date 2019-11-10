import os

from dark_area_extraction.extract_darkness import ExtractDarkness


if __name__ == '__main__':

    _cur_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(_cur_dir, "bg", "9ZZAjllXBail.png")
    ExtractDarkness(_cur_dir).extract_darkness()
    # ExtractDarkness(_cur_dir).extract_darkness_image(image_path)
