import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Cloud
from ..service.CloudService import CloudService
from ..utility.DataValidator import DataValidator


class CloudCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['fileName'] = requestForm.get('fileName','')
        self.form['fileSize'] = requestForm.get('fileSize','')
        self.form['uploadDate'] = requestForm.get('uploadDate','')
        self.form['storageType'] = requestForm.get('storageType','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.fileName = self.form['fileName']
        obj.fileSize = self.form['fileSize']
        obj.uploadDate = self.form['uploadDate']
        obj.storageType = self.form['storageType']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['fileName'] = obj.fileName
        self.form['fileSize'] = obj.fileSize
        self.form['uploadDate'] = obj.uploadDate
        self.form['storageType'] = obj.storageType


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['fileName'])):
            inputError['fileName'] = "fileName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isSpecial(self.form['fileName'])):
                inputError['fileName'] = "fileName contains only "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['fileSize'])):
            inputError['fileSize'] = "fileSize can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isSpecial(self.form['fileSize'])):
                inputError['fileSize'] = "fileSize contains only"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['uploadDate'])):
            inputError['uploadDate'] = "uploadDate can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['uploadDate'])):
                inputError['uploadDate'] = "uploadDate contains only"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['storageType'])):
            inputError['storageType'] = "storageType is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['storageType'])):
                inputError['storageType'] = "storageType Incorrect"
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
            uniqueAttrib = {"fileName": self.form['fileName']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Cloud
            cloud = self.form_to_model(Cloud())
            self.get_service().save(cloud)
            res["success"] = True
            res["result"]["data"] = cloud.id
            res["result"]["message"] = "Cloud added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["fileName"] = json_request.get("fileName", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Cloud.objects.last().id
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
            cloud_list = CloudService().preload()
            preloadList = []
            for x in cloud_list:
                preloadList.append(x.to_json())
            res["result"]["cloudList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return CloudService()