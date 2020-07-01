import os
import bson
import json

from datetime import datetime, timedelta

from gridfs import GridFS
from gridfs.errors import NoFile

from mongoengine.connection import get_db

from flask import Blueprint, request, redirect, json, jsonify, make_response, send_file
from werkzeug import exceptions
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

from macmod import db
from .models import Orders
from .models import Nabvar, Products, ProductCatalog, ProductLogos, ProductPhases,Contacts,PostersPresentations
from .models import PhaseImages, Applications, ApplicationGuides, Notes, Webinar
from .models import Brands, Phases, ColumnLength, ProductTypes, ColumnIds, ParticleSizes, PoreSizes
from .models import PhasePages
from .discovery import get_document_bullet_points

main = Blueprint("main", __name__)
menu = Blueprint("menu", __name__, url_prefix='/menu')
shop = Blueprint("shop", __name__, url_prefix='/shop')

@main.route("/products/", methods=['GET', 'POST'])
@main.route("/products/<int:id>", methods=['GET', 'POST'])
def get_products(id=None):

    if id is None:
        results = json.dumps(Products.objects.all())
    else:
        results = json.dumps(Products.objects.filter(_id=id))

    return results, 200

@main.route("/products/add/", methods=['GET', 'POST'])
@jwt_required
def add_products():

    reqProducts = request.get_json()

    if reqProducts is None:
        return jsonify({'code': 999, 'message': 'no products, please check'}), 403
        
    result = []
    for reg in reqProducts:

        if reg['name'] is not None and reg['label'] is not None:
            
            new_id = str(Products.objects.count() + 1)
            product = Products()

            product._id     = new_id
            product.name    = reg['name']
            product.label   = reg['label']
                
            product.save()

            result.append(product._id)
        
    return jsonify({'data': result, 'code': 000, 'message': 'inserted'}), 200

@main.route("/products/update/", methods=['GET', 'POST'])
@jwt_required
def update_products():
    
    if request is None:
        return jsonify({'code': 999, 'message': 'no products, please check'}), 403
    
    reqProducts = request.get_json()
    result = []

    for reg in reqProducts:

        if reg['id'] is not None:
            product = Products.objects(_id=str(reg['id']))
            label = None
            name = None

            if 'name' in reg:
                if reg['name'] is not None:
                    product.update(name=reg['name'])

            if 'label' in reg:
                if reg['label'] is not None:
                    product.update(label=reg['label'])

            result.append(reg['id'])

    return jsonify({'data': result, 'code': 000, 'message': 'Updated'}), 200

@main.route("/products/delete/", methods=['GET', 'POST'])
@jwt_required
def delete_products():
    
    if request is None:
        return jsonify({'code': 999, 'message': 'no products, please check'}), 403
    
    reqProducts = request.get_json()
    result = []

    for reg in reqProducts:

        if reg['id'] is not None:
            product = Products.objects(_id=str(reg['id'])).delete()
            result.append(reg['id'])

    return jsonify({'data': result, 'code': 000, 'message': 'deleted'}), 200
    

###########################
## Product Catalog       ##
###########################

@main.route("/refresh/catalogs/", methods=['GET', 'POST'])
def refresh_product_catalog(id=None):

    products = ProductCatalog.objects.all()

    for product in products:
        
        brand = Brands.objects.filter(brand=product.brand)

        if brand:
            print("exists")
        else:
            newbrand = Brands()
            newbrand.brand = product.brand
            newbrand.save()

        phase = Phases.objects.filter(phase=product.bonded_phase)

        if phase:
            print("exists")
        else:
            newphase = Phases()
            newphase.phase = product.bonded_phase
            newphase.save()

        column_length = ColumnLength.objects.filter(columnlength=product.column_length_mm)

        if column_length:
            print("exists")
        else:
            newcolumn_length = ColumnLength()
            newcolumn_length.columnlength = product.column_length_mm
            newcolumn_length.columnlengthtype = 'mm'
            newcolumn_length.save()

        producttypes = ProductTypes.objects.filter(producttype=product.product_type)

        if producttypes:
            print("exists")
        else:
            newproducttype = ProductTypes()
            newproducttype.producttype = product.product_type
            newproducttype.save()

        columnid = ColumnIds.objects.filter(columnid=product.column_id_mm)

        if columnid:
            print("exists")
        else:
            newcolumnid = ColumnIds()
            newcolumnid.columnid = product.column_id_mm
            newcolumnid.columnidtype = 'mm'
            newcolumnid.save()

        particlesize = ParticleSizes.objects.filter(particlesize=product.particle_size)

        if particlesize:
            print("exists")
        else:
            newparticlesize = ParticleSizes()
            newparticlesize.particlesize = product.particle_size
            newparticlesize.save()

        poresize = PoreSizes.objects.filter(poresize=product.pore_size_a)

        if poresize:
            print("exists")
        else:
            newporesize = PoreSizes()
            newporesize.poresize = product.pore_size_a
            newporesize.save()

    return "results", 200

@main.route("/products/catalog/", methods=['GET', 'POST'])
def get_product_catalog():
    
    query = request.get_json()

    product = []
    allFilters = {
        "Brands" : [],
        "Phases": [],
        "ColumnLength": [],
        "ProductTypes": [],
        "ColumnIds": [],
        "ParticleSizes": [],
        "PoreSizes": []
    }

    if "filters" in query and len(query['filters']) > 0:

        params = {}
        filters = query['filters']

        if 'product' in filters: params['product_type'] = filters['product']
        if 'brand' in filters: params['brand'] = filters['brand']
        if 'phase' in filters: params['bonded_phase'] = filters['phase']
        if 'particle-size' in filters: params['particle_size'] = filters['particle-size']
        if 'pore-size' in filters: params['pore_size_a'] = filters['pore-size']
        if 'column-length' in filters: params['column_length_mm'] = filters['column-length']
        if 'column-id' in filters: params['column_id_mm'] = filters['column-id']

        # valid if user clicks buy now from product table page
        if 'Bonded Phase' in filters: params['bonded_phase'] = filters['Bonded Phase']
        # if 'Particle Size (µm)' in filters: params['particle_size'] = filters['Particle Size (µm)']
        if 'Pore Size (Å)' in filters: params['pore_size_a'] = str(filters['Pore Size (Å)'])

        products = ProductCatalog.objects(__raw__=params).limit(50)

        for prod in products:

            if prod.brand not in allFilters["Brands"]: allFilters["Brands"].append(prod.brand)
            if prod.bonded_phase not in allFilters["Phases"]: allFilters["Phases"].append(prod.bonded_phase)
            if prod.column_length_mm not in allFilters["ColumnLength"]: allFilters["ColumnLength"].append(prod.column_length_mm)
            if prod.product_type not in allFilters["ProductTypes"]: allFilters["ProductTypes"].append(prod.product_type)
            if prod.column_id_mm not in allFilters["ColumnIds"]: allFilters["ColumnIds"].append(prod.column_id_mm)
            if prod.particle_size not in allFilters["ParticleSizes"]: allFilters["ParticleSizes"].append(prod.particle_size)
            if prod.pore_size_a not in allFilters["PoreSizes"]: allFilters["PoreSizes"].append(prod.pore_size_a)

            product.append(prod)
        
    else:
        filters = []
        for i in Brands.objects.all().order_by('brand'): allFilters['Brands'].append(i.brand)
        for i in Phases.objects.all().order_by('phase'): allFilters['Phases'].append(i.phase)
        for i in ColumnLength.objects.all().scalar('columnlength').order_by('columnlength'): allFilters['ColumnLength'].append(i)
        for i in ProductTypes.objects.all().order_by('producttype'): allFilters['ProductTypes'].append(i.producttype)
        for i in ColumnIds.objects.all().scalar('columnid').order_by('columnid'): allFilters['ColumnIds'].append(i)
        for i in ParticleSizes.objects.all().order_by('particlesize'): allFilters['ParticleSizes'].append(i.particlesize)
        for i in PoreSizes.objects.all().order_by('poresize'): allFilters['PoreSizes'].append(i.poresize)

        products = ProductCatalog.objects.limit(50)

        for prod in products:
            product.append(prod)

    allFilters["SelectedFilters"] = filters

    return jsonify(products=product, filters=allFilters), 200

@main.route("/products/catalog/query", methods=['GET','POST'])
def get_products_query():

    query = request.get_json()
    if len(query) <=0:
        results = json.dumps(ProductCatalog.objects.limit(50))
    else:
        results = json.dumps(ProductCatalog.objects.filter(description__icontains=query['query']).limit(40))
    
    return results, 200

@main.route("/products/catalog/add/", methods=['GET', 'POST'])
@jwt_required
def add_product_catalog():

    reqProducts = request.get_json()

    if reqProducts is None:
        return jsonify({'code': 999, 'message': 'no products, please check'}), 403
        
    result = []
    for reg in reqProducts:

        if all(key in reg for key in ('name', 'description', 'brand', 'product_type', 'base_price',' internal_id')):
            product = ProductCatalog()

            product.name    = reg['name']
            product.description   = reg['description']
            product.brand   = reg['brand']
            product.product_type   = reg['product_type']
            product.bonded_phase   = reg['bonded_phase']
            product.particle_size   = reg['particle_size']
            product.column_length_mm   = reg['column_length_mm']
            product.column_id_mm   = reg['column_id_mm']
            product.pore_size_a   = reg['pore_size_a']
            product.base_price   = reg['base_price']
            product.internal_id   = reg['internal_id']
                
            product.save()

            result.append(product._id)
    
    if result == []:
        return jsonify({'code': 999, 'message': 'no values inserted, please check'}), 403
    return jsonify({'data': result, 'code': 000, 'message': 'inserted'}), 200

@main.route("/products/catalog/update/", methods=['GET', 'POST'])
@jwt_required
def update_product_catalog():
    
    if request is None:
        return jsonify({'code': 999, 'message': 'no product specified, please check'}), 403
    
    reqProducts = request.get_json()
    result = []

    for reg in reqProducts:

        if reg['id'] is not None:
            product = ProductCatalog.objects(_id=str(reg['id']))

        if reg['internal_id'] is not None and product is None:
            product = ProductCatalog.objects(internal_id=str(reg['internal_id']))

            if 'name' in reg:
                if reg['name'] is not None:
                    ProductCatalog.update(name=reg['name'])

            if 'description' in reg:
                if reg['description'] is not None:
                    ProductCatalog.update(description=reg['description'])

            if 'brand' in reg:
                if reg['brand'] is not None:
                    ProductCatalog.update(brand=reg['brand'])

            if 'product_type' in reg:
                if reg['product_type'] is not None:
                    ProductCatalog.update(product_type=reg['product_type'])

            if 'bonded_phase' in reg:
                if reg['bonded_phase'] is not None:
                    ProductCatalog.update(bonded_phase=reg['bonded_phase'])

            if 'particle_size' in reg:
                if reg['particle_size'] is not None:
                    ProductCatalog.update(particle_size=reg['particle_size'])

            if 'column_length_mm' in reg:
                if reg['column_length_mm'] is not None:
                    ProductCatalog.update(column_length_mm=reg['column_length_mm'])

            if 'column_id_mm' in reg:
                if reg['column_id_mm'] is not None:
                    ProductCatalog.update(column_id_mm=reg['column_id_mm'])

            if 'pore_size_a' in reg:
                if reg['pore_size_a'] is not None:
                    ProductCatalog.update(pore_size_a=reg['pore_size_a'])

            if 'base_price' in reg:
                if reg['base_price'] is not None:
                    ProductCatalog.update(base_price=reg['base_price'])

            result.append(reg['id'])

    return jsonify({'data': result, 'code': 000, 'message': 'Updated'}), 200

@main.route("/products/catalog/delete/", methods=['GET', 'POST'])
@jwt_required
def delete_product_in_catalog():
    
    if request is None:
        return jsonify({'code': 999, 'message': 'no products, please check'}), 403
    
    reqProducts = request.get_json()
    result = []

    for reg in reqProducts:

        if reg['id'] is not None:
            product = ProductCatalog.objects(_id=str(reg['id'])).delete()
            result.append(reg['id'])
        
        if reg['internal_id'] is not None:
            product = ProductCatalog.objects(internal_id=str(reg['internal_id'])).delete()
            result.append(reg['internal_id'])

    return jsonify({'data': result, 'code': 000, 'message': 'deleted'}), 200


###########################
## Product Logos       ##
###########################

@main.route('/productlogos', methods=['GET','POST'])
def get_product_logos():
    query = request.get_json()

    # if type doesnt exist then we get all products
    if "type" not in query:

        p = []
        products = ProductLogos.objects.order_by('brand').all()
        
        for prod in products:

            if prod['layout'] == query:
                p.append(prod)
                
        results = json.dumps(p)

        return results,200 

    p = []
    products = ProductLogos.objects.all()
    for prod in products:

        if not prod['brandphases']:
            continue

        if prod['brand'] == 'lc-mode':
            p.append(prod)
            break
        
        for brandphase in prod['brandphases']:

            if "layout" not in brandphase:
                continue

            if 'ace halo' in query['id']:

                if "productlayout" in brandphase:

                    if query['type'] in brandphase['productlayout']:
                        p.append(brandphase)
                continue

            if "productlayout" not in brandphase:
                if query['type'] in brandphase['layout']: 
                    p.append(prod)
                    break
                continue
            
            if query['type'] in brandphase['layout']:
                p.append(prod)
                break
    
    results = json.dumps(p)
    
    return results,200


###########################
## Product Phases     ##
###########################
@main.route('/productphases', methods=['GET','POST'])
def get_product_phases():
    query = request.get_json()

    if query == "ACE Semi-Prep and Prep":
        bullet_points = get_document_bullet_points("ACE Semi-Preparative and Preparative HPLC Columns")
    else:
        bullet_points = get_document_bullet_points(query)
 
    results = ProductPhases.objects(phasename__icontains=query).order_by('Phase Number').all()
 
    return {'results':json.dumps(results, sort_keys=False), 'bullet_points': bullet_points},200


@main.route('/productphases/phaseimage',methods=['GET','POST'])
def get_phase_image():
    query = request.get_json()
    results = []
    for a in query:
        results.append(PhaseImages.objects.filter(phase__icontains=a).limit(1))
    
    return {'results': results},200


###########################
## Phase Page Content  ##
###########################
@main.route('/phasepagecontent',methods=['POST'])
def phase_page_content():
    query = request.get_json()

    results = json.dumps(PhasePages.objects.filter(__raw__={"Phase Number": str(query['type']),"Bonded Phase": query['id']}).all())

    return results, 200


###########################
## Applications    ##
###########################

@main.route('/applications', methods=['GET','POST'])
def get_applications_pdf():
    results = json.dumps(Applications.objects.limit(10),sort_keys=False)

    return results,200

@main.route('/applicationguides', methods=['POST'])
@main.route('/applicationguides/<int:num>', methods=['POST'])
def get_application_guides(num=None):
    query = request.get_json()

    appguide = ApplicationGuides.objects.filter(belongsTo=query).limit(num)

    results = json.dumps(appguide, sort_keys=False)

    return results, 200

@main.route('/applicationguides/download/', methods=['GET','POST'])
@main.route('/applicationguides/download/<string:filename>', methods=['GET'])
@main.route('/applicationguides/download/<string:filename>/<string:belongsto>', methods=['GET'])
def get_application_guides_files(filename=None, belongsto=None):
    
    if request.method == 'POST':
        query = request.get_json()
        if 'filename' in query:
            filename = query['filename']
            belongsto=query['belongsTo']

    if filename is not None:

        try:

            if belongsto is not None:
                appguide = ApplicationGuides.objects.get(filename=filename, belongsTo=belongsto)
            else:
                appguide = ApplicationGuides.objects.get(filename=filename)

        except Exception as e:
            error = {
                "message": str(e), 
                "userMessage": "filename - '{}' or belongsTo - '{}' criteria doesn't exists". format(filename, belongsto)
            }
            return error, 404

        if appguide:
            dbConn = get_db()
            FS = GridFS(dbConn)

            try:
                file = FS.get(appguide._id)
                response = make_response(file.read())
                response.mimetype = file.content_type
                return response
            except NoFile:
                return {"message": "file can't find in the database. please check the name"}, 404
            except Exception as e:
                return {"message": str(e)}, 500
        else:
            return {"Error": "filename - {} doesn't exists.".format(filename)}, 403
    
    return {"Error": "filename and belongsTo are required"}, 403

@main.route('/applications/upload/', methods=['GET','POST'])
def upload_application_guides_files():
    
    if 'files' not in request.files:
        return {'message': 'Bad request. No File parameter.'}, 400

    result = []
    dbConn = get_db()
    FS = GridFS(dbConn)

    for f in request.files.getlist('files'):
        filename = secure_filename(f.filename)
        oid = FS.put(f, content_type=f.content_type, filename=f.filename, belongsTo="Applications", form="ACE Excel Applications")
        result.append({"filename": f.filename, "id": oid})
    
    return 'done', 200

#######################################
## Technical Notes & Knowledge Notes ##
#######################################

@main.route('/notes/', methods=['GET', 'POST'])
def get_notes():

    query = request.get_json()

    allNotes = []
    notesFilters = {
        "Number" : [],
        "Title": [],
        "Brand": [],
        "Format_Note": [],
        "Lc_Mode": [],
        "Instrument_Type": [],
        "Topic": [],
        "Industry": []
    }

    if 'filters' in query:

        params = {}
        filters = query['filters']

        if 'Number' in filters: params['number'] = filters['Number']
        if 'Brand' in filters: params['brand'] = filters['Brand']
        if 'Title' in filters: params['title'] = filters['Title']
        if 'Industry' in filters: params['industry'] = filters['Industry']
        if 'Instrument_Type' in filters: params['instrument_type'] = filters['Instrument_Type']
        if 'Lc_Mode' in filters: params['lc_mode'] = filters['Lc_Mode']
        if 'Format_Note' in filters: params['format_note'] = filters['Format_Note']
        if 'Topic' in filters: params['topic'] = filters['Topic']

        allNotes = Notes.objects(__raw__=params).all()
    else:
        filters = []
        allNotes = Notes.objects.all()

    for note in allNotes:
        notesFilters['Number'].append(note['number'])
        if note['title'] not in notesFilters['Title']:
            notesFilters['Title'].append(note['title'])
        if note['format_note'] not in notesFilters['Format_Note']:
            notesFilters['Format_Note'].append(note['format_note'])
        for i in note['brand']:
            if i not in notesFilters['Brand']:
                notesFilters['Brand'].append(i)
        for i in note['lc_mode']:
            if i not in notesFilters['Lc_Mode']:
                notesFilters['Lc_Mode'].append(i)
        for i in note['instrument_type']:
            if i not in notesFilters['Instrument_Type']:
                notesFilters['Instrument_Type'].append(i)
        for i in note['topic']:
            if i not in notesFilters['Topic']:
                notesFilters['Topic'].append(i)
        for i in note['industry']:
            if i not in notesFilters['Industry']:
                notesFilters['Industry'].append(i)

    notesFilters['SelectedFilters'] = filters

    results = json.dumps({'values': allNotes, 'filters': notesFilters}, sort_keys=False)

    return results, 200

@main.route('/webinar/', methods=['GET', 'POST'])
def get_webinars():

    query = request.get_json()

    allWebinar = []
    webinarsFilters = {
        "Title": [],
        "Brand": [],
        "Lc_Mode": [],
        "Instrument_Type": [],
        "Topic": [],
        "Industry": []
    }

    if 'filters' in query:

        params = {}
        filters = query['filters']

        if 'Brand' in filters: params['brand'] = filters['Brand']
        if 'Title' in filters: params['title'] = filters['Title']
        if 'Industry' in filters: params['industry'] = filters['Industry']
        if 'Instrument_Type' in filters: params['instrument_type'] = filters['Instrument_Type']
        if 'Lc_Mode' in filters: params['lc_mode'] = filters['Lc_Mode']
        if 'Topic' in filters: params['topic'] = filters['Topic']

        allWebinar = Webinar.objects(__raw__=params).all()
    else:
        filters = []
        allWebinar = Webinar.objects.all()

    for webinar in allWebinar:
        if webinar['title'] not in webinarsFilters['Title']:
            webinarsFilters['Title'].append(webinar['title'])
        for i in webinar['brand']:
            if i not in webinarsFilters['Brand']:
                webinarsFilters['Brand'].append(i)
        for i in webinar['lc_mode']:
            if i not in webinarsFilters['Lc_Mode']:
                webinarsFilters['Lc_Mode'].append(i)
        for i in webinar['instrument_type']:
            if i not in webinarsFilters['Instrument_Type']:
                webinarsFilters['Instrument_Type'].append(i)
        for i in webinar['topic']:
            if i not in webinarsFilters['Topic']:
                webinarsFilters['Topic'].append(i)
        for i in webinar['industry']:
            if i not in webinarsFilters['Industry']:
                webinarsFilters['Industry'].append(i)

    webinarsFilters['SelectedFilters'] = filters

    results = json.dumps({'values': allWebinar, 'filters': webinarsFilters}, sort_keys=False)

    return results, 200

@main.route('/whitepaper/', methods=['GET', 'POST'])
def get_whitepapers():

    query = request.get_json()

    allwhitepaper = []
    whitepapersFilters = {
        "Title": [],
        "Brand": [],
        "Lc_Mode": [],
        "Instrument_Type": [],
        "Topic": [],
        "Industry": []
    }

    if 'filters' in query:

        params = {}
        filters = query['filters']

        if 'Brand' in filters: params['brand'] = filters['Brand']
        if 'Title' in filters: params['title'] = filters['Title']
        if 'Industry' in filters: params['industry'] = filters['Industry']
        if 'Instrument_Type' in filters: params['instrument_type'] = filters['Instrument_Type']
        if 'Lc_Mode' in filters: params['lc_mode'] = filters['Lc_Mode']
        if 'Topic' in filters: params['topic'] = filters['Topic']

        allwhitepaper = WhitePaper.objects(__raw__=params).all()
    else:
        filters = []
        allwhitepaper = WhitePaper.objects.all()

    for whitepaper in allwhitepaper:
        if whitepaper['title'] not in whitepapersFilters['Title']:
            whitepapersFilters['Title'].append(whitepaper['title'])
        for i in whitepaper['brand']:
            if i not in whitepapersFilters['Brand']:
                whitepapersFilters['Brand'].append(i)
        for i in whitepaper['lc_mode']:
            if i not in whitepapersFilters['Lc_Mode']:
                whitepapersFilters['Lc_Mode'].append(i)
        for i in whitepaper['instrument_type']:
            if i not in whitepapersFilters['Instrument_Type']:
                whitepapersFilters['Instrument_Type'].append(i)
        for i in whitepaper['topic']:
            if i not in whitepapersFilters['Topic']:
                whitepapersFilters['Topic'].append(i)
        for i in whitepaper['industry']:
            if i not in whitepapersFilters['Industry']:
                whitepapersFilters['Industry'].append(i)

    whitepapersFilters['SelectedFilters'] = filters

    results = json.dumps({'values': allwhitepaper, 'filters': whitepapersFilters}, sort_keys=False)

    return results, 200


###########################
## Posters Presentations ##
###########################

@main.route('/posterspresentations', methods=['POST'])
def get_poster_presentations():

    query = request.get_json()
    
    allPoster = []
    postersFilters = {
        "Title": [],
        "Brand": [],
        "Lc_Mode": [],
        "Instrument_Type": [],
        "Year": [],
        "Industry": [],
        "Conference": [],
        "Format": []
    }

    if 'filters' in query:
        params = {}
        filters = query['filters']

        if 'Brand' in filters: params['brand'] = filters['Brand']
        if 'Title' in filters: params['title'] = filters['Title']
        if 'Industry' in filters: params['industry'] = filters['Industry']
        if 'Instrument_Type' in filters: params['instrument_type'] = filters['Instrument_Type']
        if 'Lc_Mode' in filters: params['lc_mode'] = filters['Lc_Mode']
        if 'Conference' in filters: params['conference'] = filters['Conference']
        if 'Year' in filters: params['year'] = filters['Year']

        allPoster = PostersPresentations.objects(__raw__=params).all()
    else:
        filters = []
        allPoster = PostersPresentations.objects.all()

    for Poster in allPoster:
        if Poster['title'] not in postersFilters['Title']:
            postersFilters['Title'].append(Poster['title'])
        if Poster['conference'] not in postersFilters['Conference']:
            postersFilters['Conference'].append(Poster['conference'])
        if Poster['format'] not in postersFilters['Format']:
            postersFilters['Format'].append(Poster['format'])
        if Poster['year'] not in postersFilters['Year']:
            postersFilters['Year'].append(Poster['year'])
        for i in Poster['brand']:
            if i not in postersFilters['Brand']:
                postersFilters['Brand'].append(i)
        for i in Poster['lc_mode']:
            if i not in postersFilters['Lc_Mode']:
                postersFilters['Lc_Mode'].append(i)
        for i in Poster['instrument_type']:
            if i not in postersFilters['Instrument_Type']:
                postersFilters['Instrument_Type'].append(i)
        for i in Poster['industry']:
            if i not in postersFilters['Industry']:
                postersFilters['Industry'].append(i)

    postersFilters['SelectedFilters'] = filters

    return json.dumps({'values': allPoster, 'filters': postersFilters}),200


###########################
## Contact Us    ##
###########################

@main.route('/contactus', methods=['GET'])
def get_contactus_details():

    results = json.dumps(Contacts.objects.all())

    return results, 200


###########################
## Orders & OrderHistory    ##
###########################

@main.route('/order', methods=['POST'])
def submit_order():

    reqOrder = request.get_json()

    if reqOrder is None:

        return jsonify({'code': 999, 'message': 'cart empty, please check'}), 403

    items = []
    for i in reqOrder['items']:
        item = {}
        item['product_id'] = i['product']['_id']['$oid']
        item['quantity'] = i['product']['quantity']
        item['base_price'] = i['product']['base_price']
        items.append(item)

    order = Orders()

    order._id = str(bson.objectid.ObjectId())
    order.items = items
    order.orderplaced = datetime.now()
    order.companyname = reqOrder['companyname']
    order.companyaddress = reqOrder['companyaddress']
    order.state = reqOrder['state']
    order.city = reqOrder['city']
    order.zipcode = reqOrder['zipcode']
    order.ccname = reqOrder['ccname']
    order.card = reqOrder['card']
    order.ccv = reqOrder['ccv']
    order.expiration = reqOrder['expiration']

    order.save()

    return jsonify(order_no=order._id), 200

        
@main.route('/orderhistory', methods=['GET'])
def get_order_history():
    
    results = json.dumps(Orders.objects.all())

    return results, 200

@main.route('/orderitems', methods=['POST'])
def order_items():

    items = request.get_json()

    if items is None:

        return jsonify({'code': 999, 'message': 'cart empty, please check'}), 403

    result = []
    for item in items:

        prod = ProductCatalog.objects.filter(_id=item['product_id']).first()
        result.append({
            "amount": item['amount'],
            "part_number": prod.name,
            "description": prod.description,
            "base_price": prod.base_price
        })

    return {"result":result}, 200
    

###########################
## Menus and Utils       ##
###########################

@menu.route("/navbar/", methods=['GET', 'POST'])
def getnav_menu():

    results = json.dumps(Nabvar.objects.all())

    return results, 200


######################
##   Error methods  ##
######################

@main.errorhandler(exceptions.HTTPException) # main methods error handler
@menu.errorhandler(exceptions.HTTPException) # menu error handler
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })

    response.content_type = "application/json"

    print(response.data)

    return response