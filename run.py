from langbridge import create_app

app = create_app()
app.app_context().push()
app.run(debug=True)
