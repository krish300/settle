import os
import re
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import SettlementSerializer
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from . import models
from . import serializers
from django.conf import settings


class Base:
    filter_backends = (DjangoFilterBackend,)
    # FIXME(kt): temporaray disable of auth
    # permission_classes = (IsAuthenticated,)


class EntityViewSet(Base, ReadOnlyModelViewSet):
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntitySerializer
    filter_fields = ('type', 'category')


class EntityTypeViewSet(Base, ReadOnlyModelViewSet):
    queryset = models.EntityType.objects.all()
    serializer_class = serializers.EntityTypeSerializer
    filter_fields = ('name',)


class EntryCategoryViewSet(Base, ReadOnlyModelViewSet):
    queryset = models.EntryCategory.objects.all()
    serializer_class = serializers.EntryCategorySerializer
    filter_fields = ('name',)


class EntryViewSet(Base, ModelViewSet):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    filter_fields = ('date', 'settlement')


class SettlementViewSet(Base, ModelViewSet):
    queryset = models.Settlement.objects.all()
    serializer_class = serializers.SettlementSerializer
    filter_fields = ('date', 'name')

    @action(detail=False, methods=['get'], url_path='latest')
    def get_latest(self, request, *args, **kwargs):
        headers = {}
        settlement = SettlementSerializer(models.Settlement.objects.earliest())
        return Response(settlement.data, headers=headers, status=200)


class SaleSummaryViewSet(Base, ModelViewSet):
    queryset = models.SaleSummary.objects.all()
    serializer_class = serializers.SaleSummarySerializer
    filter_fields = ('settlement', 'date')


class PaymentModeViewSet(Base, ReadOnlyModelViewSet):
    queryset = models.PaymentMode.objects.all()
    serializer_class = serializers.PaymentModeSerializer
    filter_fields = ('display_in',)


class AppConfigViewSet(Base, ViewSet):

    def list(self, request, format=None):
        headers = {}
        conf = {}
        app_config = models.AppConfig.objects.all()
        for row in app_config:
            conf[row.prop] = row.value
        return Response(conf, headers=headers, status=200)


class PosistDataViewSet(ViewSet):

    @action(detail=False, methods=['get'])
    def get_posist_sale(self, request, format=None):
        headers = {}
        posist_app_mapping_obj = models.AppConfig.objects.get(
            prop='posist-ui-payment-apps-mapping')
        posist_app_mapping = model_to_dict(posist_app_mapping_obj).get('value')
        dt = request.query_params.get('settlemment_date')
        posist_to_settle_sale = {}
        try:
            with open(os.path.join(settings.API_DIR, "temp", "sale-csv", dt + ".csv")) as csv_file:
                try:
                    content = csv_file.read()
                    posist_sale_txt = re.search(
                        r"Collection Break-Up,,\n.*?Gross Sales,", content, re.DOTALL).group()
                    posist_sale = posist_sale_txt.split(",\n")
                    # remove the first and last line which has tect "Collection Break-Up,," "Gross Sales,"
                    posist_sale.pop(0)
                    posist_sale.pop(len(posist_sale)-1)
                    posist_to_settle_sale = {}
                    for sale_app_dtl in posist_sale:
                        nm, val = sale_app_dtl.split(',')
                        nm = nm.strip()
                        val = val.strip().replace('-', '').replace(',', '')
                        # removing float
                        val = int(re.sub(r'\.\d*', '', val))
                        if app_nm := posist_app_mapping.get(nm, None):
                            posist_to_settle_sale[app_nm] = val
                except Exception as e:
                    return Response("Error processing the sale summary file. Check the file from PosIst.", headers=headers, status=400)
        except FileNotFoundError as e:
            return Response("Sale data for the given date not available, Please download from PosIst and try again!", headers=headers, status=400)

        return Response(posist_to_settle_sale, headers=headers, status=200)

    @csrf_exempt
    def create(self, request, format=None):
        headers = {}
        file_obj = request.FILES.get('file')
        file_name = file_obj.name
        infiles_dir = os.path.join(settings.API_DIR, "temp", "sale-csv")
        pattern = r"(\d{4}\.\d{2}\.\d{2})--(\d{4}\.\d{2}\.\d{2})"
        if match := re.search(pattern, file_name, re.IGNORECASE):
            start_dt = match.group(1)
            end_dt = match.group(2)
            if start_dt != end_dt:
                return Response("Invalid File Sent", headers=headers, status=400)

            # at any point there is only one file in this location
            for f in os.listdir(infiles_dir):
                os.remove(os.path.join(infiles_dir, f))

            new_file_name = datetime.datetime.strptime(
                start_dt, '%Y.%m.%d').strftime('%d-%m-%Y') + ".csv"
            new_file = os.path.join(infiles_dir, new_file_name)
            with open(new_file, "wb") as f:
                f.write(file_obj.read())
        else:
            return Response("Invalid File Sent", headers=headers, status=400)

        return Response("Successfully Uploaded", headers=headers, status=200)
