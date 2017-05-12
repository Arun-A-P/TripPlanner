#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2016 Mike Lewis
import logging; log = logging.getLogger(__name__)

from . import BaseAuthenticatedEndpointTestCase, BaseUserlessEndpointTestCase



class VenuesEndpointTestCase(BaseAuthenticatedEndpointTestCase):
    """
    General
    """
    def test_venue(self):
        response = self.api.venues(self.default_venueid)
        assert 'venue' in response


    def test_categories(self):
        response = self.api.venues.categories()
        assert 'categories' in response


    def test_explore(self):
        response = self.api.venues.explore(params={'ll': self.default_geo})
        assert 'groups' in response

    def test_explore_radius(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'radius': 30})
        assert 'groups' in response

    def test_explore_section(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'section': u'café'})
        assert 'groups' in response

    def test_explore_query(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'query': 'donuts'})
        assert 'groups' in response

    def test_explore_limit(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'limit': 10})
        assert 'groups' in response

    def test_explore_intent(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'intent': 'specials'})
        assert 'groups' in response


    def test_managed(self):
        response = self.api.venues.managed()
        assert 'venues' in response


    def test_search(self):
        response = self.api.venues.search(params={'ll': self.default_geo})
        assert 'venues' in response

    def test_search_query(self):
        response = self.api.venues.search(params={'ll': self.default_geo, 'query': 'donuts'})
        assert 'venues' in response

    def test_search_limit(self):
        response = self.api.venues.search(params={'ll': self.default_geo, 'limit': 10})
        assert 'venues' in response

    def test_search_browse(self):
        response = self.api.venues.search(params={'ll': self.default_geo, 'radius': self.default_geo_radius, 'intent': 'browse'})
        assert 'venues' in response


    def test_suggestcompletion(self):
        response = self.api.venues.suggestcompletion(params={'ll': self.default_geo, 'query': 'cof'})
        assert 'minivenues' in response


    def test_trending(self):
        response = self.api.venues.trending(params={'ll': self.default_geo})
        assert 'venues' in response

    def test_trending_limit(self):
        response = self.api.venues.trending(params={'ll': self.default_geo, 'limit': 10})
        assert 'venues' in response

    def test_trending_radius(self):
        response = self.api.venues.trending(params={'ll': self.default_geo, 'radius': 100})
        assert 'venues' in response


    """
    Aspects
    """
    def test_event(self):
        response = self.api.venues.events(self.default_venueid)
        assert 'events' in response


    def test_herenow(self):
        response = self.api.venues.herenow(self.default_venueid)
        assert 'hereNow' in response

    def test_herenow_limit(self):
        response = self.api.venues.herenow(self.default_venueid, params={'limit': 10})
        assert 'hereNow' in response

    def test_herenow_offset(self):
        response = self.api.venues.herenow(self.default_venueid, params={'offset': 3})
        assert 'hereNow' in response


    def test_listed(self):
        response = self.api.venues.listed(self.default_venueid)
        assert 'lists' in response

    def test_listed_group(self):
        response = self.api.venues.listed(self.default_venueid, params={'group': 'friends'})
        assert 'lists' in response

    def test_listed_limit(self):
        response = self.api.venues.listed(self.default_venueid, params={'limit': 10})
        assert 'lists' in response

    def test_listed_offset(self):
        response = self.api.venues.listed(self.default_venueid, params={'offset': 3})
        assert 'lists' in response


    def test_photos(self):
        response = self.api.venues.photos(self.default_venueid, params={'group': 'venue'})
        assert 'photos' in response

    def test_photos_limit(self):
        response = self.api.venues.photos(self.default_venueid, params={'limit': 10})
        assert 'photos' in response

    def test_photos_offset(self):
        response = self.api.venues.photos(self.default_venueid, params={'offset': 3})
        assert 'photos' in response


    def test_similar(self):
        response = self.api.venues.similar(self.default_venueid)
        assert 'similarVenues' in response


    def test_tips(self):
        response = self.api.venues.tips(self.default_venueid)
        assert 'tips' in response

    def test_tips_group(self):
        response = self.api.venues.tips(self.default_venueid, params={'sort': 'popular'})
        assert 'tips' in response

    def test_tips_limit(self):
        response = self.api.venues.tips(self.default_venueid, params={'limit': 10})
        assert 'tips' in response

    def test_tips_offset(self):
        response = self.api.venues.tips(self.default_venueid, params={'offset': 3})
        assert 'tips' in response



class VenuesUserlessEndpointTestCase(BaseUserlessEndpointTestCase):
    """
    General
    """
    def test_venue(self):
        response = self.api.venues(self.default_venueid)
        assert 'venue' in response


    def test_categories(self):
        response = self.api.venues.categories()
        assert 'categories' in response


    def test_explore(self):
        response = self.api.venues.explore(params={'ll': self.default_geo})
        assert 'groups' in response

    def test_explore_radius(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'radius': 30})
        assert 'groups' in response

    def test_explore_section(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'section': 'coffee'})
        assert 'groups' in response

    def test_explore_query(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'query': 'donuts'})
        assert 'groups' in response

    def test_explore_limit(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'limit': 10})
        assert 'groups' in response

    def test_explore_intent(self):
        response = self.api.venues.explore(params={'ll': self.default_geo, 'intent': 'specials'})
        assert 'groups' in response


    def test_search(self):
        response = self.api.venues.search(params={'ll': self.default_geo})
        assert 'venues' in response

    def test_search_query(self):
        response = self.api.venues.search(params={'ll': self.default_geo, 'query': 'donuts'})
        assert 'venues' in response

    def test_search_limit(self):
        response = self.api.venues.search(params={'ll': self.default_geo, 'limit': 10})
        assert 'venues' in response

    def test_search_browse(self):
        response = self.api.venues.search(params={'ll': self.default_geo, 'radius': self.default_geo_radius, 'intent': 'browse'})
        assert 'venues' in response

    def test_search_ampersand(self):
        response = self.api.venues.search(params={'query': u'Mirch Masala Restaurant & Bar', 'll': u'22.52,88.36'})
        assert 'venues' in response
        assert len(response['venues']) # Make sure there's at least one result


    def test_trending(self):
        response = self.api.venues.trending(params={'ll': self.default_geo})
        assert 'venues' in response

    def test_trending_limit(self):
        response = self.api.venues.trending(params={'ll': self.default_geo, 'limit': 10})
        assert 'venues' in response

    def test_trending_radius(self):
        response = self.api.venues.trending(params={'ll': self.default_geo, 'radius': 100})
        assert 'venues' in response


    """
    Aspects
    """
    def test_listed(self):
        response = self.api.venues.listed(self.default_venueid)
        assert 'lists' in response

    def test_listed_group(self):
        response = self.api.venues.listed(self.default_venueid, params={'group': 'other'})
        assert 'lists' in response

    def test_listed_limit(self):
        response = self.api.venues.listed(self.default_venueid, params={'limit': 10})
        assert 'lists' in response

    def test_listed_offset(self):
        response = self.api.venues.listed(self.default_venueid, params={'offset': 3})
        assert 'lists' in response


    def test_photos(self):
        response = self.api.venues.photos(self.default_venueid, params={'group': 'venue'})
        assert 'photos' in response

    def test_photos_limit(self):
        response = self.api.venues.photos(self.default_venueid, params={'limit': 10})
        assert 'photos' in response

    def test_photos_offset(self):
        response = self.api.venues.photos(self.default_venueid, params={'offset': 3})
        assert 'photos' in response


    def test_tips(self):
        response = self.api.venues.tips(self.default_venueid)
        assert 'tips' in response

    def test_tips_group(self):
        response = self.api.venues.tips(self.default_venueid, params={'sort': 'popular'})
        assert 'tips' in response

    def test_tips_limit(self):
        response = self.api.venues.tips(self.default_venueid, params={'limit': 10})
        assert 'tips' in response

    def test_tips_offset(self):
        response = self.api.venues.tips(self.default_venueid, params={'offset': 3})
        assert 'tips' in response
