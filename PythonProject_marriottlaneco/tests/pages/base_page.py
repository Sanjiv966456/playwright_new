class BasePage:
    def __init__(self, page, base_url: str = ""):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def goto(self, path: str = ""):
        url = f"{self.base_url}/{path.lstrip('/') }" if path else self.base_url
        return self.page.goto(url)

    def title(self):
        return self.page.title()

    def get_h1_text(self):
        h1 = self.page.query_selector("h1")
        return h1.inner_text().strip() if h1 else None

