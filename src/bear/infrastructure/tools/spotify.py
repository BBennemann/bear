import spotipy
from spotipy.oauth2 import SpotifyOAuth

from bear.config import config
from langchain_core.tools import tool

class SpotifyService():
    def __init__(self, client_id: str, client_secret:str, redirect_uri: str, favorite_device: str = "TV Sala"):
        scope = "user-read-playback-state user-modify-playback-state"
        auth_manager = SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

        self.client = spotipy.Spotify(auth_manager=auth_manager)
        self.favorite_device = favorite_device

    def _get_device_id(self):
        devices = self.client.devices().get("devices", [])
            
        if not devices:
            return None
    
        if self.favorite_device:
            for d in devices:
                if self.favorite_device.lower() in d["name"].lower():
                    return d["id"]
    
        for d in devices:
            if d["is_active"]:
                return d["id"]
    
        return devices[0]["id"]

    def play_track(self, music_name: str) -> dict:
        try:
            device_id = self._get_device_id()
                
            if not device_id:
                return {"Error": "No active spotify device found. Please open spotify"}

            result = self.client.search(q=music_name, limit=1, type="track")
            
            tracks = result["tracks"]["items"]
            
            if not tracks:
                return {"Error": "Music not found"}
    
            music_uri = tracks[0]["uri"]
            official_name = tracks[0]["name"]
            artist = tracks[0]["artists"][0]["name"]
    
            self.client.start_playback(uris=[music_uri], device_id=device_id)
            music = f"Playing now: {official_name} by {artist}"
        except Exception as e:
            return {"Error": f"Failed to get music from spotify: {e}"}
    
        return {"response": music}
    
spotify_service = SpotifyService(config.SPOTIPY_CLIENT_ID, config.SPOTIPY_CLIENT_SECRET, config.SPOTIPY_REDIRECT_URI, config.FAVORITE_DEVICE)

@tool
def play_music(music_name: str) -> dict:

    """Searches for a song on Spotify and immediately starts playing it on the user's active Spotify device.

    Use this tool whenever the user asks to play, listen to, or put on a specific song or tracks.
    Do not use this tool for pausing, skipping, or adjusting volume.
    Always present the music as a radio host

    Args:
        music_name (str): The search query for the tracks to play. Include both the song title
            and the artist's name whenever available to ensure the most accurate match
            (e.g., "Bohemian Rhapsody Queen" or "Maine Noah Kahan").

    Returns:
        dict: A Dict message containing the official tracks name and artist currently playing,
            or an error message if no matching tracks or active Spotify device was found.
    """

    return spotify_service.play_track(music_name)
    