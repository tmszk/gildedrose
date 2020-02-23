from original.gilded_rose import Item
from enum import Enum, auto


def create_item(name, sell_in, quality):

    if name == "Aged Brie":
        return Brie(name, sell_in, quality)
    elif name == "Sulfuras, Hand of Ragnaros":
        return Sulfuras(name, sell_in, quality)
    elif name == "Backstage passes to a TAFKAL80ETC concert":
        return Backstage(name, sell_in, quality)
    elif name == "Conjured Mana Cake":
        return Conjured(name, sell_in, quality)
    else:
        return DefaultItem(name, sell_in, quality)


class QualityDeltaType(Enum):  # Values not needed
    add = auto()
    subtract = auto()


class DefaultItem(Item):

    MINIMUM_QUALITY = 0
    MAXIMUM_QUALITY = 50

    QUALITY_DELTA_PROCESSING_TYPE = QualityDeltaType.subtract
    DEFAULT_QUALITY_DELTA = 1
    DELTA_MULTIPLICATION_ONCE_EXPIRED = 2

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)

    def update_items(self):
        self.update_sell_in()
        self.update_quality()

    def update_sell_in(self):

        self.sell_in -= 1

    def update_quality(self):

        quality_delta = self.calculate_quality_delta()

        if self.QUALITY_DELTA_PROCESSING_TYPE == QualityDeltaType.add:
            self.quality += quality_delta
            self.check_quality_limits(min, self.MAXIMUM_QUALITY)
        elif self.QUALITY_DELTA_PROCESSING_TYPE == QualityDeltaType.subtract:
            self.quality -= quality_delta
            self.check_quality_limits(max, self.MINIMUM_QUALITY)
        else:
            raise Exception(f"'{self.quality_delta_type}' is unrecognized as delta processing type for quality")

    def calculate_quality_delta(self):

        quality_delta = self.DEFAULT_QUALITY_DELTA

        if self.sell_in < 0:
            quality_delta *= self.DELTA_MULTIPLICATION_ONCE_EXPIRED

        return quality_delta

    def check_quality_limits(self, func, limit):

        self.quality = func(self.quality, limit)


class Brie(DefaultItem):

    QUALITY_DELTA_PROCESSING_TYPE = QualityDeltaType.add

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)


class Sulfuras(DefaultItem):
    def update_sell_in(self):
        pass

    def update_quality(self):
        pass


class Backstage(DefaultItem):

    QUALITY_DELTA_PROCESSING_TYPE = QualityDeltaType.add

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)

    def update_quality(self):

        if self.sell_in < 0:
            self.quality = 0
        else:
            super().update_quality()

    def calculate_quality_delta(self):

        if 0 <= self.sell_in <= 5:
            quality_delta = 3
        elif 5 < self.sell_in <= 10:
            quality_delta = 2
        elif self.sell_in < 0:
            quality_delta = 0
        else:
            quality_delta = self.DEFAULT_QUALITY_DELTA

        return quality_delta


class Conjured(DefaultItem):

    QUALITY_DELTA_PROCESSING_TYPE = QualityDeltaType.subtract
    DEFAULT_QUALITY_DELTA = 2

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)
