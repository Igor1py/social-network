class Table:

    def __init__(self, database):
        self._database = database

    def params_to_condition(self, **kwargs):
        if not kwargs:
            return ''
        kwargs.pop('limit', None)
        kwargs.pop('offset', None)
        return 'WHERE ' + ' AND '.join(
            f'{key} = %({key})s'
            for key in kwargs.keys()
        )

    def params_to_update(self, **kwargs):
        if not kwargs:
            return ''
        return 'SET ' + ', '.join(
            f'{key} = %({key})s'
            for key in kwargs.keys()
        )


class UserInfoTable(Table):

    table = None

    def create(self, **kwargs):
        self._database.execute_and_commit('''
        INSERT INTO {0} (user_id)
        VALUES (%(user_id)s)
        '''.format(self.table), kwargs)

    def get(self, **kwargs):
        return self._database.fetch_one('''
        SELECT * FROM {0}
        WHERE user_id = %(user_id)s
        '''.format(self.table), kwargs)

    def update(self, **kwargs):
        self._database.execute_and_commit('''
        UPDATE {0}
        {1}
        WHERE user_id = %(user_id)s
        '''.format(self.table, self.params_to_update(**kwargs)), kwargs)


class AuthorContentTable(Table):

    metadata = {
        'table': None,
        'model': None,
        'foreign_key': None,
        'dependent_table': None
    }

    @property
    def dependent_objects(self):
        if not self.metadata.get('dependent_table'):
            return ''
        return ''', (
            SELECT count(*) AS {dependent_table}_count
            FROM {dependent_table}
            WHERE {model}_id = id
        )'''.format(**self.metadata)

    @property
    def count_likes(self):
        return ''', (
            SELECT count(*) AS likes_count
            FROM {model}_likes
            WHERE id = {model}_id
        )'''.format(**self.metadata)

    def get(self, **kwargs):
        return self._database.fetch_one('''
        SELECT *{count_likes}{dependent_objects} FROM {table}
        WHERE id = %(id)s
        '''.format(**self.metadata,
                   count_likes=self.count_likes,
                   dependent_objects=self.dependent_objects
                   ), kwargs)

    def filter(self, **kwargs):
        return self._database.fetch_all('''
        SELECT *{count_likes}{dependent_objects} FROM {table}
        {condition}
        ORDER BY created DESC
        LIMIT %(limit)s
        OFFSET %(offset)s
        '''.format(**self.metadata,
                   count_likes=self.count_likes,
                   dependent_objects=self.dependent_objects,
                   condition=self.params_to_condition(**kwargs)
                   ), kwargs)

    def count(self, **kwargs):
        return self._database.fetch_one('''
        SELECT count(*) AS total_count FROM {table}
        {condition}
        '''.format(**self.metadata, condition=self.params_to_condition(**kwargs)), kwargs)

    def get_author_id(self, **kwargs):
        return self._database.fetch_one('''
        SELECT author_id FROM {table}
        WHERE id = %(id)s
        '''.format(**self.metadata), kwargs)

    def create(self, **kwargs):
        return self._database.execute_with_returning('''
        INSERT INTO {table}
        (author_id, {foreign_key}, content)
        VALUES
        (%(author_id)s, %({foreign_key})s, %(content)s)
        RETURNING *, (SELECT 0 AS likes_count)
        '''.format(**self.metadata), kwargs)

    def update(self, **kwargs):
        return self._database.execute_with_returning('''
        UPDATE {table}
        SET content = %(content)s
        WHERE id = %(id)s
        RETURNING *
        '''.format(**self.metadata), kwargs)

    def delete(self, **kwargs):
        return self._database.execute_and_commit('''
        DELETE FROM {table}
        WHERE id = %(id)s
        '''.format(**self.metadata), kwargs)

    def like(self, **kwargs):
        self._database.execute_and_commit('''
        INSERT INTO {model}_likes
        (user_id, {model}_id)
        VALUES
        (%(user_id)s, %({model}_id)s)
        '''.format(**self.metadata), kwargs)

    def unlike(self, **kwargs):
        self._database.execute_and_commit('''
        DELETE FROM {model}_likes
        WHERE user_id = %(user_id)s
        AND {model}_id = %({model}_id)s
        '''.format(**self.metadata), kwargs)
