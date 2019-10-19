import vgmdb

def get_lang(obj):
	if 'ja-latn' in obj: return obj['ja-latn']
	elif 'Romaji' in obj: return obj['Romaji']
	elif 'en' in obj: return obj['en']
	elif 'English' in obj: return obj['English']
	elif 'ja' in obj: return obj['ja']
	elif 'Japanese' in obj: return obj['Japanese']
	else: return None

def search_albums(results, media, lang):
    query = media.album
    if query is None:
        query = media.name
    result = vgmdb.search_albums(query)

    if result is None:
        return

    s = 100
    for album in result:
        results.Append(MetadataSearchResult(
            id = album['link'].replace('album/', ''),
            name = get_lang(album['titles']),
            year = album['release_date'][0:4],
            score = s,
            lang = lang
        ))
        s = s - 1

def search_artists(results, media, lang):
    query = media.artist
    if query is None:
        query = media.name
    result = vgmdb.search_artists(query)

    if result is None:
        return

    s = 100
    for artist in result:
        results.Append(MetadataSearchResult(
            id = artist['link'].replace('artist/', ''),
            name = get_lang(artist['names']),
            score = s,
            lang = lang
        ))
        s = s - 1
