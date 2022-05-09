class Feed:
    def __init__(self, url: str = None,
                 text: str = None,
                 photo: str = None,
                 post_id: str = None) -> None:
        self.url = url
        self.post_id = post_id
        self.text = text
        self.photo = photo
