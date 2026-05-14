import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Podcast
from ..service.PodcastService import PodcastService
from ..utility.DataValidator import DataValidator


class PodcastCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['podcastCode'] = requestForm.get('podcastCode','')
        self.form['podcastTitle'] = requestForm.get('podcastTitle','')
        self.form['hostName'] = requestForm.get('hostName','')
        self.form['status'] = requestForm.get('status','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.podcastCode = self.form['podcastCode']
        obj.podcastTitle = self.form['podcastTitle']
        obj.hostName = self.form['hostName']
        obj.status = self.form['status']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['podcastCode'] = obj.podcastCode
        self.form['podcastTitle'] = obj.podcastTitle
        self.form['hostName'] = obj.hostName
        self.form['status'] = obj.status


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['podcastCode'])):
            inputError['podcastCode'] = "podcastCode can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isAlphaNumeric(self.form['podcastCode'])):
                inputError['podcastCode'] = "podcastCode contains only ABC123 "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['podcastTitle'])):
            inputError['podcastTitle'] = "podcastTitle can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['podcastTitle'])):
                inputError['podcastTitle'] = "podcastTitle contains only letter"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['hostName'])):
            inputError['hostName'] = "hostName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['hostName'])):
                inputError['hostName'] = "hostName contains only "
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
            uniqueAttrib = {"podcastCode": self.form['podcastCode']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Podcast
            podcast = self.form_to_model(Podcast())
            self.get_service().save(podcast)
            res["success"] = True
            res["result"]["data"] = podcast.id
            res["result"]["message"] = "Podcast added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["podcastCode"] = json_request.get("podcastCode", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Podcast.objects.last().id
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
            podcast_list = PodcastService().preload()
            preloadList = []
            for x in podcast_list:
                preloadList.append(x.to_json())
            res["result"]["podcastList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return PodcastService()