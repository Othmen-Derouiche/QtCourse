from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

if __name__ == '__main__':

    benchling = Benchling(url="https://my.benchling.com", auth_method=ApiKeyAuth("api_key"))
    #print(benchling)
    example_entities = benchling.dna_sequences.list()
    for page in example_entities:
        for sequence in page:
            print(f"name: {sequence.name}\nid:{sequence.id}\n")