import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Hotel
from ..service.HotelService import HotelService
from ..utility.DataValidator import DataValidator


class HotelCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['guestName'] = requestForm.get('guestName','')
        self.form['roomType'] = requestForm.get('roomType','')
        self.form['checkInDate'] = requestForm.get('checkInDate','')
        self.form['totalBill'] = requestForm.get('totalBill','')


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.guestName = self.form['guestName']
        obj.roomType = self.form['roomType']
        obj.checkInDate = self.form['checkInDate']
        obj.totalBill = self.form['totalBill']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['guestName'] = obj.guestName
        self.form['roomType'] = obj.roomType
        self.form['checkInDate'] = obj.checkInDate
        self.form['totalBill'] = obj.totalBill


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['guestName'])):
            inputError['guestName'] = "guestName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['guestName'])):
                inputError['guestName'] = "guestName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['roomType'])):
            inputError['roomType'] = "roomType can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['roomType'])):
                inputError['roomType'] = "roomType contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['checkInDate'])):
            inputError['checkInDate'] = "checkInDate can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['checkInDate'])):
                inputError['checkInDate'] = "checkInDate contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['totalBill'])):
            inputError['totalBill'] = "totalBill can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isinteger(self.form['totalBill'])):
                inputError['totalBill'] = "efficiencyRate Number must start with 6,7,8,9"
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
            uniqueAttrib = {"guestName": self.form['guestName']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the Hotel
            hotel = self.form_to_model(Hotel())
            self.get_service().save(hotel)
            res["success"] = True
            res["result"]["data"] = hotel.id
            res["result"]["message"] = "Hotel added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["guestName"] = json_request.get("guestName", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Hotel.objects.last().id
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
            hotel_list = HotelService().preload()
            preloadList = []
            for x in hotel_list:
                preloadList.append(x.to_json())
            res["result"]["hotelList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return HotelService()