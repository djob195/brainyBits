import random

class ImageURLMock:
    def __init__(self):
        self.providers = [
            self._picsum
        ]

    def image_url(self, width=640, height=480):
        provider = random.choice(self.providers)
        return provider(width, height)

    def _picsum(self, width, height):
        seed = random.randint(1, 9999)
        return f"https://picsum.photos/seed/{seed}/{width}/{height}"
    
image_url_mock = ImageURLMock()