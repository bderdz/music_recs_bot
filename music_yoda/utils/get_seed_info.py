def get_seed_info(genres: list[str] = None, artists: list[dict] = None, tracks: list[dict] = None):
    seed_info: str = "Your chosen seeds:"

    if genres:
        seed_info += "\nGenres:\n"
        for i, genre in enumerate(genres):
            seed_info += f"{i + 1}. {genre}\n"

    if artists:
        seed_info += "\nArtists:\n"
        for i, artist in enumerate(artists):
            seed_info += f"{i + 1}. {artist["name"]}\n"

    if tracks:
        seed_info += "\nTracks:\n"
        for i, tracks in enumerate(tracks):
            seed_info += f"{i + 1}. {tracks["name"]}\n"

    return seed_info
