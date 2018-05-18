# Radarr Agent for Plex

MOVIES_URL = "{}/api/movie"

RE_STRIP_YEAR = Regex('( \(\d{4}\))$')

####################################################################################################
def Start():

	pass

####################################################################################################
def GetApiData(url):

	if not Prefs['radarr_api_key']:
		Log("Enter your Radarr API key in the agent's preferences")
		return None

	try:
		data = HTTP.Request(url, headers={"X-Api-Key": Prefs['radarr_api_key']}).content
		return data
	except:
		Log("Error requesting URL {}".format(url))
		return None

####################################################################################################
class RadarrAgent(Agent.Movies):

	name = 'Radarr'
	languages = [Locale.Language.English]
	primary_provider = True
	accepts_from = ['com.plexapp.agents.localmedia']
	contributes_to = [
		'com.plexapp.agents.imdb',
		'com.plexapp.agents.themoviedb'
	]

	def search(self, results, media, lang, manual):

		if media.primary_agent in ['com.plexapp.agents.imdb', 'com.plexapp.agents.themoviedb']:

			results.Append(MetadataSearchResult(
				id = media.primary_metadata.id,
				score = 100
			))

		else:

			radarr_movies = MOVIES_URL.format(Prefs['radarr_url'].rstrip('/'))
			json = GetApiData(radarr_movies)

			if not json:
				return None

			json_obj = JSON.ObjectFromString(json)

			for movie in json_obj:

				scanner_title = RE_STRIP_YEAR.sub("", media.name).lower()
				api_title = RE_STRIP_YEAR.sub("", movie['title']).replace('-', ' ').lower()

				if scanner_title != api_title:
					continue

				if media.year and int(media.year) > 1900 and int(media.year) == movie['year']:
					score = 100
				else:
					score = 90

				results.Append(MetadataSearchResult(
					id = movie['imdbId'],
					name = movie['title'],
					year = movie['year'],
					score = score,
					lang = lang
				))

	def update(self, metadata, media, lang):

		radarr_movies = MOVIES_URL.format(Prefs['radarr_url'].rstrip('/'))
		json = GetApiData(radarr_movies)

		if not json:
			return None

		json_movies = JSON.ObjectFromString(json)

		for movie in json_movies:

			if metadata.id != movie['imdbId'] and metadata.id != str(movie['tmdbId']):
				continue

			# Start adding metadata
			metadata.title = movie['title']
			metadata.year = movie['year']
			metadata.originally_available_at = Datetime.ParseDate(movie['inCinemas']).date()
			metadata.summary = movie['overview']
			metadata.duration = movie['runtime'] * 60 * 1000
			metadata.studio = movie['studio']

			metadata.genres.clear()
			for genre in movie['genres']:
				metadata.genres.add(genre)

			valid_names = list()

			for image in movie['images']:

				image_url = "{}/api/MediaCover/{}".format(Prefs['radarr_url'].rstrip('/'), image['url'].split('/MediaCover/')[-1])
				valid_names.append(image_url)

				if image['coverType'] == "poster":
					metadata.posters[image_url] = Proxy.Media(GetApiData(image_url))
				elif image['coverType'] == "banner":
					metadata.banners[image_url] = Proxy.Media(GetApiData(image_url))

			metadata.posters.validate_keys(valid_names)
			metadata.banners.validate_keys(valid_names)

			break
