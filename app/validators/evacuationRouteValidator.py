from app.models.evacuationRoute import EvacuationRoute
import re


class EvacuationRouteValidator:
    def __init__(self, params, route=None):
        self.errors = {}
        self.params = params
        self.route = route

    # Validaciones a efectuar a la hora de crear un usuario
    def validate_create(self):
        self.__validate_name()
        self.__validate_input_field()

        return self.errors

    # Validaciones a afectuar a la hora de actualizar la info de un usuario tercero
    def validate_update(self):
        self.__validate_name_update()
        self.__validate_input_field()

        return self.errors

    def __validate_name(self):
        name_is_registered = EvacuationRoute.query.filter(
            EvacuationRoute.name == self.params.name
        ).first()
        if name_is_registered:
            self.errors["name"] = "Ya existe un recorrido con este nombre"

    def __validate_input_field(self):
        if self.params.name == "" or self.params.description == "":
            self.errors["emptyField"] = "Debe completar todos los campos"

    def __validate_name_update(self):
        name_is_registered = (
            EvacuationRoute.query.filter(EvacuationRoute.name == self.params.name)
            .filter(EvacuationRoute.name != self.route.name)
            .first()
        )

        if name_is_registered:
            self.errors["name"] = "Ya existe un recorrido con este nombre"
