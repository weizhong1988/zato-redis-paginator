Django-like Redis pagination for Python
---------------------------------------

Except for the \__init\__ method, this is 100% API compatible with Django's own pagination
but works with Redis instead of SQL databases.

Supported data types:

- lists
- sorted sets
- ranges of sorted sets between min/max scores

The first two don't do it but the last one needs to fetch an entire results between
min and max score to calculate the pages. This is because ZREVRANGEBYSCORE doesn't
have any means to obtain the number of results that would've been returned without
actually returning them. 

Working with lists
==================

Establishes a connection, creates a list and splits it into pages.

```python
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
```

Working with sorted sets
========================

Establishes a connection, creates a sorted set and splits it into pages.

```python
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
```

Working with sorted sets and min/max scores
===========================================

Establishes a connection, creates a sorted set and splits it into pages while
including only these member that are between min and max scores.

```python
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
```

Changelog
=========

* Aug 11, 2013 - Initial 1.0 release

License
=======
BSD 3-clause license, see LICENSE.txt for terms and conditions.

More information
================

Originally part of Zato - ESB, SOA and cloud integrations in Python - https://zato.io/docs/
