import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Topic
from ..service.TopicService import TopicService
from ..utility.DataValidator import DataValidator


class TopicCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['topicCode'] = requestForm.get('topicCode','')
        self.form['topicName'] = requestForm.get('topicName','')
        self.form['partitions'] = requestForm.get('partitions','')
        self.form['status'] = requestForm.get('status','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.topicCode = self.form['topicCode']
        obj.topicName = self.form['topicName']
        obj.partitions = self.form['partitions']
        obj.status = self.form['status']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['topicCode'] = obj.topicCode
        self.form['topicName'] = obj.topicName
        self.form['partitions'] = obj.partitions
        self.form['status'] = obj.status


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['topicCode'])):
            inputError['topicCode'] = "topicCode can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isAlphaNumeric(self.form['topicCode'])):
                inputError['topicCode'] = "topicCode contains only "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['topicName'])):
            inputError['topicName'] = "topicName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['topicName'])):
                inputError['topicName'] = "topicName contains only"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['partitions'])):
            inputError['partitions'] = "partitions can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isSpecial(self.form['partitions'])):
                inputError['partitions'] = "partitions contains only "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['status'])):
            inputError['status'] = "statuscan not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isSpecial(self.form['status'])):
                inputError['status'] = "status contains only "
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
            uniqueAttrib = {"topicCode": self.form['topicCode']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Topic
            topic = self.form_to_model(Topic())
            self.get_service().save(topic)
            res["success"] = True
            res["result"]["data"] = topic.id
            res["result"]["message"] = "Topic added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["topicCode"] = json_request.get("topicCode", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Topic.objects.last().id
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
            topic_list = TopicService().preload()
            preloadList = []
            for x in topic_list:
                preloadList.append(x.to_json())
            res["result"]["topicList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return TopicService()