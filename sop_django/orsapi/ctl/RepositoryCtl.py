import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Repository
from ..service.RepositoryService import RepositoryService
from ..utility.DataValidator import DataValidator


class RepositoryCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['repoName'] = requestForm.get('repoName','')
        self.form['owner'] = requestForm.get('owner','')
        self.form['branch'] = requestForm.get('branch','')
        self.form['visibility'] = requestForm.get('visibility','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.repoName = self.form['repoName']
        obj.owner = self.form['owner']
        obj.branch = self.form['branch']
        obj.visibility = self.form['visibility']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['repoName'] = obj.repoName
        self.form['owner'] = obj.owner
        self.form['branch'] = obj.branch
        self.form['visibility'] = obj.visibility


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['repoName'])):
            inputError['repoName'] = "repoName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['repoName'])):
                inputError['repoName'] = "repoName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['owner'])):
            inputError['owner'] = "owner can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['owner'])):
                inputError['owner'] = "owner contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['branch'])):
            inputError['branch'] = "branch can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['branch'])):
                inputError['branch'] = "branch contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['visibility'])):
            inputError['visibility'] = "visibility is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['visibility'])):
                inputError['visibility'] = "visibility Incorrect"
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
            uniqueAttrib = {"repoName": self.form['repoName']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Repository
            repository = self.form_to_model(Repository())
            self.get_service().save(repository)
            res["success"] = True
            res["result"]["data"] = repository.id
            res["result"]["message"] = "Repository added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["repoName"] = json_request.get("repoName", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Repository.objects.last().id
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
            repository_list = RepositoryService().preload()
            preloadList = []
            for x in repository_list:
                preloadList.append(x.to_json())
            res["result"]["repositoryList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return RepositoryService()