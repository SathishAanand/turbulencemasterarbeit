import csv
import glob
import json
import math
import os

json_dir_name = '/home/satish/thesis/flask/repos/data/lstm_101/'

json_pattern = os.path.join(json_dir_name, '*.json')
file_list = glob.glob(json_pattern)
##print(file_list)

## full values each filewise
jsondata=[]
names=[]
tstep=[]
epochs=[]
batch=[]
learningr=[]
activationfn=[]
variety=[]
acc=[]
err=[]
for file in file_list:
    with open(file) as f:
        data = json.load(f)
        errorlists=[]
        #counter=0
        #print(len(data['test_output']))
        for i in range(len(data['test_output'])):
            errorlist=math.sqrt(((pow((data['test_output'][i][0]-data['prediction'][i][0]),2))+
            (pow((data['test_output'][i][1]-data['prediction'][i][1]),2))+
            (pow((data['test_output'][i][2]-data['prediction'][i][2]),2)))/3)
            #print(errorlist)
            errorlists.append(errorlist)
            #counter +=1
            #print(counter)
        #errorlist += errorlist
        #print(errorlists)
        #print(sum(errorlists))
        data['model_accuracy']=int(float(data['model_accuracy'].replace('%',''))*100)
        filesplitter=file.split("/")[-1]
        name=filesplitter.split("_")[-2]
        #jsondata.append({'filename': name, 'model_accuracy': data['model_accuracy'],'errorvalues': math.ceil(sum(errorlists))})
        #jsondata.extend([name, data['model_accuracy'], math.ceil(sum(errorlists))])
        names.append( name)
        
        if(name[1] == '3'):
            ts=3
            tstep.append(ts)
            ep=name[6:8]
            epochs.append(ep)
            bs=name[10:13]
            batch.append(bs)
            if(name[15:19] == '0.01'):
                lr=0.01
                learningr.append(lr)
            if(name[15:20] == '0.001'):
                lr=0.001
                learningr.append(lr)
            if(name[15:21] == '0.0001'):
                lr=0.0001
                learningr.append(lr)
            af=name[-1]
            activationfn.append(af)
            varie='three'
            variety.append(varie)
            #print(names)
        
        if(name[1] == '5'):
            ts=5
            tstep.append(ts)
            ep=name[6:8]
            epochs.append(ep)
            bs=name[10:13]
            batch.append(bs)
            if(name[15:19] == '0.01'):
                lr=0.01
                learningr.append(lr)
            if(name[15:20] == '0.001'):
                lr=0.001
                learningr.append(lr)
            if(name[15:21] == '0.0001'):
                lr=0.0001
                learningr.append(lr)
            af=name[-1]
            activationfn.append(af)
            varie='five'
            variety.append(varie)
            #print(names)
        
        if(name[1:3] == '10'):
            ts=10
            tstep.append(ts)
            ep=name[7:9]
            epochs.append(ep)
            bs=name[11:14]
            batch.append(bs)
            if(name[16:20] == '0.01'):
                lr=0.01
                learningr.append(lr)
            if(name[16:21] == '0.001'):
                lr=0.001
                learningr.append(lr)
            if(name[16:22] == '0.0001'):
                lr=0.0001
                learningr.append(lr)
            af=name[-1]
            activationfn.append(af)
            varie='ten'
            variety.append(varie)
            #print(names)

        if(name[1:3] == '20'):
            ts=20
            tstep.append(ts)
            ep=name[7:9]
            epochs.append(ep)
            bs=name[11:14]
            batch.append(bs)
            if(name[16:20] == '0.01'):
                lr=0.01
                learningr.append(lr)
            if(name[16:21] == '0.001'):
                lr=0.001
                learningr.append(lr)
            if(name[16:22] == '0.0001'):
                lr=0.0001
                learningr.append(lr)
            af=name[-1]
            activationfn.append(af)
            varie='twenty'
            variety.append(varie)
            #print(names)
        #acc.append( data['model_accuracy'])
        #err.append(math.ceil(sum(errorlists)))
        #'timestep','epochs','batchsize','learningrate','activationfunction','variety'
        jsondata.append({'filename': name, 'timestep':ts,'epochs':ep, 'batchsize':bs,'learningrate':lr,'activationfunction':af,
              'model_accuracy': data['model_accuracy'],'errorvalues': math.ceil(sum(errorlists)),'variety':varie})
#jsondata.append(names) 
#print(jsondata)

keys = jsondata[0].keys()
with open('/home/satish/thesis/flask/repos//MA-Aanand-Turbulence/visualization/parallel4.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(jsondata)
#print(jsondata)
