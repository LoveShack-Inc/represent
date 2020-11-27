import logging

def iterate_through_paged_query(query_callable, page_size):
    """
        For misc workflows, it's sometimes desirable to stream thru a large result set for a given
        query, perform some operation, and write the result to the database. The most straightforward
        way to do this, would be to iterate over the result set in the sqlite cursor object, and then
        write to the db with another connection. This causes a problem though, because sqlite will
        throw if you try to perform a write operation, while there is still a read operation open.
        We can get around that by making all of our SELECT queries pageable, and then page thru them.
        That ensures that a read operation will always be closed by the time that the caller gets the
    """
    more_records = True
    current = 0
    page_size = 1
    while more_records:
        logging.info(f"Getting page {current} for query: '{query_callable.__name__}'")
        for i in query_callable(page_size, current):
            yield i

        # page
        current += 1
        if not query_callable(page_size, current):
            more_records = False
