from http.server import HTTPServer, BaseHTTPRequestHandler
from pprint import pprint 

# 1.	Метод принимает идентификатор geonameid и возвращает информацию о городе.
# 2.	Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией. 
# 3.	Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах, а также дополнительно: 
#           какой из них расположен севернее и одинаковая ли у них временная зона 
#           (когда несколько городов имеют одно и то же название, разрешать неоднозначность выбирая город с большим населением;
#               если население совпадает, брать первый попавшийся)

class GeoNames(BaseHTTPRequestHandler):

    # def do_GET(self):
    #     self.send_response(200)
    #     self.send_header('content-type', 'text/html')
    #     self.end_headers()



    #МЕТОД 1
    def get_str(self) -> list:
        file_name = 'test.txt'
        cities = []
        data = {}
        info_list = [
            "geonameid",
            "name",
            "asciiname",
            "alternatenames",
            "latitude",
            "longitude",
            "feature class",
            "feature code",
            "country code",
            "cc2",
            "admin1 code",
            "admin2 code",
            "admin3 code",
            "admin4 code",
            "population",
            "elevation",
            "dem",
            "timezone",
            "modification date"
        ]

        with open(file_name, encoding="utf-8") as file:
            for line in file:
                line = line.split('\t')
                data = dict(zip(info_list, line))
                cities.append(data)
        
        return cities
                


    def get_city_info_geonameid(self, geonameid: int) ->dict:
        for city in cities:
            if city['geonameid'] == str(geonameid):
                return city 


    #МЕТОД 2 отображение на странице кол-ва городов  
    def get_page_and_count(self, page: int, count):
        start = page*count
        end = page*count + count
        return cities[start:end]


    def cities_list(self):
        cities_list = {}
        for i,city in enumerate(cities,1):
            k,v = i,city['name']
            cities_list[k] = v
        return cities_list


         
    #МЕТОД 3 ДОДЕЛАТЬ 


    #3.	Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах, 
    # а также дополнительно: какой из них расположен севернее и одинаковая ли у них временная зона 
    # (когда несколько городов имеют одно и то же название, разрешать неоднозначность выбирая город с большим населением;
    #  если население совпадает, брать первый попавшийся)

    # принимать на русском 
    def get_two_cities_inf0(self, city_1: str, city_2: str) -> dict:

        key_ind1 = self.get_index(city_1)
        key_ind2 = self.get_index(city_2)

        two_cities_dict = {
            '1':cities[key_ind1 - 1],
            '2':cities[key_ind2 - 1],
        }
        # pprint(two_cities_dict,  sort_dicts=False)
        
        # if city_1 in cities['name']:
        #     print(True) 
        # else:
        #     print(False)
        return two_cities_dict



    def get_index(seif, city: dict) ->dict:

        key_list = list(cities_list.keys())
        val_list = list(cities_list.values())
        position = val_list.index(city)
        return key_list[position]


# Рефакторинг 
    def north_cities(self, city_dict: dict) ->dict:

        l1:float = city_dict["1"]["latitude"]
        l2:float = city_dict["2"]["latitude"]

        if l1 > l2:
            return city_dict["1"]
        else:
            return city_dict["2"]

        # timezone

    def same_timezone(self, city_dict:dict) -> dict:

        if city_dict["1"]['timezone'] == city_dict["2"]['timezone']:
            return {"Timezone is:" "True"}
        else:
            # Вернуть различие 
            return {"Timezone is:" "False"}
            




            
        # population
    def _get_population_from_city_line(self, city:dict) ->int:
    # Возвращает количество жителей города
        return int(city["1"]["population"])





    def do_GET(self):
        
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()



def runserver(server_class=HTTPServer, handler_class=GeoNames):
    server_address = ('127.0.0.1', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()







if __name__ == '__main__':
    
    GEONAMEID = 451747
    CITY_NAME_1 = 'Zyabrikovo'
    CITY_NAME_2 = 'Znamenka'

    runserver()
    
    run = GeoNames()


    cities = run.get_str()
    geoname = run.get_city_info_geonameid(GEONAMEID)
    cities_list = run.cities_list()
    two_cities = run.get_two_cities_inf0(CITY_NAME_1, CITY_NAME_2)
    north = run.north_cities(two_cities)
    run.same_timezone(two_cities)
    population = run._get_population_from_city_line(two_cities)




    

