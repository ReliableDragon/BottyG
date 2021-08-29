import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('bottyg-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection(u'users').document(u'57331')
doc_ref.set({
    u'name': u'test',
    u'id': u'57331',
    u'rocketry_love': 0,
})

data = db.collection(u'users').document(u'57331').get()
if not data.exists:
  print("Data does not exist!")
else:
  print("Rocketry love: {}".format(data.to_dict()['rocketry_love']))
