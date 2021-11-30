from flask import redirect, render_template, request, url_for, session, abort, g
from app.helpers.auth import authenticated
from app.models.report import Report
from app.models.evacuationRoute import EvacuationRoute
from app.db import db
from app.helpers.permisoValidator import permisoChecker
from app.validators.reportValidator import ReportValidator
from sqlalchemy.sql import text, and_
import json


def index():
    if not authenticated(session):
        abort(401)

    """Accedo a la variable de configuracion del g object, pagino por la cantidad de
    elementos que tenga almacenada en esa variable y ordeno por el criterio"""
    params = request.args
    reports = Report.query
    if params.get("name", False):
        reports = reports.filter(Report.name == params["name"])

    if params.get("state", False):
        reports = reports.filter(Report.state == params["state"])

    reports = reports.order_by(
        text(f"created_at {g.config.criterio_de_ordenacion}")
    ).paginate(per_page=g.config.elementos_por_pagina)
    errors = {}
    return render_template(
        "report/index.html", errors=errors, fieldsInfo=params, reports=reports
    )


def new():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_index"):
        abort(401)
    errors = {}
    return render_template("report/new.html", errors=errors)


def create():
    if not authenticated(session):
        abort(401)
    """ Se transforma el diccionario inmutable en el que vienen almacenadas las coordenadas
     a un diccionario mutable y se guardan por separados en los campos de longitud y latitud para
     mandarlo al punto nuevo"""
    latLng = json.loads(request.form["coordinates"])
    params = request.form.to_dict()
    del params["coordinates"]
    params["latitude"] = latLng["lat"]
    params["longitude"] = latLng["lng"]
    new_report = Report(**params)
    errors = ReportValidator(new_report).validate_create()
    if errors:
        return render_template("report/new.html", errors=errors, fieldsInfo=new_report)
    db.session.add(new_report)
    db.session.commit()
    return redirect(url_for("reports_index"))