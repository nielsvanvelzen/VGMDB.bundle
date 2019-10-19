from datetime import datetime
from vgmdb import get_album, get_artist

def get_lang(obj):
    if 'ja-latn' in obj: return obj['ja-latn']
    elif 'Romaji' in obj: return obj['Romaji']
    elif 'en' in obj: return obj['en']
    elif 'English' in obj: return obj['English']
    elif 'ja' in obj: return obj['ja']
    elif 'Japanese' in obj: return obj['Japanese']
    else: return None

def update_album(metadata, media, force):
    result = get_album(metadata.id)

    metadata.genres = result['categories']
    metadata.collections = map(lambda p: get_lang(p['names']), result['products'])
    metadata.rating = float(result['rating'])
    metadata.original_title = str(result['name'])
    metadata.title = get_lang(result['names'])
    metadata.summary = result['notes']
    metadata.studio = get_lang(result['publisher']['names'])

    split = map(lambda s: int(s), result['release_date'].split('-'))
    release_date = datetime(split[0], split[1], split[2])
    metadata.originally_available_at = release_date

    get_poster(metadata, result['picture_small'], result['picture_full'])
    for poster in result['covers']:
        if poster['full'] != result['picture_full']:
            get_poster(metadata, poster['thumb'], poster['full'])


    trackNum = 0
    for disc in result['discs']:
        for track in disc['tracks']:
            trackNum = trackNum + 1

            metadata.tracks[trackNum].name = get_lang(track['names'])

    Log.Info(metadata)

def update_artist(metadata, media, force):
    result = get_artist(metadata.id)

    metadata.rating = float(result['info']['Weighted album rating'].replace('/10', ''))
    metadata.title = result['name']
    metadata.summary = result['notes']

    if result['picture_full'] is not None:
        get_poster(metadata, result['picture_small'], result['picture_full'])

def get_poster(metadata, thumb, full):
    try:
        thumbnail = Proxy.Preview(HTTP.Request(
            thumb, immediate = True
        ).content)
        metadata.posters[full] = thumbnail
    except:
        Log.Error('Error loading poster')
