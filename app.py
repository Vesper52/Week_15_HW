from flask import Flask, render_template, jsonify, redirect
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/names')
def names():
    metadata_df = pd.read_csv("Belly_Button_Biodiversity_Metadata.csv")
    BB_list = metadata_df['SAMPLEID'].tolist()
    BB_list2=[]
    for i in BB_list:
        i = "BB_"+str(i)
        BB_list2.append(i)
        jsonBB_list= jsonify(BB_list2)
    return jsonBB_list

@app.route('/otu')
def otu():
    otudata_df = pd.read_csv('belly_button_biodiversity_otu_id.csv')
    OTU_list = otudata_df['lowest_taxonomic_unit_found'].tolist()
    jsonOTU = jsonify(OTU_list)
    return jsonOTU

@app.route('/metadata/<sample>')
def metadata(sample):
    metadict={}
    metadata_df = pd.read_csv("Belly_Button_Biodiversity_Metadata.csv")
    some_id = int(sample)
    test_bb = metadata_df['SAMPLEID']== some_id
    small_meta =metadata_df[test_bb]
    Age = small_meta['AGE'].values[0]
    BBType = small_meta['BBTYPE'].values[0]
    Ethnicity = small_meta['ETHNICITY'].values[0]
    Gender = small_meta['GENDER'].values[0]
    Location = small_meta['LOCATION'].values[0]
    SampleID = small_meta['SAMPLEID'].values[0]

    metadict["AGE"]=str(Age)
    metadict['BBTYPE']=str(BBType)
    metadict['ETHNICITY']=str(Ethnicity)
    metadict['GENDER']=str(Gender)
    metadict['LOCATION']=str(Location)
    metadict['SAMPLEID']=int(SampleID)

    meta = json.dumps(metadict)
    metajson = json.loads(meta)
    jsonmeta = jsonify(metajson)
    return jsonmeta


@app.route('/wfreq/<sample>')
def wfreq(sample):
    metadata_df = pd.read_csv("Belly_Button_Biodiversity_Metadata.csv")
    some_id = int(sample)
    test_bb = metadata_df['SAMPLEID']== some_id
    small_meta =metadata_df[test_bb]
    WFREQ = int(small_meta['WFREQ'].values[0])
    return jsonify(WFREQ)

@app.route('/samples/<sample>')
def samples(sample):
    sampledata_df = pd.read_csv("belly_button_biodiversity_samples.csv")
    some_id = str(sample)
    bb = sampledata_df[['otu_id',some_id]]
    remove_zero = bb[some_id]!=0
    nonzero_bb = bb[remove_zero]
    nonzero_bb = nonzero_bb.sort_values(some_id,ascending=False)
    nonzero_bb = nonzero_bb.head(10)
    bact_dict={}
    bact_dict['otu_ids'] = nonzero_bb['otu_id'].tolist()
    bact_dict['sample_values'] = nonzero_bb[some_id].tolist()
    bactjson = jsonify(bact_dict)

    return bactjson




if __name__ == "__main__":
    app.run(debug=True)
