The main flask python file is the entry point of this web application.
It is installed with the required packages and the has different routes.

1)@app.route('/')
Renders the home.html file.

2)@app.route('/next')
Renders the visualizations.html with datasets.Here the location of the trained json files is given as path. 

3)@app.route('/available')
Renders the available.html file whuich has the details of available models that can be used for exploring and gives
general details about the user interactive features in visualizations.html.

4)@app.route("/dimRed", methods=["POST"])
Renders the selected dataset by the user. Based on the selection either values from 3ts,5ts,10ts,20ts are rendered.  

5)@app.route('/comparison')
Renders the comparison.html with datasets.Here the location of the trained json files is given as path.

6)@app.route("/comparing", methods=["POST"])
Renders the selected dataset by the user for comaprison. Based on the selection either values from 3ts,5ts,10ts,20ts are rendered.

7)@app.route('/zerohidden')
Renders the zerohidden.html with datasets.Here the location of the trained json files is given as path.

8)@app.route('/overall')
Renders the parallelplot.html.Here the overall combination of hyperparameter values with the error values are rendered.

9)@app.route('/errortable')
Renders the RMSE.html. Here the table of overall combination of hyperparameter values with the error values are rendered.