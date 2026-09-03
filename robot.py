from dataclasses import dataclass
from math import radians, cos
from config import LINKS, PAYLOAD


@dataclass
class Link:
    name: str
    length: float
    mass: float
    com: float


class Robot:
    def __init__(self, links=None, payload=None):
        source = links or LINKS
        self.links = [Link(**item) for item in source]
        self.payload = payload or PAYLOAD

    @property
    def axes(self):
        return len(self.links)

    def total_mass(self):
        return sum(link.mass for link in self.links) + self.payload["mass"]

    def horizontal_distance(self, link_index, angles_deg):
        """Horizontal reach contribution of a point on a planar chain."""
        distance = 0.0
        cumulative_angle = 0.0
        for i in range(link_index + 1):
            cumulative_angle += angles_deg[i]
            length = self.links[i].com if i == link_index else self.links[i].length
            distance += length * cos(radians(cumulative_angle))
        return distance
