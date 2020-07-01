import json 
import os

from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('<KEY>')
discovery = DiscoveryV1(
    version='2018-08-01',
    authenticator=authenticator)

discovery.set_service_url('<URL>')

environments = discovery.list_environments().get_result()

macmod_docs_environment_id = '<ID>'

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
