import datetime

class Date():
    Jour : int
    Mois : int
    Annee : int

    def __init__(self, Jour : int = None, Mois : int = None, Annee : int = None, date : str = None):
        if (date is not None):
            temp = date.split("-")
            self.Jour = int(temp[2])
            self.Mois = int(temp[1])
            self.Annee = int(temp[0])
        if (date is None):
            self.Jour = Jour
            self.Mois = Mois
            self.Annee = Annee
    
    def get_date(self) -> str:
        return str(self.Annee) + "-" + str(self.Mois) + "-" + str(self.Jour)
    
    def is_before(self, date):
        if self.Annee < date.Annee:
            return True
        elif self.Annee == date.Annee:
            if self.Mois < date.Mois:
                return True
            elif self.Mois == date.Mois:
                if self.Jour < date.Jour:
                    return True
        return False
    
    def is_before_today(self):
        today = Date(date=datetime.date.today().strftime("%Y-%m-%d"))
        return self.is_before(today)
    
    def date_after_days(self, days):
        date = datetime.date(year=self.Annee, month=self.Mois, day=self.Jour)
        date += datetime.timedelta(days=days)
        return Date(date=date.strftime("%Y-%m-%d"))
    
    def today():
        return Date(date=datetime.date.today().strftime("%Y-%m-%d"))