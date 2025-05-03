class ENDPOINTS:
    BASE_ENDPOINT = "https://www.fewandfar.co.uk/api/techtest/v1/"

    # url and methods
    GET_SUPPORTERS = f"{BASE_ENDPOINT}supporters"#GET
    GET_DONATIONS = f"{BASE_ENDPOINT}donations"#GET
    POST_DONATIONS_EXPORTS = f"{BASE_ENDPOINT}donations_exports" #POST
    GET_DONATION_EXPORT = f"{BASE_ENDPOINT}donations_exports/{{export_id}}" #GET

    @classmethod
    def get_donations(cls, page=1):
        return f"{cls.GET_DONATIONS}?page={page}"

    @classmethod
    def get_supporters(cls, page=1):
        return f"{cls.GET_SUPPORTERS}?page={page}"
    
    @classmethod
    def get_donation_exports(cls, export_id):
        return cls.GET_DONATION_EXPORT.format(export_id=export_id)
    
    @classmethod
    def post_donation_exports(cls):
        return cls.POST_DONATIONS_EXPORTS

