from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import ast
from .models import PointPromotion, PricePackage, Rewards, ConditionRewards, Voucher, Redemption, PromotionPackage, PackageItem, ItemTopping, CustomerPoint, ExchangeHistory
from .serializers import PackageListSerializer, PointSerializer, VoucherSerializer,  RewardsSerializer, ConditionRewardsSerializer, CustomerPointSerializer, ExchangeHistorySerializer, PromotionPackageImage, PricePackageSerializer,PromotionPackageImage
from product.serializers import PackageSerializer, ItemToppingSerializer
from rest_framework.parsers import FormParser, MultiPartParser


class PointPOS(APIView):
    def get(sel, request):
        if PointPromotion.objects.filter(status=True).exists():
            p = PointPromotion.objects.get(status=True)
            ser = PointSerializer(p)
            return Response(ser.data, status=200)
        return Response(None, status=200)


class PointPromotionAPI(APIView):
    def get_object(self, pk):
        try:
            return PointPromotion.objects.get(id=pk)
        except PointPromotion.DoesNotExist:
            raise 404

    def get(self, request):
        point = PointPromotion.objects.all()
        serializer = PointSerializer(point, many=True)
        return Response(serializer.data)

    def put(self, request):
        point = self.get_object(request.data['id'])
        serializer = PointSerializer(point, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        serializer = PointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class Point(APIView):
    def get_object(self, pk):
        try:
            return PointPromotion.objects.get(id=pk)
        except PointPromotion.DoesNotExist:
            raise 404

    def get(self, request, pk):
        point = self.get_object(pk)
        serializer = PointSerializer(point)
        return Response(serializer.data)

    def put(self, request, pk):
        point = self.get_object(pk)
        point.status = request.data['status']
        point.save()
        serializer = PointSerializer(point)
        return Response(serializer.data)

    def delete(self, request, pk):
        point = self.get_object(pk)
        point.delete()
        serializer = PointSerializer(point)
        return Response(serializer.data)


class VoucherAPI(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self, pk):
        try:
            return Voucher.objects.get(id=pk)
        except Voucher.DoesNotExist:
            raise 404

    def get(self, request):
        voucher = Voucher.objects.all()
        serializer = VoucherSerializer(
            voucher, context={'request': request}, many=True)
        return Response(serializer.data)

    def put(self, request):
        voucher = Voucher.objects.get(id=request.data['id'])
        print(voucher, 'voucher')
        serializer = VoucherSerializer(voucher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        serializer = VoucherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class VoucherGET(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self, pk):
        try:
            return Voucher.objects.filter(id=pk)
        except Voucher.DoesNotExist:
            raise 404

    def get(self, request, pk):
        voucher = self.get_object(pk)
        serializer = VoucherSerializer(
            voucher, context={'request': request}, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        voucher = self.get_object(pk)
        voucher.status = request.data['status']
        voucher.save()
        serializer = VoucherSerializer(voucher)
        return Response(serializer.data)


class PackageBySaleChannel(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, pk):
        price = PricePackage.objects.filter(sale_channel_id=pk)
        print(price)
        list = [p.package_id for p in price]
        print(list)
        product = PromotionPackage.objects.filter(
            pk__in=list, status=True)
        serializer = PackageListSerializer(
            product, context={"request": request}, many=True)
        return Response(serializer.data)


class getPackagePOS(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, pk):
        package = PromotionPackage.objects.get(pk=pk)
        serializer = PackageSerializer(
            package, context={'request': request})
        return Response(serializer.data)

class PackageImage(APIView):
    def put(self, request, pk):
        package = PromotionPackage.objects.get(pk=pk)
        serializer = PromotionPackageImage(package,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)

class PackageAPI(APIView):
    def get(self, request):
        package = PromotionPackage.objects.all()
        serializer = PackageSerializer(package,many=True)
        return Response(serializer.data,status=200)

    def post(self, request):
        serializer = PackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors ,status=400)

class PackageDetailAPI(APIView):

    def put(self, request,pk):
        package = PromotionPackage.objects.get(pk=pk)
        serializer = PackageSerializer(package,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)

    parser_classes = []
    def get(self, request,pk):
        package = PromotionPackage.objects.get(pk=pk)
        serializer = PackageSerializer(package)
        return Response(serializer.data,status=200)

class RewardAPI(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self, pk):
        try:
            return Rewards.objects.get(id=pk)
        except Rewards.DoesNotExist:
            raise 404

    def get(self, request):
        reward = Rewards.objects.all()
        serializer = RewardsSerializer(
            reward, context={'request': request}, many=True)
        return Response(serializer.data)

    def put(self, request):
        reward = Rewards.objects.get(id=request.data['id'])
        serializer = RewardsSerializer(reward, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        serializer = RewardsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RewardGET(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self, pk):
        data = []
        try:
            return Rewards.objects.get(id=pk)
        except Rewards.DoesNotExist:
            raise 404

    def get(self, request, pk):
        reward = self.get_object(pk)
        serializer = RewardsSerializer(reward, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        reward = self.get_object(pk)
        reward.status = bool(request.data['status'])
        reward.save()
        serializer = RewardsSerializer(reward)
        return Response(serializer.data)


class ConditionRewardAPI(APIView):
    def get_object(self, pk):
        try:
            return ConditionRewards.objects.get(id=pk)
        except ConditionRewards.DoesNotExist:
            raise 404

    def get(self, request):
        reward = ConditionRewards.objects.all()
        serializer = ConditionRewardsSerializer(reward, many=True)
        return Response(serializer.data)

    def put(self, request):
        reward = ConditionRewards.objects.get(id=request.data['id'])
        serializer = ConditionRewardsSerializer(reward, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        serializer = ConditionRewardsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ConditionRewardGET(APIView):
    def get_object(self, pk):
        try:
            return ConditionRewards.objects.filter(reward_id=pk)
        except ConditionRewards.DoesNotExist:
            raise 404

    def get(self, request, pk):
        rewards = self.get_object(pk)
        print(rewards)
        data = []
        if len(rewards) != 0:
            for i in rewards:
                serializer = ConditionRewardsSerializer(i)
                data.append(serializer.data)
        return Response(data)

    def put(self, request, pk):
        ConditionRewards.objects.get(id=pk).delete()
        return Response('deleted')


class CustomerPointAPI(APIView):
    def get_object(self, pk):
        try:
            return CustomerPoint.objects.get(customer_id=pk)
        except CustomerPoint.DoesNotExist:
            raise 404

    def get(self, request):
        cus_point = CustomerPoint.objects.all()
        serializer = CustomerPointSerializer(cus_point, many=True)
        return Response(serializer.data)

    def put(self, request):
        cus_point = CustomerPoint.objects.get(id=request.data['id'])
        serializer = CustomerPointSerializer(cus_point, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        serializer = CustomerPointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CustomerPointGET(APIView):
    def get_object(self, pk):
        try:
            return CustomerPoint.objects.filter(customer_id=pk)
        except CustomerPoint.DoesNotExist:
            raise 404

    def get(self, request, pk):
        cus_points = self.get_object(pk)
        print(cus_points)
        data = []
        if len(cus_points) != 0:
            for i in cus_points:
                serializer = CustomerPointSerializer(i)
                data.append(serializer.data)
        return Response(data)


class CustomerPointAPI(APIView):
    def get_object(self, pk):
        try:
            return CustomerPoint.objects.get(customer_id=pk)
        except CustomerPoint.DoesNotExist:
            raise 404

    def get(self, request):
        cus_point = CustomerPoint.objects.all()
        serializer = CustomerPointSerializer(cus_point, many=True)
        return Response(serializer.data)

    def put(self, request):
        cus_point = CustomerPoint.objects.get(id=request.data['id'])
        serializer = CustomerPointSerializer(cus_point, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        serializer = CustomerPointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ExchangeHistoryAPI(APIView):
    def get_object(self, pk):
        try:
            return ExchangeHistory.objects.get(customer_id=pk)
        except ExchangeHistory.DoesNotExist:
            raise 404

    def get(self, request):
        exchange_history = ExchangeHistory.objects.all()
        serializer = ExchangeHistorySerializer(exchange_history, many=True)
        return Response(serializer.data)

    def put(self, request):
        exchange_history = ExchangeHistory.objects.get(id=request.data['id'])
        serializer = ExchangeHistorySerializer(
            exchange_history, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        print(request.data)
        reward = Rewards.objects.get(id=request.data['reward_id'])
        reward.qty -= 1
        reward.save()
        customer = CustomerPoint.objects.get(
            customer_id=request.data['customer_id'])
        customer.point -= int(request.data['point'])
        customer.save()
        serializer = ExchangeHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ExchangeHistoryGET(APIView):
    def get_object(self, pk):
        try:
            return ExchangeHistory.objects.filter(customer_id=pk)
        except ExchangeHistory.DoesNotExist:
            raise 404

    def get(self, request, pk):
        exchange_histories = self.get_object(pk)
        print(exchange_histories)
        data = []
        if len(exchange_histories) != 0:
            for i in exchange_histories:
                serializer = ExchangeHistorySerializer(i)
                data.append(serializer.data)
        return Response(data)


class DBS(APIView):
    def get(self, request):
        with open("dbs.txt", "r") as data:
            dictionary = ast.literal_eval(data.read())
        print(dictionary['change'], 'read')
        return Response(dictionary)

    def post(self, request):
        my_file = open("dbs.txt", "w")
        data = repr(request.data)
        my_file.write(data)
        my_file.close()
        print(request.data, 'data')
        return Response('good')
