from attr import dataclass


@dataclass
class BookDTO:
    source: str
    book_id: str
    title: str
    subtitle: str
    editor: str
    description: str
    publication_date: str
    categories: list = []
    authors: list = []

    def business_key(self) -> str:
        return f"{self.source}_{self.book_id}"

    def parse_to_dict(self) -> dict:
        return {
            'source': self.source,
            'id': self.book_id,
            'title': self.title,
            'subtitle': self.subtitle,
            'authors': self.authors,
            'editor': self.editor,
            'published_date': self.publication_date,
            'description': self.description,
            'categories': self.categories,
        }
