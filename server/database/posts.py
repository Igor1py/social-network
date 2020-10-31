from .tables import AuthorContentTable

class Posts(AuthorContentTable):

    metadata = {
        'table': 'posts',
        'model': 'post',
        'foreign_key': 'category',
        'dependent_table': 'comments'
    }
    
    def get_categories(self):
        return self._database.fetch_all('SELECT * FROM categories')
