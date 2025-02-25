from core.knowledge import Knowledge

knowledge = Knowledge("test",query_ns=2)
# knowledge.upsert(
#     [
#         {
#             "document": "my name is jack, i am 32, i live in beijing, my job is an engineer",
#             "metadata": {
#                 "name": "jack",
#                 "age": 32,
#                 "city": "beijing",
#                 "job": "engineer",
#             },
#             "id": "id1",
#         },
#         {
#             "document": "i like play basketball and video game",
#             "metadata": {"sport": "basketball", "game": "video game"},
#             "id": "id2",
#         },{
#             "document":"my wife's name is miya, she is an accountant",
#             "metadata":{"wifename":"miya","wifejob":"accountant"},
#             "id":"id3"
#         }
#     ]
# )

# knowledge.destory()

result=knowledge.query("what deos her do?")

knowledge_content = "\n".join(f"{i+1}. {item}" for i, item in enumerate(result["documents"][0]))

print(knowledge_content)