from blue_objects.objects import unique_object

from blue_objects.mysql.cache.functions import read, write


def test_mysql_cache_write_read():
    keyword = unique_object()

    assert write(keyword, "this,that")

    keyword_as_read = read(keyword)

    assert keyword_as_read == keyword
