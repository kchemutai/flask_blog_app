from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='skmbuga', email='skmbuga@gmail.com')
        u.set_password('test_pass')
        self.assertFalse(u.check_password('testpass'))
        self.assertTrue(u.check_password('test_pass'))

    def test_avatar(self):
        u = User(username='skmbuga', email='skmbuga@gmail.com')
        self.assertEqual(u.avatar(10), 'https://www.gravatar.com/avatar/3221f180bce31e12dc0c8e508d34a58f?d=mp&s=10')

    def test_follow_and_unfollow(self):
        user1 = User(username='skmbuga', email='skmbuga@gmail.com')
        user2 = User(username='gnakimera', email='gnakimera@ymail.com')
        user3 = User(username='kchemutai', email='kchemutai@yahoo.com')
        user4 = User(username='tmusani', email='tmusani@gmail.com')

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)

        db.session.commit()

        self.assertEqual(user1.followed.all(), [])
        self.assertEqual(user2.followed.all(), [])
        self.assertEqual(user3.followed.all(), [])
        self.assertEqual(user4.followed.all(), [])

        user1.follow(user2)
        user2.follow(user3)
        user3.follow(user4)
        user4.follow(user1)

        db.session.commit()

        self.assertFalse(user4.is_following(user2))
        self.assertTrue(user1.is_following(user2))
        self.assertFalse(user1.is_following(user3))
        self.assertTrue(user2.is_following(user3))
        self.assertTrue(user3.is_following(user4))
        self.assertTrue(user4.is_following(user1))

        user1.unfollow(user2)
        user3.unfollow(user4)
        db.session.commit()

        self.assertFalse(user1.is_following(user2))
        self.assertFalse(user3.is_following(user4))
        
def test_follow_posts(self):
    user1 = User(username='skmbuga', email='skmbuga@gmail.com')
    user2 = User(username='gnakimera', email='gnakimera@ymail.com')
    user3 = User(username='kchemutai', email='kchemutai@yahoo.com')
    user4 = User(username='tmusani', email='tmusani@gmail.com')

    db.session.add_all(user1, user2, user3,user4)
    db.session.commit()

    now = datetime.now()

    #  create 4 posts
    p1 = Post(content="post from skmbuga", author=user1, timestamp=now + timedelta(seconds=1))
    p2 = Post(content="post from gnakimera", author=user2, timestamp=now + timedelta(seconds=4))
    p3 = Post(content="post from kchemutai", author=user3, timestamp=now + timedelta(seconds=3))
    p4 = Post(content="post from tmusani", author=user4,timestamp=now + timedelta(seconds=2))
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()

    user1.follow(user2)
    user1.follow(user4)
    user2.follow(user3)
    user3.follow(user4)

    db.session.commit()

    # check for followed posts in each user
    followed_posts_user1 = user1.followed_posts.all()
    followed_posts_user2 = user2.followed_posts.all()
    followed_posts_user3 = user3.followed_posts.all()
    followed_posts_user4 = user4.followed_posts.all()

    self.assertEqual(followed_posts_user1, [p1, p2, p4])
    self.assertEqual(followed_posts_user2, [p2, p3])
    self.assertEqual(followed_posts_user3, [p3, p4])
    self.assertEqual(followed_posts_user4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)