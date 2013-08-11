# -*- coding: utf-8 -*-

"""
Copyright (C) 2013 Dariusz Suchojad <dsuch at zato.io>

Licensed under the BSD 3-clause license, see LICENSE.txt for terms and conditions.
"""

# stdlib
from random import randint
from unittest import TestCase
from uuid import uuid4

# Zato
from zato import redis_paginator

dummy = uuid4().hex
dummy_default_args = [dummy] * 3

def get_rand_int():
    return randint(0, 100)

class DummyRedisConn(object):
    def __init__(self):
        self.lrange_args = None
        self.llen_args = None
        self.zrangebyscore_args = None
        self.zrange_args = None
        self.zcard_args = None
        
    def lrange(self, key, start, stop):
        self.lrange_args = key, start, stop
        
    def llen(self, key):
        self.llen_args = key
        
    def zrange(self, key, start, stop):
        self.zrange_args = key, start, stop
        
    def zcard(self, key):
        self.zcard_args = key
        
    def zrangebyscore(self, key, score_min, score_max):
        self.zrangebyscore_args = key, score_min, score_max
        return []

class PaginatorTestCase(TestCase):
    def test_source_type_not_given(self):
        self.assertRaises(KeyError, redis_paginator.RedisPaginator, *dummy_default_args)

    def test_source_type_mapping(self):
        self.assertTrue(redis_paginator._source_type_object_list['list'] is redis_paginator._ListObjectList)
        self.assertTrue(redis_paginator._source_type_object_list['zset'] is redis_paginator._ZSetObjectList)
        
    def test_use_zrangebyscore(self):
        p1 = redis_paginator.ZSetPaginator(*dummy_default_args)
        self.assertEqual(p1.object_list._use_zrangebyscore, False)
        
        p2 = redis_paginator.ZSetPaginator(*dummy_default_args, score_min=uuid4().hex)
        self.assertEqual(p2.object_list._use_zrangebyscore, True)
        
        p3 = redis_paginator.ZSetPaginator(*dummy_default_args, score_max=uuid4().hex)
        self.assertEqual(p3.object_list._use_zrangebyscore, True)
        
        p4 = redis_paginator.ZSetPaginator(*dummy_default_args, score_min=uuid4().hex, score_max=uuid4().hex)
        self.assertEqual(p4.object_list._use_zrangebyscore, True)
        
    def test_choose_object_list_type(self):
        p1 = redis_paginator.ListPaginator(*dummy_default_args)
        self.assertTrue(p1.object_list, redis_paginator._ListObjectList)
        
        p2 = redis_paginator.ZSetPaginator(*dummy_default_args)
        self.assertTrue(p2.object_list, redis_paginator._ZSetObjectList)
        
    def test_api_called_list(self):
        conn, key = DummyRedisConn(), uuid4().hex
        start, stop = get_rand_int(), get_rand_int()
        
        object_list = redis_paginator._ListObjectList(conn, key)
        object_list[start:stop]
        object_list.count()
        
        self.assertEqual(conn.lrange_args, (key, start, stop-1))
        self.assertEqual(conn.llen_args, key)
        
    def test_api_called_zset(self):
        conn, key = DummyRedisConn(), uuid4().hex
        score_min, score_max = '-inf', '+inf'
        start, stop = get_rand_int(), get_rand_int()
        
        object_list = redis_paginator._ZSetObjectList(conn, key, score_min, score_max)
        object_list[start:stop]
        object_list.count()
        
        self.assertEqual(conn.zrange_args, (key, start, stop-1))
        self.assertEqual(conn.zcard_args, key)
        
    def test_api_called_zset_with_score(self):
        conn, key = DummyRedisConn(), uuid4().hex
        score_min, score_max = get_rand_int(), get_rand_int()
        start, stop = get_rand_int(), get_rand_int()
        
        object_list = redis_paginator._ZSetObjectList(conn, key, score_min, score_max)
        object_list[start:stop]
        object_list.count()
        
        self.assertEqual(conn.zrangebyscore_args, (key, score_min, score_max))
