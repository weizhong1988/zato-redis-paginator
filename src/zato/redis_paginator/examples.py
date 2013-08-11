# -*- coding: utf-8 -*-

"""
Copyright (C) 2013 Dariusz Suchojad <dsuch at zato.io>

Licensed under the BSD 3-clause license, see LICENSE.txt for terms and conditions.
"""

#
# * Django-like Redis pagination - a drop-in replacement except for the __init__ method.
#
# * Originally part of Zato - ESB, SOA and cloud integrations in Python https://zato.io
#

# Examples below are self-contained and ready to copy'n'paste 

def list_example():
    """ Example list pagination.
    """
    from uuid import uuid4
    from redis import StrictRedis
    from zato.redis_paginator import ListPaginator
    
    conn = StrictRedis()
    key = 'paginator:{}'.format(uuid4().hex)
    
    for x in range(1, 18):
        conn.rpush(key, x)
        
    p = ListPaginator(conn, key, 6)
    
    print(p.count)      # 17
    print(p.num_pages)  # 3
    print(p.page_range) # [1, 2, 3]
    
    page = p.page(3)
    print(page)             # <Page 3 of 3>
    print(page.object_list) # ['13', '14', '15', '16', '17']
        
    conn.delete(key)
    
def zset_example():
    """ Example sorted set pagination.
    """
    from uuid import uuid4
    from redis import StrictRedis
    from zato.redis_paginator import ZSetPaginator
    
    conn = StrictRedis()
    key = 'paginator:{}'.format(uuid4().hex)
    
    # 97-114 is 'a' to 'r' in ASCII
    for x in range(1, 18):
        conn.zadd(key, x, chr(96 + x))
        
    p = ZSetPaginator(conn, key, 6)
    
    print(p.count)      # 17
    print(p.num_pages)  # 3
    print(p.page_range) # [1, 2, 3]
    
    page = p.page(3)
    print(page)             # <Page 3 of 3>
    print(page.object_list) # ['m', 'n', 'o', 'p', 'q']
        
    conn.delete(key)
    
def zset_score_min_max_example():
    """ Example sorted set with min/max score pagination.
    """
    from uuid import uuid4
    from redis import StrictRedis
    from zato.redis_paginator import ZSetPaginator
    
    conn = StrictRedis()
    key = 'paginator:{}'.format(uuid4().hex)
    
    # 97-114 is 'a' to 'r' in ASCII
    for x in range(1, 18):
        conn.zadd(key, x, chr(96 + x))
        
    p = ZSetPaginator(conn, key, 2, score_min=5, score_max=13)
    
    print(p.count)      # 9
    print(p.num_pages)  # 5
    print(p.page_range) # [1, 2, 3, 4, 5]
    
    page = p.page(3)
    print(page)             # <Page 3 of 5>
    print(page.object_list) # ['i', 'j']
        
    conn.delete(key)
