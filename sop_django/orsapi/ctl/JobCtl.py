import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Job
from ..service.JobService import JobService
from ..utility.DataValidator import DataValidator


class JobCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['applicantName'] = requestForm.get('applicantName','')
        self.form['companyName'] = requestForm.get('companyName','')
        self.form['position'] = requestForm.get('position','')
        self.form['applicationStatus'] = requestForm.get('applicationStatus','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.applicantName = self.form['applicantName']
        obj.companyName = self.form['companyName']
        obj.position = self.form['position']
        obj.applicationStatus = self.form['applicationStatus']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['applicantName'] = obj.applicantName
        self.form['companyName'] = obj.companyName
        self.form['position'] = obj.position
        self.form['applicationStatus'] = obj.applicationStatus


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['applicantName'])):
            inputError['applicantName'] = "applicantName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['applicantName'])):
                inputError['applicantName'] = "applicantName contains only "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['companyName'])):
            inputError['companyName'] = "companyName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['companyName'])):
                inputError['companyName'] = "companyName contains only letter"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['position'])):
            inputError['position'] = "position can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['position'])):
                inputError['position'] = "position contains only "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['applicationStatus'])):
            inputError['applicationStatus'] = "applicationStatus not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['applicationStatus'])):
                inputError['applicationStatus'] = "applicationStatus contains only  letter"
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
            uniqueAttrib = {"applicantName": self.form['applicantName']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Job
            job = self.form_to_model(Job())
            self.get_service().save(job)
            res["success"] = True
            res["result"]["data"] = job.id
            res["result"]["message"] = "Job added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["applicantName"] = json_request.get("applicantName", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Job.objects.last().id
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
            job_list = JobService().preload()
            preloadList = []
            for x in job_list:
                preloadList.append(x.to_json())
            res["result"]["jobList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return JobService()