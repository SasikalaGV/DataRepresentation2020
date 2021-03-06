from flask import Flask, url_for, request, redirect, abort, jsonify, json
from StockDAO import stockDAO
from bs4 import BeautifulSoup
#import requests




app  = Flask(__name__, static_url_path='', static_folder='.')
#jsglue = JSGlue(app)

##################################################################
# GetAll()
#curl "http://127.0.0.1:5000/stock"
@app.route('/stock')
def getAll():
    #print("in getall")
    results = stockDAO.getAll()
    return jsonify(results)
##################################################################
#curl "http://127.0.0.1:5000/stock/2"
@app.route('/stock/<int:id>')
def findById(id):
    foundStock = stockDAO.findByID(id)

    return jsonify(foundStock)


##################################################################
# create()
#
# Action = Create a stock item in the DB
# curl -i -H "Content-Type:application/json" -X POST -d "{\"Category\": \"Stationary\", \"Name\":\"Handbook\", \"Quantity\":10 }" "http://127.0.0.1:5000/Stock"

@app.route('/stock', methods=['POST'])
def create():
    #return "in create"

    if not request.json:
        abort(400)
    
    # id - Auto increment 
    Stock = {
        "Category": request.json['Category'],
        "Name": request.json['Name'],
        "Quantity": request.json['Quantity'] 
    }

    # Make the tuple for DB
    #values = (Stock['Category'], Stock['Name'], Stock['Quantity'])
    values = (request.json['Category'], request.json['Name'], request.json['Quantity'])
    newId = stockDAO.create(values)
    Stock['id'] = newId

    return jsonify(Stock)

##################################################################
# update(id)
#
# Action = Update stock in DB by ID
# curl -i -H "Content-Type:application/json" -X PUT -d "{\"quantity\":120}" "http://127.0.0.1:5000/stock/1"
# curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Name\":\"some\",\"Quantity\":123}" http://127.0.0.1:5000/stock/1

@app.route('/stock/<int:id>', methods=['PUT'])
def update(id):
    #return "in update by ID for id "+ str(id)

    # Find the stock in DB table
    foundStock = stockDAO.findByID(id)

    if not foundStock:
        #return "That id does not exist in the database table"
        abort(404)

    if not request.json:
        abort(400)

    # Get what was passed up
    reqJson = request.json
    if 'Quantity' in reqJson and type(reqJson['Quantity']) is not int:
        abort(400)
   
    
    # Info to update    
    if 'Category' in reqJson:
        foundStock['Category'] = reqJson['Category']
    if 'Name' in reqJson:
        foundStock['Name'] = reqJson['Name']
    if 'Quantity' in reqJson:
        foundStock['Quantity'] = reqJson['Quantity']

    # Make the tuple for DB
    values = (foundStock['Name'],foundStock['Quantity'], foundStock['id'])
    
    # Do the update on DB
    stockDAO.update(values)
    return jsonify(foundStock)

##################################################################

# Action = Delete stock in DB by ID
# curl -X DELETE "http://127.0.0.1:5000/stock/1"

@app.route('/stock/<int:id>', methods=['DELETE'])
def delete(id):
    #return "in delete by ID for id "+ str(id)

    # Check if id exists in stock table in DB
    foundStock = stockDAO.findByID(id)
    if not foundStock:
        #return "That id does not exist in the database table"
        abort(404)

    # Remove stock from DB by id
    stockDAO.delete(id)
    return jsonify({"done":True})

#################################################################


if __name__ == "__main__":
    print("in if")
    app.run(debug=True)