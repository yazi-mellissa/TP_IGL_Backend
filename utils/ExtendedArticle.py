from utils import get_file_path
from utils.Date import Date
from grobid_client_python.grobid_client.grobid_client import GrobidClient
from bs4 import BeautifulSoup
import os
import string

class ExtendedArticle():

    ID : int
    Titre : str
    Resume : str 
    Texte : str
    Link : str
    Date_pub : Date or str
    _Soup: BeautifulSoup

    Auteurs : list[(str, str, (str, str))] = []
    References : list[str] = []
    Mots_Cles : list[str] = []

    def __init__(self, data : bytes):

        file = open("./data/articles/current/current.pdf",'wb')
        file.write(data)
        file.close()
        client = GrobidClient(config_path="./config.json")
        client.process("processFulltextDocument", "./data/articles/current/", consolidate_citations=True, tei_coordinates=True, force=True)
        print("hh1")
        self.set_data()
        print("hh2")
        os.remove("./data/articles/current/current.pdf")
        os.remove("./data/articles/current/current.grobid.tei.xml")

    
    def set_id(self, ID : int) -> None:
        self.ID = ID
        
    def _elem_to_text(self, elem, default=""):
        if elem:
            return elem.getText()
        else:
            return default
        
    def _read_tei(self):
        with open("./data/articles/current/current.grobid.tei.xml", 'r', encoding="utf-8") as tei:
            self._Soup = BeautifulSoup(tei, "lxml")
    
    def _get_title(self):
        return self._Soup.title.getText()
    
    def _get_abstract(self):
        return self._Soup.abstract.getText(separator=' ', strip=True)
    
    def _get_text(self):
        divs_text = []
        for div in self._Soup.body.find_all("div"):
            if not div.get("type"):
                div_text = div.get_text(separator='\n\n', strip=True)
                divs_text.append(div_text)
        plain_text = " ".join(divs_text)
        return plain_text
    
    def _get_auteurs(self):
        authors_in_header = self._Soup.analytic.find_all('author')
        print(authors_in_header)
        result = []
        for author in authors_in_header:
            persname = author.persname
            if not persname:
                continue

            firstname = self._elem_to_text(persname.find("forename", type="first"))
            middlename = self._elem_to_text(persname.find("forename", type="middle"))
            surname = self._elem_to_text(persname.surname)
            institution_name = "university"
            institution_address = "unknown"
            if author.affiliation:
                institution_name = self._elem_to_text(author.affiliation.orgname)
                institution_address = self._elem_to_text(author.affiliation.address.addrline)

            name = [var for var in [firstname, middlename, surname] if var]
            author = (" ".join(name), (".".join(name)+"@"+institution_name.replace(" ","")).lower()+".edu", (institution_name, institution_address))
            result.append(author)
            print(author)
        return result
    
    def _get_mots_cles(self):
        keywords = self._Soup.keywords.find_all('term')
        result = []
        for keyword in keywords:
            term = self._elem_to_text(keyword)
            if term: 
                printable = set(string.printable)
                term = ''.join(filter(lambda x: x in printable, term))
                result.append(term)
        return result
    
    def _get_references(self):
        monogr_in_references = self._Soup.back.find_all('monogr')
        result = []
        for monogr in monogr_in_references:
            title = monogr.title
            if not title:
                continue
            reference = self._elem_to_text(title)
            result.append(reference)
    
        result = [var for var in result if var]
        return result
    
    def set_data(self) -> None:
        self._read_tei()
        self.Titre = self._get_title()
        self.Resume = self._get_abstract()
        self.Texte = self._get_text()
        self.Date_pub = Date.today()
        self.Auteurs = self._get_auteurs()
        self.Mots_Cles = self._get_mots_cles()
        self.References = self._get_references()

    def get_date(self) -> str:
        return self.Date_pub.get_date()

    # def save_pdf(self, data) -> None:
    #     self.Link = get_file_path(self.ID)
    #     file = open(self.Link,'wb')
    #     file.close()