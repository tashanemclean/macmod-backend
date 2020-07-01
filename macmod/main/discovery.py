import json 
import os

from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('SmSeNMU__n3jThLMv60r10NGkmi7DStgaKAstabnCZVq')
discovery = DiscoveryV1(
    version='2018-08-01',
    authenticator=authenticator)

discovery.set_service_url('https://api.us-south.discovery.watson.cloud.ibm.com/instances/15f4fc3b-de49-4a10-96e5-cd7033a7373e')

environments = discovery.list_environments().get_result()

macmod_docs_environment_id = '91042ae5-ec41-4cf8-8dbe-45dbcd6b283b'

collections = discovery.list_collections(macmod_docs_environment_id).get_result()
macmod_collections = [x for x in collections['collections']]

configurations = discovery.list_configurations(
    environment_id=macmod_docs_environment_id).get_result()

def get_document_bullet_points(query):
    query_results = discovery.query(
        macmod_docs_environment_id,
        macmod_collections[0]['collection_id'],
        filter=(f'title:"{query}"'),
        return_fields='title').get_result()
    return query_results