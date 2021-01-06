import os
from decouple import config
# os.environ['LeMedicinMongo'] = "mongodb+srv://swarnabha:sddb@cluster0.yxfcm.mongodb.net/MIC-Silicon?retryWrites=true&w=majority"
# os.environ['secretLeMedicin'] = "hello_mic"

print(config('LeMedicinMongo'))