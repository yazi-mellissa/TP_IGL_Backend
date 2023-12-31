from utils import get_file_path
from utils.Date import Date

class ExtendedArticle():
    
    ID : int
    Titre : str
    Resume : str
    Texte : str
    Link : str
    Date_pub : Date

    Auteurs : list[(str, str, (str, str))] = []
    References : list[str] = []
    Mots_Cles : list[str] = []

    def __init__(self, Link : str):
        self.Link = Link
        self.set_data()
    
    def set_id(self, ID : int) -> None:
        self.ID = ID

    def set_data(self) -> None:
        # Samy for data extraction here
        self.Titre = ""
        self.Resume = ""
        self.Texte = ""
        self.date_pub = Date(date="01/01/1970")
        self.Auteurs = []
        self.Mots_Cles = []
        self.References = []
        pass

    def indexer(self) -> None:
        # Hiba for elastic search indexation here
        pass

    def get_date(self) -> str:
        return self.Date_pub.get_date()

    def save_pdf(self, data) -> None:
        self.Link = get_file_path(self.ID)
        file = open(self.Link,'wb')
        file.write(data)
        file.close()