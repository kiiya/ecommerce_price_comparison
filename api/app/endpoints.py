from app import Resource, api, reqparse, requests
import json

parser = reqparse.RequestParser()
parser.add_argument('q', location='args')


class ProductList(Resource):
    def get(self):
        url = 'http://localhost:9200/api_index-2017-03/_search'
        query = {
            "query": {
                "match_all": {}
            },
            "size": 2000
        }

        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        products = []
        for hit in data['hits']['hits']:
            product = hit['_source']
            product['id'] = hit['_id']
            products.append(product)
        return products

api.add_resource(ProductList, '/products')


class Search(Resource):
    def get(self):
        query_string = parser.parse_args()
        url = 'http://localhost:9200/api_index-2017-03/_search'
        print query_string
        query = {
            "query": {
                "multi_match": {
                    "fields": ["product_name", "product_url"],
                    "query": query_string['q'],
                    "type": "cross_fields",
                    "use_dis_max": False
                }
            },
            "size": 2000
        }
        print query
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        products = []
        for hit in data['hits']['hits']:
            product = hit['_source']
            product['id'] = hit['_id']
            products.append(product)
        return products

api.add_resource(Search, '/search')
