import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Claim
from ..service.ClaimService import ClaimService
from ..utility.DataValidator import DataValidator


class ClaimCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['claimNumber'] = requestForm.get('claimNumber','')
        self.form['claimAmount'] = str(requestForm.get('claimAmount',''))
        self.form['status'] = requestForm.get('status','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.claimNumber = self.form['claimNumber']
        obj.claimAmount = self.form['claimAmount']
        obj.status = self.form['status']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['claimNumber'] = obj.claimNumber
        self.form['claimAmount'] = obj.claimAmount
        self.form['status'] = obj.status


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['claimNumber'])):
            inputError['claimNumber'] = "claimNumber can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isAlphaNumeric(self.form['claimNumber'])):
                inputError['claimNumber'] = "claimNumber contains only ABC123 "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['claimAmount'])):
            inputError['claimAmount'] = "claimAmount can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isinteger(self.form['claimAmount'])):
                inputError['claimAmount'] = "claimAmount contains only letter"
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
            uniqueAttrib = {"claimNumber": self.form['claimNumber']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Claim
            claim = self.form_to_model(Claim())
            self.get_service().save(claim)
            res["success"] = True
            res["result"]["data"] = claim.id
            res["result"]["message"] = "Claim added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["claimNumber"] = json_request.get("claimNumber", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Claim.objects.last().id
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
            claim_list = ClaimService().preload()
            preloadList = []
            for x in claim_list:
                preloadList.append(x.to_json())
            res["result"]["claimList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return ClaimService()