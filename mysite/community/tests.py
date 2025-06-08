from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import StudyGroup, Forum, Discussion, Comment, UserReputation, ReportedContent
from django.utils.text import slugify

User = get_user_model()

class CommunityModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.staff_user = User.objects.create_user(username='staffuser', password='12345', is_staff=True)
        
        # Create a study group
        self.group = StudyGroup.objects.create(
            name='Test Group',
            description='A test study group',
            admin=self.user1,
            is_private=False
        )
        self.group.members.add(self.user1)
        
        # Create a forum
        self.forum = Forum.objects.create(
            name='Test Forum',
            description='A test forum',
            study_group=self.group
        )
        
        # Create a discussion
        self.discussion = Discussion.objects.create(
            title='Test Discussion',
            content='This is a test discussion',
            forum=self.forum,
            author=self.user1
        )
        
        # Create a comment
        self.comment = Comment.objects.create(
            discussion=self.discussion,
            author=self.user2,
            content='This is a test comment'
        )

    def test_study_group_creation(self):
        """Test that study group is created with correct slug"""
        self.assertEqual(self.group.slug, slugify(self.group.name))
        self.assertEqual(str(self.group), 'Test Group')

    def test_forum_creation(self):
        """Test that forum is created with correct slug"""
        self.assertEqual(self.forum.slug, slugify(self.forum.name))
        self.assertEqual(str(self.forum), 'Test Forum')

    def test_discussion_creation(self):
        """Test that discussion is created correctly"""
        self.assertEqual(str(self.discussion), 'Test Discussion')
        self.assertEqual(self.discussion.author, self.user1)
        self.assertFalse(self.discussion.is_pinned)
        self.assertFalse(self.discussion.is_locked)

    def test_comment_creation(self):
        """Test that comment is created correctly"""
        self.assertEqual(self.comment.discussion, self.discussion)
        self.assertEqual(self.comment.author, self.user2)
        self.assertFalse(self.comment.is_solution)

    def test_user_reputation_system(self):
        """Test the reputation system"""
        reputation = UserReputation.objects.create(user=self.user2)
        self.assertEqual(reputation.points, 0)
        self.assertEqual(reputation.level, 1)
        
        # Test reputation points increase
        reputation.points += 10
        reputation.save()
        self.assertEqual(reputation.points, 10)

    def test_report_content(self):
        """Test content reporting system"""
        report = ReportedContent.objects.create(
            reporter=self.user2,
            content_type='discussion',
            content_id=self.discussion.id,
            reason='Inappropriate content'
        )
        self.assertFalse(report.is_resolved)
        self.assertEqual(report.content_type, 'discussion')

class CommunityViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = StudyGroup.objects.create(
            name='Test Group',
            description='A test study group',
            admin=self.user,
            is_private=False
        )

    def test_group_list_view(self):
        """Test the group list view"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('community:group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Group')

    def test_private_group_access(self):
        """Test private group access restrictions"""
        other_user = User.objects.create_user(username='otheruser', password='12345')
        private_group = StudyGroup.objects.create(
            name='Private Group',
            description='A private study group',
            admin=self.user,
            is_private=True
        )
        
        # Test access as non-member
        self.client.login(username='otheruser', password='12345')
        response = self.client.get(reverse('community:group_detail', kwargs={'slug': private_group.slug}))
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_discussion_creation(self):
        """Test discussion creation"""
        self.client.login(username='testuser', password='12345')
        forum = Forum.objects.create(
            name='Test Forum',
            description='A test forum',
            study_group=self.group
        )
        
        response = self.client.post(
            reverse('community:discussion_create', kwargs={'forum_slug': forum.slug}),
            {'title': 'New Discussion', 'content': 'Discussion content'}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after creation
        self.assertTrue(Discussion.objects.filter(title='New Discussion').exists())

    def test_comment_solution_marking(self):
        """Test marking a comment as solution"""
        self.client.login(username='testuser', password='12345')
        forum = Forum.objects.create(name='Test Forum', description='A test forum', study_group=self.group)
        discussion = Discussion.objects.create(
            title='Test Discussion',
            content='Content',
            forum=forum,
            author=self.user
        )
        comment = Comment.objects.create(
            discussion=discussion,
            author=self.user,
            content='Solution comment'
        )
        
        response = self.client.post(reverse('community:mark_solution', kwargs={'pk': comment.pk}))
        comment.refresh_from_db()
        self.assertTrue(comment.is_solution)

    def test_community_link_visibility(self):
        """Test that community link is visible only to authenticated users"""
        # Test unauthenticated user
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'href="' + reverse('community:group_list') + '"')
        self.assertNotContains(response, '学习社区')

        # Test authenticated user
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="' + reverse('community:group_list') + '"')
        self.assertContains(response, '学习社区')
