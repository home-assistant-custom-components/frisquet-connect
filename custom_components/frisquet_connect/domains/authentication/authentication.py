from typing import List

from custom_components.frisquet_connect.domains.site.site_light import SiteLight


class Authentication:
    _token: str
    _sites: List[SiteLight]

    def __init__(self, response_json: dict):
        if response_json is None:
            raise ValueError("The response JSON must not be None")

        for key, value in response_json.items():
            attr_name = f"_{key}"
            if key == "utilisateur":
                if "sites" in response_json:
                    self._sites = []
                    for site in response_json["sites"]:
                        self._sites.append(SiteLight(site))
            elif hasattr(self, attr_name):
                setattr(self, attr_name, value)

    @property
    def token(self) -> str:
        return self._token

    @property
    def sites(self) -> List[SiteLight]:
        return self._sites
