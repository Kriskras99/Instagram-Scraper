"""Implements image parsing."""
import easyocr
import re

class OCR:
    """Class used for parsing terms from images.
    
    Reuse the same instance as much as possible as initialisation can take some time!
    """
    def __init__(self):
        self.reader = easyocr.Reader(['nl', 'en'])
    
    def image_to_terms(self, path):
        """Reads the text on a image and converts it into terms."""
        terms = []
        text = reader.readtext(img)
        for t in text:
            lowered = t[1].lower()
            terms.extend(re.findall(r'\w+', lowered))
        return terms
