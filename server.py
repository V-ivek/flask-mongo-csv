from flask import *
import pymongo
import pandas as pd

app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        print(request.files)
        f = request.files['file']
        mongoClient = pymongo.MongoClient('localhost', 27017)
        mongoDb = mongoClient['mphase']
        collection = 'stock'
        db = mongoDb[collection]
        data = pd.read_csv(f)
        data_json = json.loads(data.to_json(orient='records'))
        names_key = {'% Deli. Qty to Traded Qty': '% Deli Qty to Traded Qty',
                     'No. of Trades': 'No of Trades',
                     'No.of Shares': 'No of Shares',
                     'Total Turnover (Rs.)': 'Total Turnover (Rs)'
                     }
        for row in data_json:
            for k, v in names_key.items():
                for old_name in row:
                     if k == old_name:
                        row[v] = row.pop(old_name)
        db.remove()
        db.insert(data_json)
        return render_template("success.html")
  
if __name__ == '__main__':  
    app.run(debug = True)  
