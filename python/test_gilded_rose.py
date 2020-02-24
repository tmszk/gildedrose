# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose
from items import create_item, QualityDeltaProcessingType


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [create_item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual("foo", items[0].name)

    def test_increase_quality(self):
        items = [create_item("foo", 10, 20)]
        items[0].QUALITY_DELTA_PROCESSING_TYPE = QualityDeltaProcessingType.add
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(21, items[0].quality)

    def test_decrease_quality(self):
        items = [create_item("foo", 10, 20)]
        items[0].quality_delta_type = QualityDeltaProcessingType.subtract
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(19, items[0].quality)

    def test_decrease_quality_once_expired(self):
        items = [create_item("foo", 0, 20)]
        items[0].quality_delta_type = QualityDeltaProcessingType.subtract
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(18, items[0].quality)

    def test_decrease_sell_in(self):
        items = [create_item("foo", 10, 20)]
        items[0].quality_delta_type = QualityDeltaProcessingType.subtract
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(9, items[0].sell_in)

    def test_min_quality(self):
        items = [create_item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(0, items[0].quality)

    def test_max_quality(self):
        items = [create_item("Aged Brie", 0, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(50, items[0].quality)

    def test_sulfuras_no_updates(self):
        items = [create_item("Sulfuras, Hand of Ragnaros", 10, 15)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(10, items[0].sell_in)
        self.assertEqual(15, items[0].quality)

    def test_backstages_quality_deltas(self):
        items = [
            create_item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
            create_item("Backstage passes to a TAFKAL80ETC concert", 10, 20),
            create_item("Backstage passes to a TAFKAL80ETC concert", 5, 20),
            create_item("Backstage passes to a TAFKAL80ETC concert", 0, 20)
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(21, items[0].quality)
        self.assertEqual(22, items[1].quality)
        self.assertEqual(23, items[2].quality)
        self.assertEqual(0, items[3].quality)

    def test_conjured_quality_delta(self):
        items = [create_item("Conjured Mana Cake", 10, 15)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(13, items[0].quality)





if __name__ == '__main__':
    unittest.main()
