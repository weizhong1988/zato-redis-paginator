Django-like Redis pagination for Python
---------------------------------------

Except for the \__init\__ method, this is 100% API compatible with Django's own pagination
but works with Redis instead of SQL databases.

Supports lists, sorted sets or ranges of sorted sets between min/max scores.

Working with lists
==================

The code below establishes a connection, creates a list and splits it into pages.

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


More information
================

Originally part of Zato - ESB, SOA and cloud integrations in Python - https://zato.io
