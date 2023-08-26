from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import cohere
from postProcess import get_file_content
from pathlib import Path

uri = ""
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

dbname = client['Insurance']
chunks_collection = dbname['Chunks']

api_key = ''
co = cohere.Client(api_key)



#Uploading to Mongo
def upload_file(filename):
    contents = get_file_content(filename)

    chunks_collection.insert_many(contents)

    chunks_doc = chunks_collection.find({})

    # for doc in chunks_doc:
    #     context = doc['Context']
    #     doc['embedding'] = co.embed(texts=[context], model='small').embeddings[0]
    #     chunks_collection.replace_one({'_id': doc['_id']}, doc)


folder_path = Path('/Users/angky/Cornell/Hackathon/insurance_plans')

# Iterate through all files in the folder
for file_path in folder_path.iterdir():
    if file_path.is_file():
        foldername = '/Users/angky/Cornell/Hackathon/insurance_plans'
        filename = foldername + '/' +  str(file_path.name)
        print("Processing " + filename)
        upload_file(filename)





#Query
# query = "What is the maximum number of visit"
# query_embedding = co.embed(texts=[query], model='small').embeddings[0]

# results = chunks_collection.aggregate([
#     {
#         '$search': {
#             "index": "ChunksSemanticSearch",
#             "knnBeta": {
#                 "vector": query_embedding,
#                 "k": 4,
#                 "path": "embedding"}
#         }
#     }
# ])


# for document in results:
#     print(document['context'])


#Writing




# content = []
# with open('sample.txt', 'r') as file:
#     for line in file:
#         content.append({"context":line})

# chunks_collection.insert_many(content)



# api_key = 'g8xGyFiK2FetipLLvAxAQayM2tYUojPUrWNXmADt'
# co = cohere.Client(api_key)
# phrase = "Today is great"
# co.embed([phrase]).embeddings

