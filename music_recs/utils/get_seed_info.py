def get_seed_info(genres: list[str] = None, artists: list[dict] = None, tracks: list[dict] = None):
    seed_info: str = ""

    if genres:
        seed_info += "▫️ <b>Genres:</b>\n"
        for i, genre in enumerate(genres):
            seed_info += f"{i + 1}. {genre}\n"

    if artists:
        seed_info += "▫️ <b>Artists:</b>\n"
        for i, artist in enumerate(artists):
            seed_info += f"{i + 1}. {artist["name"]}\n"

    if tracks:
        seed_info += "▫️ <b>Tracks:</b>\n"
        for i, tracks in enumerate(tracks):
            seed_info += f"{i + 1}. {tracks["name"]}\n"

    return seed_info
