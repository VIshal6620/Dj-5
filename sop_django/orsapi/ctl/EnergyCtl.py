import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Energy
from ..service.EnergyService import EnergyService
from ..utility.DataValidator import DataValidator


class EnergyCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['energySource'] = requestForm.get('energySource','')
        self.form['productionUnit'] = requestForm.get('productionUnit','')
        self.form['outputLevel'] = requestForm.get('outputLevel','')
        self.form['efficiencyRate'] = requestForm.get('efficiencyRate','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.energySource = self.form['energySource']
        obj.productionUnit = self.form['productionUnit']
        obj.outputLevel = self.form['outputLevel']
        obj.efficiencyRate = self.form['efficiencyRate']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['energySource'] = obj.energySource
        self.form['productionUnit'] = obj.productionUnit
        self.form['outputLevel'] = obj.outputLevel
        self.form['efficiencyRate'] = obj.efficiencyRate


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['energySource'])):
            inputError['energySource'] = "EnergySource Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['energySource'])):
                inputError['energySource'] = "EnergySource contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['productionUnit'])):
            inputError['productionUnit'] = "ProductionUnit can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isSpecial(self.form['productionUnit'])):
                inputError['productionUnit'] = "ProductionUnit contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['outputLevel'])):
            inputError['outputLevel'] = "outputLevel can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeck(self.form['outputLevel'])):
                inputError['outputLevel'] = "outputLevel contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['efficiencyRate'])):
            inputError['efficiencyRate'] = "efficiencyRate Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isSpecial(self.form['efficiencyRate'])):
                inputError['efficiencyRate'] = "efficiencyRate Number must start with 6,7,8,9"
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
            uniqueAttrib = {"energySource": self.form['energySource']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Energy
            energy = self.form_to_model(Energy())
            self.get_service().save(energy)
            res["success"] = True
            res["result"]["data"] = energy.id
            res["result"]["message"] = "Energy added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["energySource"] = json_request.get("energySource", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Energy.objects.last().id
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
            energy_list = EnergyService().preload()
            preloadList = []
            for x in energy_list:
                preloadList.append(x.to_json())
            res["result"]["energyList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return EnergyService()