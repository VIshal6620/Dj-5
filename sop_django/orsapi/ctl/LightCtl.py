import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Light
from ..service.LightService import LightService
from ..utility.DataValidator import DataValidator


class LightCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['lightCode'] = requestForm.get('lightCode','')
        self.form['roomName'] = requestForm.get('roomName','')
        self.form['brightnessLevel'] = requestForm.get('brightnessLevel','')
        self.form['status'] = requestForm.get('status','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.lightCode = self.form['lightCode']
        obj.roomName = self.form['roomName']
        obj.brightnessLevel = self.form['brightnessLevel']
        obj.status = self.form['status']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['lightCode'] = obj.lightCode
        self.form['roomName'] = obj.roomName
        self.form['brightnessLevel'] = obj.brightnessLevel
        self.form['status'] = obj.status


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['lightCode'])):
            inputError['lightCode'] = "lightCode can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isAlphaNumeric(self.form['lightCode'])):
                inputError['lightCode'] = "lightCode contains only ABC123 "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['roomName'])):
            inputError['roomName'] = "roomName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['roomName'])):
                inputError['roomName'] = "roomName contains only letter"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['brightnessLevel'])):
            inputError['brightnessLevel'] = "brightnessLevel can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isSpecial(self.form['brightnessLevel'])):
                inputError['brightnessLevel'] = "brightnessLevel contains only "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['status'])):
            inputError['status'] = "status not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['status'])):
                inputError['status'] = "status contains only  letter"
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
            uniqueAttrib = {"lightCode": self.form['lightCode']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Light
            light = self.form_to_model(Light())
            self.get_service().save(light)
            res["success"] = True
            res["result"]["data"] = light.id
            res["result"]["message"] = "Light added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["lightCode"] = json_request.get("lightCode", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Light.objects.last().id
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
            light_list = LightService().preload()
            preloadList = []
            for x in light_list:
                preloadList.append(x.to_json())
            res["result"]["lightList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return LightService()