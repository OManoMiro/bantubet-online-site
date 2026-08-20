import json
import unittest
import xml.etree.ElementTree as ElementTree
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAIS = ROOT / "rais"


class SiteSmokeTests(unittest.TestCase):
    def test_landing_has_seo_contract(self):
        html = (RAIS / "index.html").read_text(encoding="utf-8")
        for marker in (
            'name="description"',
            'rel="canonical"',
            'application/ld+json',
            'https://www.bantubetangola.com/',
        ):
            self.assertIn(marker, html)
        self.assertNotIn('href="#"', html)

    def test_blog_has_publisher_marker(self):
        blog = (RAIS / "blog.html").read_text(encoding="utf-8")
        self.assertIn('id="blog-posts"', blog)
        self.assertIn('rel="canonical"', blog)

    def test_crawling_files_are_valid(self):
        ElementTree.parse(RAIS / "sitemap.xml")
        robots = (RAIS / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://www.bantubetangola.com/sitemap.xml", robots)

    def test_vercel_routes_are_present(self):
        config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        redirects = config["redirects"]
        rewrites = config["rewrites"]
        self.assertTrue(any(item.get("permanent") and item.get("destination", "").startswith("https://www.bantubetangola.com") for item in redirects))
        destinations = {item["destination"] for item in rewrites}
        self.assertIn("/rais/index.html", destinations)
        self.assertIn("/rais/blog.html", destinations)
        self.assertIn("/rais/sitemap.xml", destinations)


if __name__ == "__main__":
    unittest.main()
