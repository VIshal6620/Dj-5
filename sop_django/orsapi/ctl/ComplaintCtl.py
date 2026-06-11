import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Complaint
from ..service.ComplaintService import ComplaintService
from ..utility.DataValidator import DataValidator


class ComplaintCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['citizenID'] = requestForm.get('citizenID','')
        self.form['complaintType'] = requestForm.get('complaintType','')
        self.form['description'] = requestForm.get('description', '')
        self.form['status'] = requestForm.get('status','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.citizenID = self.form['citizenID']
        obj.complaintType = self.form['complaintType']
        obj.description = self.form['description']
        obj.status = self.form['status']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['citizenID'] = obj.citizenID
        self.form['complaintType'] = obj.complaintType
        self.form['description'] = obj.description
        self.form['status'] = obj.status


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['citizenID'])):
            inputError['citizenID'] = "citizenID can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isAlphaNumeric(self.form['citizenID'])):
                inputError['citizenID'] = "citizenID contains only ABC123 "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['complaintType'])):
            inputError['complaintType'] = "complaintType can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['complaintType'])):
                inputError['complaintType'] = "complaintType contains only letter"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "description can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['description'])):
                inputError['description'] = "description contains only letter"
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
            uniqueAttrib = {"citizenID": self.form['citizenID']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Complaint
            complaint = self.form_to_model(Complaint())
            self.get_service().save(complaint)
            res["success"] = True
            res["result"]["data"] = complaint.id
            res["result"]["message"] = "Complaint added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["citizenID"] = json_request.get("citizenID", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Complaint.objects.last().id
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
            complaint_list = ComplaintService().preload()
            preloadList = []
            for x in complaint_list:
                preloadList.append(x.to_json())
            res["result"]["complaintList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return ComplaintService()