import unittest
import requests
from utils.ExtendedArticle import ExtendedArticle
from utils.Date import Date

class TestExtendedArticle(unittest.TestCase):
    def test_set_data(self):
        link = "https://apis2ee.etic-club.com/PDFs/Article_02.pdf"
        data = requests.api.get(url=link)
        article = ExtendedArticle(data.content)

        self.assertIsNotNone(article.Titre)
        self.assertIsNotNone(article.Resume)
        self.assertIsNotNone(article.Texte)
        self.assertIsNotNone(article.Date_pub)
        self.assertIsInstance(article.Date_pub, Date)
        self.assertIsInstance(article.Auteurs, list)
        self.assertIsInstance(article.References, list)
        self.assertIsInstance(article.Mots_Cles, list)

if __name__ == '__main__':
    unittest.main()