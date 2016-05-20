from app import db

class Product(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    sku = db.Column(db.String(64))
    loyality_programm = db.Column(db.Boolean)
    free_shipping = db.Column(db.Boolean)
    image_url = db.Column(db.String(128))
    product_title = db.Column(db.String(128))
    price = db.Column(db.Float)
    pricespecial = db.Column(db.Float)

    def __repr__(self):
        return '<Product %r>' % (self.sku)