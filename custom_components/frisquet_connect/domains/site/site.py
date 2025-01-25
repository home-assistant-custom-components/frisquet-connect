from datetime import datetime
from typing import List
from custom_components.frisquet_connect.domains.model_base import ModelBase
from custom_components.frisquet_connect.domains.site.alarm import Alarm
from custom_components.frisquet_connect.domains.site.product import Product
from custom_components.frisquet_connect.domains.site.site_detail import SiteDetail
from custom_components.frisquet_connect.domains.site.utils import (
    convert_api_temperature_to_float,
    convert_from_epoch_to_datetime,
)
from custom_components.frisquet_connect.domains.site.water_heater import WaterHeater
from custom_components.frisquet_connect.domains.site.zone import Zone


class Site(ModelBase):
    _agi: str
    _produit: Product
    _identifiant_chaudiere: str
    _nom: str
    _date_derniere_remontee: str
    _detail: SiteDetail
    _external_temperature: int
    _water_heater: WaterHeater
    _zones: List[Zone]
    _alarms: List[Alarm]

    def __init__(self, response_json: dict):
        super().__init__(response_json)
        if "carac_site" in response_json:
            self._detail = SiteDetail(response_json["carac_site"])
        if "ecs" in response_json:
            self._water_heater = SiteDetail(response_json["ecs"])
        if "environnement" in response_json:
            self._external_temperature = response_json["environnement"]["T_EXT"]
        if "zones" in response_json:
            self._zones = []
            for zone in response_json["zones"]:
                self._zones.append(Zone(zone))
        if "alarmes" in response_json:
            self._alarms = []
            for alarm in response_json["alarmes"]:
                self._alarms.append(Alarm(alarm))

    @property
    def product(self) -> Product:
        return self._produit

    @property
    def serial_number(self) -> str:
        return self._agi

    @property
    def name(self) -> str:
        return self._nom

    @property
    def site_id(self) -> str:
        return self._identifiant_chaudiere

    @property
    def last_updated(self) -> datetime:
        return convert_from_epoch_to_datetime(self._date_derniere_remontee)

    @property
    def external_temperature(self) -> int:
        return convert_api_temperature_to_float(self._external_temperature)

    @property
    def detail(self) -> SiteDetail:
        return self.detail

    @property
    def water_heater(self) -> WaterHeater:
        return self.water_heater

    @property
    def zones(self) -> List[Zone]:
        return self.zones

    @property
    def alarms(self) -> List[Alarm]:
        return self.alarms

    def get_zone_by_label_id(self, zone_label_id: int) -> Zone:
        for zone in self.zones:
            if zone.label_id == zone_label_id:
                return zone
        return None
