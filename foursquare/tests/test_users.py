#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2016 Mike Lewis
import logging; log = logging.getLogger(__name__)

import os

from . import TEST_DATA_DIR, BaseAuthenticatedEndpointTestCase



class UsersEndpointTestCase(BaseAuthenticatedEndpointTestCase):
    """
    General
    """
    def test_user(self):
        response = self.api.users()
        assert 'user' in response

    def test_search_twitter(self):
        response = self.api.users.search(params={'twitter': u'mLewisLogic'})
        assert 'results' in response

    def test_search_name(self):
        response = self.api.users.search(params={'name': u'Mike'})
        assert 'results' in response

    def test_requests(self):
        response = self.api.users.requests()
        assert 'requests' in response

    """
    Aspects
    """
    def test_checkins(self):
        response = self.api.users.checkins()
        assert 'checkins' in response

    def test_checkins_limit(self):
        response = self.api.users.checkins(params={'limit': 10})
        assert 'checkins' in response

    def test_checkins_offset(self):
        response = self.api.users.checkins(params={'offset': 3})
        assert 'checkins' in response

    def test_all_checkins(self):
        checkins = list(self.api.users.all_checkins())
        assert isinstance(checkins, list)

    def test_friends(self):
        response = self.api.users.friends()
        assert 'friends' in response

    def test_friends_limit(self):
        response = self.api.users.friends(params={'limit': 10})
        assert 'friends' in response

    def test_friends_offset(self):
        response = self.api.users.friends(params={'offset': 3})
        assert 'friends' in response

    def test_lists(self):
        response = self.api.users.lists()
        assert 'lists' in response

    def test_lists_created(self):
        response = self.api.users.lists(params={'group': u'created'})
        assert 'lists' in response

    def test_lists_followed(self):
        response = self.api.users.lists(params={'group': u'followed'})
        assert 'lists' in response

    def test_lists_friends(self):
        response = self.api.users.lists(params={'group': u'friends'})
        assert 'lists' in response

    def test_mayorships(self):
        response = self.api.users.mayorships()
        assert 'mayorships' in response

    def test_photos(self):
        response = self.api.users.photos()
        assert 'photos' in response

    def test_photos_limit(self):
        response = self.api.users.photos(params={'limit': 10})
        assert 'photos' in response

    def test_photos_offset(self):
        response = self.api.users.photos(params={'offset': 3})
        assert 'photos' in response

    def test_tips(self):
        response = self.api.users.tips()
        assert 'tips' in response

    def test_venuehistory(self):
        response = self.api.users.venuehistory()
        assert 'venues' in response

    def test_venuelikes(self):
        response = self.api.users.venuelikes()
        assert 'venues' in response

    """
    Actions
    """
    def test_update_name(self):
        # Change my name to Miguel
        response = self.api.users.update(params={'firstName': 'Miguel'})
        assert 'user' in response
        assert response['user']['firstName'] == 'Miguel'
        # Change it back
        response = self.api.users.update(params={'firstName': 'Mike'})
        assert 'user' in response
        assert response['user']['firstName'] == 'Mike'

    def test_update_photo(self):
        test_photo = os.path.join(TEST_DATA_DIR, 'profile_photo.jpg')
        # Fail gracefully if we don't have a test photo on disk
        if os.path.isfile(test_photo):
            photo_data = open(test_photo, 'r')
            try:
                response = self.api.users.update(photo_data=photo_data)
                assert 'user' in response
            finally:
                photo_data.close()
        else:
            print(u"Put a 'test-photo.jpg' file in the testdata/ directory to enable this test.")
