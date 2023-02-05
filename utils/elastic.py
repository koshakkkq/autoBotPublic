from elasticsearch import AsyncElasticsearch
import asyncio
es = AsyncElasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
index = 'main'

async def create_index():
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        },
        "mappings": {
            'properties': {
                'categoryId': {
                    'type': 'integer',
                },
                "text": {
                    'type': 'text',
                    'analyzer': 'russian'
                }
            }
        }
    }
    try:
        if await es.indices.exists(index=index):
            await es.indices.delete(index=index)
        await es.indices.create(index=index, body=settings)
        return None
    except Exception as e:
        return e



async def insert_category_to_es(doc):
    es_data = []
    es_data.append({'index':{'_index':index}})
    es_data.append(doc)
    await es.bulk(body=es_data)

async def find_by_text_es(text):
    ids = await es.search(index=index, query={'match':{'text':text}})
    print(ids)
async def kek():
    await create_index()
    await insert_category_to_es({'categoryId':123, 'text':'лучшая шиномонтаж'})
    await insert_category_to_es({'categoryId':1234, 'text':'шины'})
    await insert_category_to_es({'categoryId':1235, 'text':'шина'})
    await find_by_text_es('Что делать если проколол шину?')

asyncio.run(kek())