from dotenv import load_dotenv
import requests
from pprint import pprint
import pandas as pd
import os

load_dotenv()

token = os.environ['BEARER_TOKEN']

requestHeaders = {
  "Authorization": "Bearer " + token
}

# Merge all photos
def mergeAllPhotos():
  currentPage = 1
  params = {
    "page": currentPage
  }

  getAllUrl = 'https://amor-client.com/api/get_origin_photo/subpackage/111'
  try:
    getAllR = requests.get(url=getAllUrl, params=params, headers=requestHeaders)
    getAll = getAllR.json()
    lastPage = getAll['last_page']
    photos=getAll['data']
    pprint(params)
  except Exception as e:
    print("Error getAll: ")
    pprint(e)
  currentPage = 2
  for i in range(lastPage):
    if currentPage >= lastPage:
      break
    currentPage = i + 2
    params = {
      "page": currentPage
    }
    pprint(params)
    getAllR = requests.get(url=getAllUrl, params=params, headers=requestHeaders)
    getAll = getAllR.json()
    photos=photos + getAll['data']
  return photos

# Unselect all photos
def unselectAllPhotos(photos):
  basename=''
  deleteUrl= 'https://amor-client.com/api/drive/delete_selected_origin_photo/' + basename
  selectedPhotos=[]
  for photo in photos:
    if photo['is_selected'] == 1:
      selectedPhotos.append(photo)
  for selectedPhoto in selectedPhotos:
    basename=selectedPhoto['basename']
    try:
      deleteUrl= 'https://amor-client.com/api/drive/delete_selected_origin_photo/' + basename
      deleteR = requests.get(url=deleteUrl, headers=requestHeaders)
      pprint(deleteR.json())
    except Exception as e:
      print("Error unselectAllPhotos at : ")
      pprint(selectedPhoto)
      pprint(e)

# Load and select photos from CSV
def loadCsvAndSelectPhotos(csv):
  df = pd.read_csv(csv)
  preselectedPhotos = df.to_dict()['name'].values()
  basenameParam=''
  selectUrl = 'https://amor-client.com/api/drive/selected_photo?subpackageId=111' + basenameParam
  for filename in preselectedPhotos:
    photo = next((photo for photo in photos if photo['filename'] == filename), None)
    if photo == None:
      continue
    basenameParam = '&basename=' + photo['basename']
    try:
      selectUrl = 'https://amor-client.com/api/drive/selected_photo?subpackageId=111' + basenameParam
      selectR = requests.get(url=selectUrl, headers=requestHeaders)
      pprint(selectR.json())
    except Exception as e:
      print("Error loadCsvAndSelectPhotos at : ")
      pprint(photo)
      print(filename)
      pprint(e)
    

print("Merging all photos ...\n")
photos = mergeAllPhotos()
print("\nPhotos are merged.\n")

print("Running unselectAllPhotos ...\n")
unselectAllPhotos(photos)
print("\nUnselect all photos done.\n")
    
print("Load csv and select photos ...\n")
loadCsvAndSelectPhotos(r"photos.csv")
print("\nDONE.\n")