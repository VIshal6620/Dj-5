import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Car
from ..service.CarService import CarService
from ..utility.DataValidator import DataValidator


class CarCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['customerName'] = requestForm.get('customerName','')
        self.form['carModel'] = requestForm.get('carModel','')
        self.form['rentPerDay'] = requestForm.get('rentPerDay','')
        self.form['fuelType'] = requestForm.get('fuelType','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.customerName = self.form['customerName']
        obj.carModel = self.form['carModel']
        obj.rentPerDay = self.form['rentPerDay']
        obj.fuelType = self.form['fuelType']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['customerName'] = obj.customerName
        self.form['carModel'] = obj.carModel
        self.form['rentPerDay'] = obj.rentPerDay
        self.form['fuelType'] = obj.fuelType


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['customerName'])):
            inputError['customerName'] = "customerName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['customerName'])):
                inputError['customerName'] = "customerName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['carModel'])):
            inputError['carModel'] = "carModel can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isSpecial(self.form['carModel'])):
                inputError['carModel'] = "carModel contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['rentPerDay'])):
            inputError['rentPerDay'] = "rentPerDay can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isinteger(self.form['rentPerDay'])):
                inputError['rentPerDay'] = "rentPerDay contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['fuelType'])):
            inputError['fuelType'] = "fuelType is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['fuelType'])):
                inputError['fuelType'] = "fuelType Incorrect"
                self.form['error'] = True


        return self.form['error']


    def save(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            self.request_to_form(json_request)
            res = {"result": {}, "success": True}

            # perform input validation
            if (self.input_validation()):
                res["success"] = False
                res["result"]["inputerror"] = self.form["inputError"]
                return JsonResponse(res)
            # Check unique elements
            pk = int(self.form['id'])
            uniqueAttrib = {"customerName": self.form['customerName']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Car
            car = self.form_to_model(Car())
            self.get_service().save(car)
            res["success"] = True
            res["result"]["data"] = car.id
            res["result"]["message"] = "Car added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["customerName"] = json_request.get("customerName", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Car.objects.last().id
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get(self, request, params={}):
        try:
            role = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (role != None):
                res["success"] = True
                res["result"]["data"] = role.to_json()
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def delete(self, request, params={}):
        try:
            role = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (role != None):
                self.get_service().delete(params["id"])
                res["success"] = True
                res["result"]["data"] = role.to_json()
                res["result"]["message"] = "Data has been deleted successfully"
            else:
                res["success"] = False
                res["result"]["message"] = "Data was not deleted"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def preload(self, request, params={}):
        try:
            res = {"result": {}, "success": True}
            car_list = CarService().preload()
            preloadList = []
            for x in car_list:
                preloadList.append(x.to_json())
            res["result"]["carList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return CarService()