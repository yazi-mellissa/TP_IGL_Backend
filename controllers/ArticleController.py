from typing import List
from fastapi import status
from elasticsearch_connect import ElasticsearchConnection
from datetime import date, datetime
from models.Article import Article
from utils.HTTPResponse import HTTPResponse
from utils.ExtendedArticle import ExtendedArticle
from utils.Creds import ElasticsearchCreds
##Elasticsearch_connection
index_name="articles"

class SafeArticle():
    ID : int
    Titre : str
    Resume : str 
    Texte : str
    Date_pub : str
    Auteurs : list[(str, str, (str, str))] = []
    References : list[str] = []
    Mots_Cles : list[str] = []

    def __init__(self, id, titre, resume, texte, date_pub, auteurs, references, mots_cles):
        self.ID = id
        self.Titre = titre
        self.Resume = resume
        self.Texte = texte
        self.Date_pub = date_pub
        self.Auteurs = auteurs
        self.References = references
        self.Mots_Cles = mots_cles

class ArticleController():
    
    def index_article(article: SafeArticle):
        try:
            print(ElasticsearchCreds)
            es = ElasticsearchConnection().getEngine()
            print("wsalt hna")
            es.index(index=index_name, body=article.__dict__)
            print("mwsaltch")
            return "ok"
            # raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article indexed successfully")
        except Exception as e:
            
            error_message = f"Error indexing Article: {str(e)}"
            raise HTTPResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)

    def delete_indexed_article(Article_Id):
        es = ElasticsearchConnection().getEngine()
        if es.exists(index=index_name, id=Article_Id):
            es.delete(index=index_name, id=Article_Id)
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article  deleted successfully from elasticsearch")
        else:
            raise HTTPResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No article found with this id in elasticsearch")   
        
    def get_all_indexed_articles():
        es = ElasticsearchConnection().getEngine()
        search_query = {"query": {"match_all": {}}}
        result = es.search(index=index_name, body=search_query)
        articles = result['hits']['hits']
        return articles
    
    # Elasticsearch query to search in the title, keywords, authors, and full text
    def search_articles(query_terms):
        query = {
            "query": {
                "multi_match": {
                    "query": query_terms,
                    "fields": ["Titre", "Mots_Cles", "Auteurs", "Texte", "References", "Resume"]
                }
            }
        }
    
        try:
            es = ElasticsearchConnection().getEngine()
            response = es.search(index=index_name, body=query)
            hits = response.get("hits", {}).get("hits", [])
            articles = []

            for hit in hits:
                ##source = hit.get("_source", {}) //hadi ki nkono nhawso 3la les info ta3 l'article (wech kayn f _source)
                articles.append(hit)
            #sort the search results in reverse chronological order
            sorted_articles = sorted(articles, 
                                     key=lambda x: datetime.strptime(x["_source"].get("Date_pub", ""), "%Y-%m-%d").date(), 
                                     reverse=True)
            return sorted_articles
        except Exception as e:
            print(f"Error searching articles: {str(e)}")
            raise

    # Filtres 
    def apply_filters(
        self,
        articles,
        Mots_Cles: List[str] = None,
        Auteurs: List[str] = None,
        Institutions: List[str] = None,
        start_date: date = None,
        end_date: date = None,
    ):
        filtered_articles = [
            article for article in articles
            if (
                (not Mots_Cles or any(Mots_Cle.lower() in map(str.lower, article["_source"].get("Mots_Cles", [])) for Mots_Cle in Mots_Cles)) and
                (not Auteurs or any(Auteur.lower() in map(str.lower, article["_source"].get("Auteurs", [])) for Auteur in Auteurs)) and
                (not Institutions or any(Institution.lower() in map(str.lower, article["_source"].get("Institutions", [])) for Institution in Institutions)) and
                (not start_date or datetime.strptime(article["_source"].get("Date_Publication"), "%Y-%m-%d").date() >= start_date) and
                (not end_date or datetime.strptime(article["_source"].get("Date_Publication"), "%Y-%m-%d").date() <= end_date)
            )
        ]

        return filtered_articles

    # The search and filtre function 
    def search_and_filter_articles(
        self,
        query_terms: str,
        Mots_Cles: List[str] = None,
        Auteurs: List[str] = None,
        Institutions: List[str] = None,
        start_date: date = None,
        end_date: date = None,
    ):
        search_results = self.search_articles(query_terms)
        filtered_results = self.apply_filters(
            self,
            search_results,
            Mots_Cles=Mots_Cles,
            Auteurs=Auteurs,
            Institutions=Institutions,
            start_date=start_date,
            end_date=end_date,
        )
        return filtered_results