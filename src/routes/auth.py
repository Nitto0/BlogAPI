from src import create_app

app = create_app()


@app.route("")
def register():
    pass
