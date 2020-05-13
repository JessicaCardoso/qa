import pipeline

from flask import Flask, request
from flask_restx import Api, Resource, fields

import os

flask_app = Flask(__name__)
app = Api(
    app=flask_app,
    version="0.0.1",
    title="IQA IMDb",
    description="Permite a consulta de informações sobre a base de dados do IMDb.",
)

name_space = app.namespace(
    "iqa-imdb", description="Realiza consultas na base do IMDb."
)

@name_space.route("/perform_search")
class MainClass(Resource):
    @app.doc(
        responses={
            200: "OK",
            400: "Invalid Argument",
            500: "Mapping Key Error",
        },
        params={"q": "campo referente a pergunta desejada."},
    )
    def get(self):
        return pipeline.search(request.args.get("q"))


if __name__ == "__main__":
    if os.getenv("MODE") ==  "prod":
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(debug=True)
