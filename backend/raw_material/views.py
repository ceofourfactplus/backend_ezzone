from pprint import pprint
import pandas as pd
from datetime import datetime
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import RawMaterial, RawMaterialCategory, Unit, Supplier, PO, PriceRawMaterial, PickUpRawMaterial
from .serializers import RawMaterialCategorySerializer, UnitSerializer, RawMaterialSerializer, SupplierSerializer, PickUpRawMaterialSerializer, POSerializer, PriceRawMaterialSerializer, ReceiptRawMaterialSerializer, ReceiptRawMaterialDetailSerializer, RMimg

from django.db.models import F,Sum,OuterRef,Count
from rest_framework.parsers import FormParser, MultiPartParser

def change_status_raw():
    raw_material = RawMaterial.objects.all()
    for r in raw_material:
        if r.remain == 0:
            r.status = 3
        elif r.remain < r.minimum:
            r.status = 2
        elif r.remain > r.minimum:
            r.status = 1
        r.save()

class CheckPhoneNumber(APIView):
    def get(self, request, phone_number):
        if Supplier.objects.filter(phone=phone_number).exists():
            return Response('Phone number ' + phone_number + ' is already in use',status=400)
        return Response('don`t have a valid phone number',status=200)

class CheckPhoneNumberEdit(APIView):
    def get(self, request, phone_number,pk):
        if Supplier.objects.filter(phone=phone_number).exclude(pk=pk).exists():
            return Response('Phone number ' + phone_number + ' is already in use',status=400)
        return Response('don`t have a valid phone number',status=200)

class UpdateRmImg(APIView):
    def put(self, request, pk):
        rm = RawMaterial.objects.get(id=pk)
        serializer = RMimg(rm, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ReceiptRawMaterial(APIView):
    def get_object(self, pk):
        try:
            return ReceiptRawMaterial.objects.get(pk=pk)
        except ReceiptRawMaterial.DoesNotExist:
            raise 404

    def get(self, request):
        receipt_raw_material = ReceiptRawMaterial.objects.all()
        serializer = ReceiptRawMaterialSerializer(
            receipt_raw_material, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data, 'receipt data')
        serializer = ReceiptRawMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ReceiptRawMaterialDetail(APIView):
    def get_object(self, pk):
        try:
            return ReceiptRawMaterialDetail.objects.get(pk=pk)
        except ReceiptRawMaterialDetail.DoesNotExist:
            raise 404

    def get(self, request):
        recept_raw_material = ReceiptRawMaterialDetail.objects.all()
        serializer = ReceiptRawMaterialDetailSerializer(
            recept_raw_material, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['remain'] = 0
        print(request.data, 'receipt detail data')
        serializer = ReceiptRawMaterialDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GetRM(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self, pk):
        try:
            return RawMaterial.objects.get(pk=pk)
        except RawMaterial.DoesNotExist:
            raise 404

    def get(self, request, pk):
        RawMaterials = self.get_object(pk)
        serializer = RawMaterialSerializer(
            RawMaterials, context={'request': request})
        return Response(serializer.data)

        

class EditRM(APIView):

    def put(self, request, pk):
        for item in request.data['pricerawmaterial_set']:
            if Unit.objects.filter(unit=item['unit_name']).exists():
                item['unit'] = Unit.objects.get(unit=item['unit_name']).id
            elif not request.data['unit_name'] == '':
                print(1)
                item['unit'] = Unit.objects.create(
                    unit=item['unit_name']).id

        if Unit.objects.filter(unit=request.data['unit_s_name']).exists():
            request.data['unit_s_id'] = Unit.objects.get(
                unit=request.data['unit_s_name']).id
        elif not request.data['unit_s_name'] == '':
            print(2)
            request.data['unit_s_id'
                         ] = Unit.objects.create(
                unit=request.data['unit_s_name']).id
        if Unit.objects.filter(unit=request.data['unit_m_name']).exists():
            request.data['unit_m_id'] = Unit.objects.get(
                unit=request.data['unit_m_name']).id
        elif not request.data['unit_m_name'] == '':
            print(3)
            request.data['unit_m_id'] = Unit.objects.create(
                unit=request.data['unit_m_name']).id
        if Unit.objects.filter(unit=request.data['unit_l_name']).exists():
            request.data['unit_l_id'] = Unit.objects.get(
                unit=request.data['unit_l_name']).id
        elif not request.data['unit_l_name'] == '':
            print(4)
            request.data['unit_l_id'] = Unit.objects.create(
                unit=request.data['unit_l_name']).id
        RawMaterials = RawMaterial.objects.get(pk=pk)
        serializer = RawMaterialSerializer(RawMaterials, request.data)
        if serializer.is_valid():
            serializer.save()
            change_status_raw()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class RawMaterialListAPIView(APIView):
    def get(self, request):
        RawMaterials = RawMaterial.objects.all()
        serializer = RawMaterialSerializer(RawMaterials,context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        for item in request.data['pricerawmaterial_set']:
            if Unit.objects.filter(unit=item['unit_name']).exists():
                item['unit'] = Unit.objects.get(unit=item['unit_name']).id
            else:
                print(1)
                item['unit'] = Unit.objects.create(
                    unit=item['unit_name']).id

        if Unit.objects.filter(unit=request.data['unit_s_name']).exists():
            request.data['unit_s_id'] = Unit.objects.get(
                unit=request.data['unit_s_name']).id
        else:
            request.data['unit_s_id'
                         ] = Unit.objects.create(
                unit=request.data['unit_s_name']).id
        if Unit.objects.filter(unit=request.data['unit_m_name']).exists():
            request.data['unit_m_id'] = Unit.objects.get(
                unit=request.data['unit_m_name']).id
        elif not request.data['unit_m_name'] == '':
            request.data['unit_m_id'] = Unit.objects.create(
                unit=request.data['unit_m_name']).id
        if Unit.objects.filter(unit=request.data['unit_l_name']).exists():
            request.data['unit_l_id'] = Unit.objects.get(
                unit=request.data['unit_l_name']).id
        elif not request.data['unit_l_name'] == '':
            request.data['unit_l_id'] = Unit.objects.create(
                unit=request.data['unit_l_name']).id
            # else:
            #     item['unit'] = Unit.objects.create(unit=item['unit_name']).id

        serializer = RawMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            change_status_raw()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # return Response('ok')


class PriceRawMaterialAPIView(APIView):
    def get(self, request):
        price_rm = PriceRawMaterial.objects.all()
        serializer = PriceRawMaterialSerializer(price_rm, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PriceRawMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        print(serializer.data, 'serializer')
        val = 0
        price = 0
        if int(float(request.data['last_price'])) != 0:
            rm = RawMaterial.objects.get(id=request.data['raw_material_id'])
            prm = PriceRawMaterial.objects.get(
                raw_material_id=request.data['raw_material_id'], unit_id=request.data['unit_id'])
            if rm.unit_s_id == request.data['unit_id']:
                price = int(request.data['last_price']) / rm.remain
                print(price, 'price')
                rm.avg_s = price
                prm.avg_price = price
                rm.save()
                prm.save()
            elif rm.unit_m_id == request.data['unit_id']:
                val = rm.remain / rm.s_to_m
                price = int(request.data['last_price']) / int(val)
                rm.avg_m = price
                prm.avg_price = price
                rm.save()
                prm.save()
            elif rm.unit_l_id == request.data['unit_id']:
                val = (rm.remain / rm.m_to_l) / rm.s_to_m
                price = int(request.data['last_price']) / int(val)
                rm.avg_l = price
                prm.avg_price = price
                rm.save()
                prm.save()
        # return Response(serializer.errors, status=400)
        return Response(serializer.data)

    def put(self, request):
        price_rm = PriceRawMaterial.objects.get(id=request.data['id'])
        serializer = PriceRawMaterialSerializer(price_rm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class PickupPriceRM(APIView):
    def get_object(self, pk):
        try:
            return PickUpRawMaterial.objects.filter(raw_material_id=pk)
        except PickUpRawMaterial.DoesNotExist:
            raise 404

    def post(self, request):
        print(request.data, 'data')
        price_rm = self.get_object(request.data['raw_material_id'])
        return Response(price_rm)


class PickupAPIView(APIView):
    def get(self, request):
        pickup = PickUpRawMaterial.objects.all()
        serializer = PickUpRawMaterialSerializer(pickup, many=True)
        return Response(serializer.data)


class RMAPIView(APIView):
    def get(self, request, pk):
        raw_material = RawMaterial.objects.get(pk=pk)
        serializer = RawMaterialSerializer(raw_material)
        return Response(serializer.data, status=200)

    def put(self, request):
        print(request.data)
        raw_material = RawMaterial.objects.get(id=request.data['id'])
        serializer = RawMaterialSerializer(raw_material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class SupplierListAPIView(APIView):
    def get(self, request):
        Suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(Suppliers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SupplierDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            raise 404

    def get(self, request, pk):
        supplier = self.get_object(pk)
        serializer = SupplierSerializer(supplier, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        supplier = self.get_object(pk)
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        supplier = self.get_object(pk)
        supplier.delete()
        return Response(status=204)


class UnitListAPIView(APIView):

    def get(self, request):
        unit = Unit.objects.all()
        serializer = UnitSerializer(unit, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UnitDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            raise 404

    def get(self, request, pk):
        unit = self.get_object(pk)
        serializer = UnitSerializer(unit)
        return Response(serializer.data)

    def put(self, request, pk):
        unit = self.get_object(pk)
        serializer = UnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        unit = self.get_object(pk)
        unit.delete()
        return Response(status=204)


class CategoryAPIView(APIView):
    def get(self, request):
        
        category = RawMaterialCategory.objects.annotate(product= Count('rawmaterial'),amount=Sum('rawmaterial__remain'))
        serializer = RawMaterialCategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not RawMaterialCategory.objects.filter(name=request.data['name']).exists():
            serializer = RawMaterialCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        return Response('this caetgory name is already in use', status=400)


class RMCategoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return RawMaterialCategory.objects.get(pk=pk)
        except RawMaterialCategory.DoesNotExist:
            raise 404

    def get(self, request, pk):
        category = RawMaterialCategory.objects.get(id=pk)
        serializer = RawMaterialCategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        unit = self.get_object(pk)
        serializer = RawMaterialCategorySerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CategoryFilter(APIView):
    def get(self, request, q):
        if Category.objects.filter(name__contains=q).exists:
            category = Category.objects.filter(name__contains=q)
        else:
            category = Category.objects.all()[:5]
        serializer = CategorySerializer(category, many=True)
        print(serializer.data)
        return Response(serializer.data)


class FilCategoryRaw(APIView):
    def get(self, request, pk):
        raw_material = RawMaterial.objects.filter(category_id=pk)
        serializer = RawMaterialSerializer(raw_material, many=True)
        return Response(serializer.data)


class POList(APIView):
    def get(self, request):
        po = PO.objects.all()
        serializer = POSerializer(po, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = POSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        po = PO.objects.get(id=request.data['id'])
        serializer = POSerializer(po, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PONotice(APIView):
    def get(self, request):
        id_list = []
        rm_list = []
        RawMaterials = RawMaterial.objects.filter(minimum__gte=F('remain'))
        for item in RawMaterials:
            if item.remain <= item.minimum and item.remain > 0:
                id_list.append(item.id)
                item.status = 2
            elif item.remain <= 0:
                id_list.append(item.id)
                item.status = 3
            item.save()
        print(id_list, 'rm list')
        for i in id_list:
            rm_list.append(PriceRawMaterial.objects.filter(
                raw_material_id=i)[0])
        serializer = PriceRawMaterialSerializer(rm_list, many=True)
        # for item in RawMaterials:
        #     print(item.id, item.unit_l_id)
        #     price_rm = PriceRawMaterial.objects.filter(raw_material_id = item.id, unit_id=item.unit_l_id)
        #     print(price_rm, 'price_rm')
        #     rm_list.append(price_rm[0])
        # serializer = PriceRawMaterialSerializer(rm_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        return Response('ok')


class CalcPOAvg(APIView):
    def get(self, request):
        po_items = {}
        avg = {}
        sum_val = 0
        po = PO.objects.all()
        for i in po:
            if po_items.get(i.raw_material_id):
                po_items[i.raw_material_id].append(i)
            else:
                po_items[i.raw_material_id] = [i]
        for prop in po_items:
            for item in po_items[prop]:
                sum_val += int(item.last_price)
            avg[prop] = sum_val / len(po_items[prop])
            sum_val = 0
        print(avg, 'avg')
        for prop in avg:
            po_obj = PO.objects.filter(raw_material_id=prop)[0]
            rm = RawMaterial.objects.get(id=prop)
            print(rm.unit_l_id, rm.unit_m_id, rm.unit_m_id, 'id')
            rm.avg_s = avg[prop]
            l_remain = rm.remain / rm.m_to_l
            prm_l = PriceRawMaterial.objects.get(
                raw_material_id=prop, unit_id=rm.unit_l_id)
            prm_l.avg_price = int(prm_l.last_price) / int(l_remain)
            rm.avg_l = float(prm_l.avg_price)
            prm_l.save()
            m_remain = rm.remain / rm.s_to_m
            prm_m = PriceRawMaterial.objects.get(
                raw_material_id=prop, unit_id=rm.unit_m_id)
            prm_m.avg_price = int(prm_m.last_price) / int(m_remain)
            rm.avg_m = float(prm_m.avg_price)
            rm.save()
            prm_m.save()
            prm = PriceRawMaterial.objects.get(
                raw_material_id=prop, unit_id=po_obj.unit_id)
            prm.avg_price = avg[prop]
            prm.save()
        return Response('calc po avg')


class PORawqueryItem(APIView):
    def get(self, request, query):
        raw_material = RawMaterial.objects.filter(
            remain__lte=F('minimum'), name__contain=query)
        serializer = RawMaterialSerializer(raw_material, many=True)
        return Response(serializer.data)


class PORawqueryUnit(APIView):
    def get(self, request, query):

        raw_material = RawMaterial.objects.filter(
            remain__lte=F('minimum'), __contain=query)
        serializer = RawMaterialSerializer(raw_material, many=True)
        return Response(serializer.data)


class PORawquerySupplier(APIView):
    def get(self, request, query):
        raw_material = RawMaterial.objects.filter(
            remain__lte=F('minimum'), name__contain=query)
        serializer = RawMaterialSerializer(raw_material, many=True)
        return Response(serializer.data)


class CalPO(APIView):
    def post(self, request):
        print(request.data)
        if Unit.objects.filter(unit=request.data['unit']).exists():
            unit = Unit.objects.get(unit=request.data['unit'])
            request.data['unit_id'] = unit.id
        else:
            unit = Unit.objects.create(unit=request.data['unit'])
            request.data['unit_id'] = unit.id

        print(Supplier.objects.filter(company_name=request.data['supplier']))

        if Supplier.objects.filter(company_name=request.data['supplier']).exists():
            supplier = Supplier.objects.get(
                company_name=request.data['supplier'])
            request.data['supplier_id'] = supplier.id
        else:
            return Response('don`t have supplier in data', status=400)

        if RawMaterial.objects.filter(name=request.data['raw_material']).exists():
            raw_material = RawMaterial.objects.get(
                name=request.data['raw_material'])
            request.data['raw_material_id'] = raw_material.id
        else:
            return Response('don`t have raw_material in data', status=400)

        serializer = POSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GetExcelFile(APIView):
    def get(self, request):
        now = datetime.now()
        file_name = now.insert(' ', '_')+'.xlsx'
        pd
        return Response('export to excel')
