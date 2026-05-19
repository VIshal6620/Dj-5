import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Courier
from ..service.CourierService import CourierService
from ..utility.DataValidator import DataValidator


class CourierCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['senderName'] = requestForm.get('senderName','')
        self.form['receiverName'] = requestForm.get('receiverName','')
        self.form['status'] = requestForm.get('status','')
        self.form['deliveryDate'] = requestForm.get('deliveryDate','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.senderName = self.form['senderName']
        obj.receiverName = self.form['receiverName']
        obj.status = self.form['status']
        obj.deliveryDate = self.form['deliveryDate']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['senderName'] = obj.senderName
        self.form['receiverName'] = obj.receiverName
        self.form['status'] = obj.status
        self.form['deliveryDate'] = obj.deliveryDate


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['senderName'])):
            inputError['senderName'] = "senderName Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['senderName'])):
                inputError['senderName'] = "senderName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['receiverName'])):
            inputError['receiverName'] = "receiverName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['receiverName'])):
                inputError['receiverName'] = "receiverName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['status'])):
            inputError['status'] = "status can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['status'])):
                inputError['status'] = "status contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['deliveryDate'])):
            inputError['deliveryDate'] = "deliveryDate is required"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['deliveryDate'])):
                inputError['deliveryDate'] = "deliveryDate Incorrect"
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
            uniqueAttrib = {"senderName": self.form['senderName']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Courier
            courier = self.form_to_model(Courier())
            self.get_service().save(courier)
            res["success"] = True
            res["result"]["data"] = courier.id
            res["result"]["message"] = "Courier added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["senderName"] = json_request.get("senderName", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Courier.objects.last().id
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
            courier_list = CourierService().preload()
            preloadList = []
            for x in courier_list:
                preloadList.append(x.to_json())
            res["result"]["courierList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return CourierService()