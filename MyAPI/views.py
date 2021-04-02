# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from . models import approvals
from . serializers import approvalsSerializers
from pickle import load
import json
import os

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

dir = os.path.dirname(__file__)


class ApprovalsView(viewsets.ModelViewSet):
	queryset = approvals.objects.all()
	serializer_class = approvalsSerializers


@api_view(["POST"])
def approvereject(request):
	try:
		mdl= load_model(dir+"/loan_model.h5")
		mydata=request.data
		unit=np.array(list(mydata.values()))
		unit=unit.reshape(1,-1)
		scaler=load(open(dir+"/scaler.pkl", 'rb'))
		X=scaler.transform(unit)
		print(X)
		y_pred=mdl.predict(X)
		print(y_pred)
		y_pred=(y_pred>0.58)
		newdf=pd.DataFrame(y_pred, columns=['Status'])
		newdf=newdf.replace({True:'Approved', False:'Rejected'})
		return JsonResponse(f'{newdf}. Thank you',safe=False)
	except ValueError as e:
		return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
