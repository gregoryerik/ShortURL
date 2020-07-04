# ShortURL
URL to ShortURL using Flask and MongoDB

## This program will not run without the hidden folder and hidden JSON file

Create a hidden folder (in the main dir) with 'hidden-json.json' file inside.

Template for file:
```
  {
    "database-precursor": "mongodb+srv://",
    "database-suffix": "@****-*****.azure.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE",
    "database-username": "********",
    "database-password": "********",
    "code-length": 4
}
```
This requires a MONGODB database in Atlas
