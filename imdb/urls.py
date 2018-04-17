def title_to_url(title_id):
    if title_id is None:
        raise TypeError
    return "https://www.imdb.com/title/{0}/".format(title_id)

def name_to_url(name_id):
    if name_id is None:
        raise TypeError
    return "https://www.imdb.com/name/{0}/".format(name_id)