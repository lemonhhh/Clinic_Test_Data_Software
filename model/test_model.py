import pandas as pd
from xgboost import XGBClassifier as XGBC
from sklearn.model_selection import train_test_split
data = pd.read_csv("Kaggle_Sirio_Libanes_ICU_Prediction.csv")
print(data.shape)
print(data.info(verbose=True,null_counts=True))

#划分训练集和测试集
data_y = data['ICU']

#重要的参数
'''
respiratory rate, lactate, blood pressure(diastolic and systolic), neutrophils, oxygen saturation level, immature grans(Abs),
hemoglobin, procalcitonin, erythrocyte sedimentation rates, brain natriuretic peptide, ferritin, D-Dimer, platelets
hematocrit, base excess venous and arterial, albumin, urea
'''

'''
xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.3,random_state=111)
params={'silent':True,'objective':'binary:logistic',"eta":0.1,"scale_pos_weight":1}
dtrain=xgb.DMatrix(xtrain,ytrain)
dtest=xgb.Dmatrix(xtest,ytest)
bst = xgb.train(param,dtrain,num_round)
'''

