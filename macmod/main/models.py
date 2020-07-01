from macmod import db
from flask_mongoengine.wtf import model_form

class Products(db.Document):
    meta = {'collection': 'Products'}
    _id = db.StringField(primary_key=True)
    name = db.StringField(required=True)
    label = db.StringField(required=True)

class Nabvar(db.Document):
    meta = {'collection': 'Navbar'}
    _id = db.StringField(primary_key=True)
    title = db.StringField(required=True)
    component = db.StringField(required=False)
    active = db.BooleanField(required=True)
    isDropDown = db.BooleanField(required=True)
    DropdownItems = db.ListField()

class ProductCatalog(db.Document):
    meta = {'collection': 'productcatalog'}
    _id = db.ObjectIdField()
    name = db.StringField(required=True)
    description = db.StringField(required=False)
    brand = db.StringField(required=True)
    product_type = db.StringField(required=True)
    bonded_phase = db.StringField(required=False)
    particle_size = db.StringField(required=False)
    column_length_mm = db.StringField(required=False)
    column_id_mm = db.StringField(required=False)
    pore_size_a = db.StringField(required=False)
    base_price = db.StringField(required=True)
    internal_id = db.StringField(required=True)

class ProductLogos(db.Document):
    meta = {'collection': 'productlogos'}
    _id = db.StringField(primary_key=True)
    brand = db.StringField(required=True)
    logourl = db.StringField(required=True)
    path = db.StringField(requred=True)
    brandphases = db.ListField()
    layout = db.StringField()

class ProductPhases(db.Document):
    meta = {'collection': 'productphases'}
    _id = db.StringField(primary_key=True)
    phasename = db.StringField(required=True)
    phasename = db.StringField('phasename', required=True)
    Phase_Number = db.IntField()

class PhasePages(db.Document):
    meta = {'collection': 'phasepages'}
    _id = db.ObjectIdField()

class PhaseImages(db.Document):
    meta = {'collection': 'phaseimages'}
    _id = db.StringField(primary_key=True)
    brand = db.StringField(required=True)
    phase = db.StringField(required=True)
    imageurl = db.StringField(required=True)

class Applications(db.Document):
    meta = {'collection' : 'applicationslist'}
    _id = db.StringField(required=True)
    title = db.StringField(required=True)

class ApplicationGuides(db.Document):
    meta = {'collection': 'fs.files'}
    _id = db.ObjectIdField(required=True)
    md5 = db.StringField()
    filename = db.StringField(required=True)
    metadata = db.ListField()
    chunkSize = db.IntField()
    length = db.IntField()
    uploadDate = db.DateTimeField()
    belongsTo = db.StringField()
    contentType = db.StringField()
    form = db.StringField()
    daterecorded = db.DateTimeField()
    year = db.IntField()

class Contacts(db.Document):
    meta = {'collection': 'contacts'}
    _id = db.ObjectIdField(required=True)
    contacttitle = db.StringField(required=True)
    contactname = db.StringField(required=True)
    contactphone = db.StringField(required=True)
    contactemail = db.StringField(required=True)
    contactthumbnail = db.StringField(required=True)
    teamlead = db.BooleanField(required=True)

class PostersPresentations(db.Document):
    meta = {'collection': 'PostersPresentations'}
    _id = db.ObjectIdField(required=True)
    conference = db.StringField(required=True)
    year = db.StringField(required=True)
    brand = db.ListField(required=True)
    industry = db.ListField(required=True)
    title = db.StringField(required=True)
    lc_mode = db.ListField()
    format = db.StringField()
    instrument_type = db.ListField()
    src = db.StringField()


class ProductTypes(db.Document):
    meta = {'collection': 'producttypes'}
    _id = db.ObjectIdField()
    producttype = db.StringField(required=True)

class Brands(db.Document):
    meta = {'collection': 'brands'}
    _id = db.ObjectIdField()
    brand = db.StringField(required=True)

class Phases(db.Document):
    meta = {'collection': 'phases'}
    _id = db.ObjectIdField()
    phase = db.StringField(required=True)

class ColumnLength(db.Document):
    meta = {'collection': 'columnlength'}
    _id = db.ObjectIdField()
    columnlength = db.StringField(required=True)
    columnlengthtype = db.StringField(required=True)

class ColumnIds(db.Document):
    meta = {'collection': 'columnids'}
    _id = db.ObjectIdField()
    columnid = db.StringField(required=True)
    columnidtype = db.StringField(required=True)

class ParticleSizes(db.Document):
    meta = {'collection': 'particlesizes'}
    _id = db.ObjectIdField()
    particlesize = db.StringField(required=True)

class PoreSizes(db.Document):
    meta = {'collection': 'poresizes'}
    _id = db.ObjectIdField()
    poresize = db.StringField(required=True)


class Orders(db.Document):
    meta = {'collection': 'orders'}
    _id = db.ObjectIdField()
    orderplaced = db.DateTimeField()
    companyname = db.StringField(required=True)
    companyaddress = db.StringField(required=True)
    city = db.StringField(required=True)
    state = db.StringField(required=True)
    zipcode = db.IntField()
    ccname = db.StringField(required=True)
    card = db.IntField()
    expiration = db.DateTimeField()
    ccv = db.IntField()
    subtotal = db.IntField()
    items = db.ListField()

class Notes(db.Document):
    meta = {'collection': 'Notes'}
    _id = db.ObjectIdField()
    number = db.StringField(required=True)
    title = db.StringField()
    brand = db.ListField()
    format_note = db.StringField()
    lc_mode = db.ListField()
    instrument_type = db.ListField()
    topic = db.ListField()
    industry = db.ListField()

class Webinar(db.Document):
    meta = {'collection': 'Webinar'}
    _id = db.ObjectIdField()
    title = db.StringField()
    brand = db.ListField()
    lc_mode = db.ListField()
    instrument_type = db.ListField()
    topic = db.ListField()
    industry = db.ListField()

class WhitePaper(db.Document):
    meta = {'collection': 'WhitePaper'}
    _id = db.ObjectIdField()
    title = db.StringField()
    brand = db.ListField()
    lc_mode = db.ListField()
    instrument_type = db.ListField()
    topic = db.ListField()
    industry = db.ListField()