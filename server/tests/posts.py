import json
from requests import Session
from .test_cases import PostsTestCase

class PostTests(PostsTestCase):

    def test_create_post(self):
        self.register_user(self.USER_1_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        response = self.create_post(session, self.POST_1_PAYLOAD)
        self.assertEqual(response.status_code, 201)
        post = json.loads(response.content)
        self.assertEqual(post['id'], 1)
        self.assertEqual(post['author']['id'], 1)
        self.assertIn('created', post)
        self.assertEqual(post['category'], self.POST_1_PAYLOAD['category'])
        self.assertEqual(post['content'], self.POST_1_PAYLOAD['content'])
        self.assertEqual(post['likesCount'], 0)
    
    def test_create_post_not_logged(self):
        self.register_user(self.USER_1_PAYLOAD)
        session = Session()
        response = self.create_post(session, self.POST_1_PAYLOAD)
        self.assertEqual(response.status_code, 401)

    def test_get_posts_by_author_id(self):
        self.register_user(self.USER_1_PAYLOAD)
        self.register_user(self.USER_2_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        self.create_post(session, self.POST_1_PAYLOAD)
        self.create_post(session, self.POST_2_PAYLOAD)
        self.logout_user(session)
        self.login_user(session, self.USER_2_PAYLOAD)
        self.create_post(session, self.POST_3_PAYLOAD)
        response = self.get_posts({
            'authorId': 1,
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        posts = data['posts']
        self.assertEqual(len(posts), 2)
    
    def test_get_posts_by_category(self):
        self.register_user(self.USER_1_PAYLOAD)
        self.register_user(self.USER_2_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        self.create_post(session, self.POST_1_PAYLOAD)
        self.create_post(session, self.POST_2_PAYLOAD)
        self.logout_user(session)
        self.login_user(session, self.USER_2_PAYLOAD)
        self.create_post(session, self.POST_3_PAYLOAD)
        self.create_post(session, self.POST_4_PAYLOAD)
        payload = {
            'category': 'programming'
        }
        response = self.get_posts(payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        posts = data['posts']
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['category'], payload['category'])
        self.assertEqual(posts[0]['content'], self.POST_4_PAYLOAD['content'])
        self.assertEqual(posts[0]['author']['id'], 2)
        self.assertEqual(posts[1]['category'], payload['category'])
        self.assertEqual(posts[1]['content'], self.POST_1_PAYLOAD['content'])
        self.assertEqual(posts[1]['author']['id'], 1)

    def test_get_posts_by_category_and_author_id(self):
        self.register_user(self.USER_1_PAYLOAD)
        self.register_user(self.USER_2_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        self.create_post(session, self.POST_1_PAYLOAD)
        self.create_post(session, self.POST_4_PAYLOAD)
        self.create_post(session, self.POST_2_PAYLOAD)
        self.logout_user(session)
        self.login_user(session, self.USER_2_PAYLOAD)
        self.create_post(session, self.POST_3_PAYLOAD)
        self.create_post(session, self.POST_4_PAYLOAD)
        payload = {
            'category': self.POST_1_PAYLOAD['category'],
            'authorId': 1
        }
        response = self.get_posts(payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        posts = data['posts']
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['category'], payload['category'])
        self.assertEqual(posts[0]['author']['id'], payload['authorId'])
        self.assertEqual(posts[1]['category'], payload['category'])
        self.assertEqual(posts[1]['author']['id'], payload['authorId'])

    def test_update_post_by_author(self):
        self.register_user(self.USER_1_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        self.create_post(session, self.POST_1_PAYLOAD)
        response = self.update_post(session, 1, self.POST_2_PAYLOAD)
        self.assertEqual(response.status_code, 200)
        post = json.loads(response.content)
        self.assertEqual(post['category'], self.POST_2_PAYLOAD['category'])
        self.assertEqual(post['content'], self.POST_2_PAYLOAD['content'])

    def test_update_post_not_by_author(self):
        self.register_user(self.USER_1_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        self.create_post(session, self.POST_1_PAYLOAD)
        self.logout_user(session)
        self.register_user(self.USER_2_PAYLOAD)
        self.login_user(session, self.USER_2_PAYLOAD)
        response = self.update_post(session, 1, self.POST_2_PAYLOAD)
        self.assertEqual(response.status_code, 401)

    def test_update_post_not_logged(self):
        self.register_user(self.USER_1_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        self.create_post(session, self.POST_1_PAYLOAD)
        self.logout_user(session)
        response = self.update_post(session, 1, self.POST_2_PAYLOAD)
        self.assertEqual(response.status_code, 401)
    
    def test_delete_post_by_author(self):
        self.register_user(self.USER_1_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        response = self.create_post(session, self.POST_1_PAYLOAD)
        post = json.loads(response.content)
        response = self.delete_post(session, post['id'])
        self.assertEqual(response.status_code, 205)

    def test_delete_post_not_by_author(self):
        self.register_user(self.USER_1_PAYLOAD)
        self.register_user(self.USER_2_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        response = self.create_post(session, self.POST_1_PAYLOAD)
        post = json.loads(response.content)
        self.logout_user(session)
        self.login_user(session, self.USER_2_PAYLOAD)
        response = self.delete_post(session, post['id'])
        self.assertEqual(response.status_code, 401)

    def test_delete_post_not_logged(self):
        self.register_user(self.USER_1_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        response = self.create_post(session, self.POST_1_PAYLOAD)
        post = json.loads(response.content)
        self.logout_user(session)
        response = self.delete_post(session, post['id'])
        self.assertEqual(response.status_code, 401)

    def test_like_post(self):
        self.register_user(self.USER_1_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        response = self.create_post(session, self.POST_1_PAYLOAD)
        post = json.loads(response.content)
        response = self.like(session, {'post_id': post['id']})
        self.assertEqual(response.status_code, 201)
    
    def test_like_post_not_logged(self):
        self.register_user(self.USER_1_PAYLOAD)
        session = Session()
        self.login_user(session, self.USER_1_PAYLOAD)
        response = self.create_post(session, self.POST_1_PAYLOAD)
        post_data = json.loads(response.content)
        self.logout_user(session)
        response = self.like(session, {'post_id': post_data['id']})
        self.assertEqual(response.status_code, 401)
