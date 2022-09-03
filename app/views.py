from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
from app.serializers import slots, SlotsSerializer, PostSlotsSerializer, appointment, AppointmentSerializer, \
    PostAppointmentSerializer


@method_decorator(csrf_exempt, name='dispatch')
class SlotsCRUD(ListAPIView):
    queryset = slots.objects.all()
    serializer_class = SlotsSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = PostSlotsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(JSONRenderer().render({"Message": "Slot is created sucessfuly"}),
                                    status=status.HTTP_200_OK)
            else:
                return HttpResponse(JSONRenderer().render({"Message": serializer.errors}),
                                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return HttpResponse(JSONRenderer().render({"Error": str(e)}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            id = request.GET.get('id')
            if id != "":
                slot = slots.objects.filter(user=id)
                serializer = SlotsSerializer(slot, many=True)
                return HttpResponse(JSONRenderer().render(serializer.data), status=status.HTTP_200_OK)
            else:
                return HttpResponse(JSONRenderer().render({"Message": "Please Send user id"}),
                                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return HttpResponse(JSONRenderer().render({"Error": str(e)}),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class AppointmentCRUD(ListAPIView):
    queryset = appointment.objects.all()
    serializer_class = AppointmentSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            slot = slots.objects.get(id = data['PatientSlot'])
            if slot.status == True:
                return HttpResponse(JSONRenderer().render({"Message": "Slot is booked already."}),
                                    status=status.HTTP_400_BAD_REQUEST)
            serializer = PostAppointmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                slot.status = True
                slot.save()
                return HttpResponse(JSONRenderer().render({"Message": "Appointment is created successfully"}),
                                    status=status.HTTP_200_OK)
            else:
                return HttpResponse(JSONRenderer().render({"Message": serializer.errors}),
                                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return HttpResponse(JSONRenderer().render({"Error": str(e)}),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            id = request.GET.get('id')
            if id !='':
                app = appointment.objects.filter(PatientSlot__user_id__exact=id)
                serializer = AppointmentSerializer(app, many=True)
                return HttpResponse(JSONRenderer().render(serializer.data), status=status.HTTP_200_OK)
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponse(JSONRenderer().render({"Error": str(e)}),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
