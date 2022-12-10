from app import app, db
from app.models import User, Offer, Category


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Offer': Offer, 'Category': Category}

if __name__=="__main__":
    app.app_context().push()
    db.create_all()
app.run(debug=True)