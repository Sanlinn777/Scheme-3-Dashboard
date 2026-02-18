import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st 
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import plotly.graph_objects as go

st.set_page_config(page_title="Scheme III", page_icon="roller_coaster", layout="wide")

#Def for Age Group Columns
def categorize_age_group(age):
    if age >= 0 and age < 5:
        return '0-4 yrs'
    elif age >=5 and age < 15:
        return '5-14 yrs'
    elif age >= 15 and age <= 60:
        return '15-60 yrs'
    else:
        return '> 60 yrs'
    

def categorize_age_group_detail(age):
    if age >= 0 and age < 5:
        return '0-4 yrs'
    elif age >=5 and age < 10:
        return '5-9 yrs'
    elif age >= 10 and age < 15:
        return '10-14 yrs'
    elif age >= 15 and age < 25:
        return '15-24 yrs'
    elif age >= 25 and age < 35:
        return '25-34 yrs'
    elif age >= 35 and age < 45:
        return '35-44 yrs'
    elif age >= 45 and age < 55:
        return '45-54 yrs'
    elif age >= 55 and age < 65:
        return '55-64 yrs'
    else:
        return '> 65 yrs'

@st.cache_data # Cache the data to improve performance
def load_data():
   # Load the data
    df = pd.read_excel("TB03 START FROM 2018.xlsx","TB Registrar 03 Entry Form")
    # Drop rows
    df.dropna(subset=['Year'], inplace=True)
    # Convert Year to Int
    df['Year'] = df['Year'].astype(int)
    #rename 40 column before renaming all columns
    df.rename(columns={40:'DM_eligible'},inplace=True)
    #rename columns
    df.columns = df.columns.str.split('\n').str[0].str.lower().str.replace(' ', '_')
    df.rename(columns={'state/region_name':'SR','township_name':'tsp','reporting_period':'qtr',
                    'township_tb_reg_number':'TB_no',"type_of_patient's":"pt_type",
                    'smoking_status':'smoking','hiv_status':'HIV','x-ray_result':'Xray',
                    '2nd_month_xpert_result':'m2_3_Xpert','5th_month_xpert_result':'m5_Xpert','end_of_tx_':'mEnd_Xray',
                    'end_of_tx':'mEnd_sputum','treatment_outcome':'outcome','district_formula':'district',
                   'facility_name':'facility', 'treatment_registrar_date':'tx_date','treatment_regimens':'regimen',
                   'dm_status':'dm','microscope_result':'sputum', 'xpert_result':'Xpert',
                   '2nd_month_microscope_result':'m2_3_sputum','5th_month':'m5_sputum', 'end_of_tx_xpert_result':'mEnd_Xpert',
                  '':'40 yrs','cpt_':'cpt'},inplace=True)
    #drop unnecessary columns
    df.drop(['specify________(if_ep)', '3rd_month_xpert_result','3rd_month',
         'initial_regimen_started_date','gp','month','tx_date'], axis=1, inplace=True)
    #remove transfer in
    df.drop(df.loc[df['transfer_in']=='Y'].index, inplace= True)
    df.drop(df.loc[df['transfer_in']=='y'].index, inplace= True)

    # Data transformations
    df['facility']= df['facility'].str.upper()
    df['nationality']= df['nationality'].str.upper()
    df['sex']= df['sex'].str.upper()
    df['transfer_in']= df['transfer_in'].str.upper()
    df['pt_type']= df['pt_type'].str.upper()
    df['tb_site']= df['tb_site'].str.upper()
    df['regimen']= df['regimen'].str.upper()
    df['smoking']= df['smoking'].str.upper()
    df['dm']= df['dm'].str.upper()
    df['HIV']= df['HIV'].str.upper()
    df['sputum']= df['sputum'].str.upper()
    df['Xray']= df['Xray'].str.upper()
    df['Xpert']= df['Xpert'].str.upper()
    df['culture']= df['culture'].str.upper()
    df['m2_3_sputum']= df['m2_3_sputum'].str.upper()
    df['m2_3_Xpert']= df['m2_3_Xpert'].str.upper()
    df['m5_sputum']= df['m5_sputum'].str.upper()
    df['m5_Xpert']= df['m5_Xpert'].str.upper()
    df['mEnd_sputum']= df['mEnd_sputum'].str.upper()
    df['mEnd_Xray']= df['mEnd_Xray'].str.upper()
    df['mEnd_Xpert']= df['mEnd_Xpert'].str.upper()
    df['outcome']= df['outcome'].str.upper()
   
    df['regimen'].replace('I ','I', inplace = True)
    df['regimen'].replace(' I','I', inplace = True)
    
    df['Xpert'].fillna('Not test', inplace = True)
    df['nationality'].replace('','N', inplace = True)
    df['nationality'].replace('F','N', inplace = True)
    df['nationality'].replace('M','N', inplace = True)
    
    df['smoking'].replace('N ','N', inplace = True)
    df['smoking'].replace(' N','N', inplace = True)
   
    df['sputum'].replace('P ','P', inplace = True)
    df['sputum'].replace('N ','N', inplace = True)
    df['sputum'].replace('','U', inplace = True)
    
    df['Xray'].replace('P','A', inplace = True)
    df['Xray'].replace('T','ND', inplace = True)
    df['Xray'].replace('p','A', inplace = True)
    df['Xray'].replace('U','ND', inplace = True)
    df['Xray'].replace('miliary TB','A', inplace = True)
    df['Xray'].replace('Primary Complex','A', inplace = True)
    df['Xray'].replace('Miliary TB','A', inplace = True)
    df['Xray'].replace("Koch's Lung",'A', inplace = True)
    df['Xray'].replace('Hydropneumothorax','O', inplace = True)
    df['Xray'].replace('','ND', inplace = True)
    df['sex'].replace('F','Female', inplace = True)
    df['sex'].replace('M','Male', inplace = True)
    df['regimen'].replace('I','Initial Regimen', inplace = True)
    df['regimen'].replace('R','Retreatment Regimen', inplace = True)
    df['regimen'].replace('C','Childhood Regimen', inplace = True)
    df['regimen'].replace('M','Modified Regimen', inplace = True)
    df['smoking'].replace('N','Never', inplace = True)
    df['smoking'].replace('P','Past', inplace = True)
    df['smoking'].replace('C','Current', inplace = True)
   
    df['outcome'].replace('N','Not Evaluated', inplace = True)
    df['outcome'].replace('C','Cure', inplace = True)
    df['outcome'].replace('T','Treatment complete', inplace = True)
    df['outcome'].replace('F','Failure', inplace = True)
    df['outcome'].replace('D','Died', inplace = True)
    df['outcome'].replace('LFU','Loss to follow up', inplace = True)
    df['outcome'].replace('SLD','Moved to second line', inplace = True)
    df['pt_type'].replace('N','New', inplace = True)
    df['pt_type'].replace('R','Relapse', inplace = True)
    df['pt_type'].replace('F','Tx after failure', inplace = True)
    df['pt_type'].replace('L','Tx after loss to follow up', inplace = True)
    df['pt_type'].replace('O','Other previously treated', inplace = True)
    df['pt_type'].replace('U','Unknown', inplace = True)
    df['tb_site'].replace('P','Pulmonary', inplace = True)
    df['tb_site'].replace('EP','Extrapulmonary', inplace = True)
    df['tb_site'].replace('EP-TBM','TB menigitis', inplace = True)
   
    df['dm'].replace('Y','Yes', inplace = True)
    df['dm'].replace('N','No', inplace = True)
    df['dm'].replace('U','Unknown', inplace = True)
    df['HIV'].replace('P','Pos', inplace = True)
    df['HIV'].replace('N','Neg', inplace = True)
    df['HIV'].replace('U','Unk', inplace = True)
    df['sputum'].replace('P','Pos', inplace = True)
    df['sputum'].replace('N','Neg', inplace = True)
    df['sputum'].replace('U','Unk', inplace = True)
    df['bac'].replace(True,'Bact confirm', inplace = True)
    df['bac'].replace(False,'Clinical', inplace = True)
    df['tb_type'] = df['tb_site']+" "+df['bac']
    df['SR'].replace('NayPyitaw','Naypyitaw', inplace = True)
    df['SR'].replace('NaypyiTaw','Naypyitaw', inplace = True)
        
    df['age_group'] = df['age'].apply(categorize_age_group)
    df['age_group_detail'] = df['age'].apply(categorize_age_group_detail)

    #O8 Dataframe
    df_o8 = df.copy()
    df_o8['Reported_yr'] = df_o8['year'] + 1
    return df, df_o8

df, df_o8 = load_data()

   

# ---- SIDEBAR ----
def handle_all_selection(selection, options):
    if 'All' in selection:
        return options  # Returns all options if 'All' is selected
    return selection  # Otherwise, return the selection


st.sidebar.header("Please Filter Here:")

df_sr_sort= df.sort_values('SR', ascending= True)

State_options = list(df_sr_sort["SR"].unique())
State = st.sidebar.multiselect(
    "Select the State & Region:",
   options=['All'] + State_options,
    default= ['Yangon'])

State = handle_all_selection(State, State_options)

df_tsp_sort = df.query( "SR == @State").sort_values('tsp', ascending= True)


Township_options = list(df_tsp_sort["tsp"].unique())
Township = st.sidebar.multiselect(
    "Select the Township:",
    options= ['All'] + Township_options,
    default= ['All'])

Township = handle_all_selection(Township, Township_options)


Year = st.sidebar.multiselect(
    "Select the Year:",
   options=df["year"].unique(),
    default= df["year"].unique())

selected_age = st.sidebar.slider(
    "Select the Age Range:",
    min_value=int(df["age"].min()),
    max_value=int(df["age"].max()),
    value=(int(df["age"].min()), int(df["age"].max())))

selected_sex = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["sex"].unique(),
    default=['Male','Female'])

# Apply filter
df = df.query( 
    "SR == @State & tsp == @Township & year == @Year & age >= @selected_age[0] & age <= @selected_age[1] & sex in @selected_sex"
)

# Apply filter for O8
df_o8 = df_o8.query( 
    "SR == @State & tsp == @Township & Reported_yr == @Year & age >= @selected_age[0] & age <= @selected_age[1] & sex in @selected_sex"
)

# ---- MAINPAGE ----
st.title(":roller_coaster: Scheme 3")
st.markdown("##")

# Display DataFrame or a message if empty
if df.empty:
    st.write('DataFrame is empty!')
    
else:
    total_cases = df["year"].count()
    st.subheader ('Total TB Patient: ')
    st.subheader (f"{total_cases}")

    #year dataframe
    df_year= df.groupby(['year'], as_index=False).agg({'tsp':'count'})
    df_year.rename(columns={'tsp':'patients'}, inplace=True)

    #year chart
    fig_yr = px.line(df_year,x='year',y='patients',title='Yearly Case Holdings')
    fig_yr.update_xaxes(tick0= 0,dtick = 1 )
    st.plotly_chart(fig_yr, use_container_width= True)

    #qtr df
    df_qtr= df.groupby(['qtr'], as_index=False).agg({'year':'count'})
    df_qtr.rename(columns={'year':'patients'}, inplace=True)

    #qtr chart
    fig_qtr= px.line(df_qtr,x='qtr',y='patients',title='Quarterly Case Holdings')
    st.plotly_chart(fig_qtr, use_container_width= True)


    #SR dataframe
    df_sr= df.groupby(['SR'],as_index=False).agg({'year':'count'})
    df_sr = df_sr.sort_values('year', ascending= False)

    # States and Regions Bar Plot
    
    fig_SR= px.bar(df_sr,x = 'SR', y= 'year', labels={'year':'Patients'},
                        title='Total TB cases of States and Regions', color='SR', 
                             color_discrete_sequence=px.colors.diverging.balance)
    fig_SR.update_layout(showlegend=False)

    st.plotly_chart(fig_SR, use_container_width= True)

    #tsp dataframe
    df_tsp= df.groupby(['tsp'],as_index=False).agg({'year':'count'}).sort_values('year', ascending= False)
    df_tsp.insert(0, 'Serial No', range(1, 1 + len(df_tsp)))
    df_tsp.rename(columns={'year':'Total Cases'},inplace=True)
    
    st.subheader('Township with Highest Case Holdings')
    st.dataframe(df_tsp, hide_index=True, use_container_width= True)
   

    #Tsps Bar Plot
    fig_tsp= px.bar(df_tsp, x = 'tsp', y= 'Total Cases',
                        title='Township-wise Case Holdings', color='tsp', 
                             color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_tsp.update_layout(showlegend=False)
   

    st.plotly_chart(fig_tsp, use_container_width= True)

    #sex data frame
    df_sex=df.groupby(['SR','sex']).size().reset_index(name='Patient_count')

    #sex chart
    color_map = {'Female':'blue','Male':'orange'}
    fig_sex= px.bar(df_sex,x='SR',y='Patient_count',color= 'sex',
           barmode ='group',
           title='Gender in TB',
           color_discrete_map=color_map)
    fig_sex.update_layout(showlegend=False)
    #st.plotly_chart(fig_sex, use_container_width= True)

    #Sex Based Data Frame
    df_sex_all= df.groupby(['sex'], as_index= False).agg({'year':'count'})

    #Sex Based Pie Plot
    colors= {'Male':'blue','Female':'orange'}
    fig_sex_all = px.pie(df_sex_all, names= 'sex',values='year',labels={'year':'Patients'},
                            title='Gender Contribution',
                    color= 'sex',color_discrete_map= colors)
    
    st.plotly_chart(fig_sex_all, use_container_width= True)

    #Age group dfs
    df_child= df.groupby(['child'], as_index= False).agg({'year':'count'})


    df_age_group= df.groupby(['age_group'], as_index= False).agg({'year':'count'})


    df_age_group_detail= df.groupby(['age_group_detail'], as_index= False).agg({'year':'count'})


    #Age group charts
    colors= {'adult':'blue','child':'orange'}
    fig_child = px.pie(df_child, names= 'child',values='year',labels={'year':'Patients','child':'Child or Adult'},
                        title='Childhood TB (<15 yrs)',
                  color= 'child',color_discrete_map= colors)
    fig_child.update_traces(pull=[0, 0.2])
    st.plotly_chart(fig_child, use_container_width= True)

    fig_age_group = px.histogram(df_age_group, x= 'age_group',y='year',labels={'year':'Patients'},
                        title='Age category of TB cases', color='age_group', 
                             color_discrete_sequence=px.colors.sequential.Viridis,barmode='overlay',
                             category_orders=dict(age_group=['0-4 yrs','5-14 yrs','15-60 yrs','> 60 yrs']))
    fig_age_group.update_layout(showlegend=False)

    st.plotly_chart(fig_age_group, use_container_width= True)


    fig_age_group_detail = px.histogram(df_age_group_detail, x= 'age_group_detail',y='year',labels={'year':'Patients'},
                        title='Age category detail of TB cases', color='age_group_detail', 
                             color_discrete_sequence=px.colors.sequential.Aggrnyl,barmode='overlay',
                             category_orders=dict(age_group_detail=['0-4 yrs','5-9 yrs','10-14 yrs','15-24 yrs','25-34 yrs',
                                                             '35-44 yrs','45-54 yrs','55-64 yrs','> 65 yrs']))
    fig_age_group_detail.update_layout(showlegend=False)

    st.plotly_chart(fig_age_group_detail, use_container_width= True)

    #Pt type df
    df_pt_type = df.groupby(['pt_type'], as_index= False).agg({'year':'count'})

    #Pt type chart
    colors= {'New':'blue','Relapse':'grey','Other previously treated':'orange','Tx after failure':'purple',
            'Tx after loss to follow up':'red','Unknown':'green'}
    fig_pt_type = px.pie(df_pt_type, names= 'pt_type',values='year',labels={'year':'Patients'},
                            title='Type of Patients',
                    color= 'pt_type',color_discrete_map= colors, hole= 0.4)
    fig_pt_type.update_traces(pull=[0,0.2, 0.3, 0.4, 0.5,0.6])
    st.plotly_chart(fig_pt_type, use_container_width= True)


   
    #TB type df
    df_tb_type =df.groupby(['tb_type'], as_index= False).agg({'year':'count'})
    df_tb_type['tb_type'].replace({'TB menigitis Bact confirm':'Extrapulmonary Bact confirm',
                              'TB menigitis Clinical':'Extrapulmonary Clinical'}, inplace=True)
    df_tb_type= df_tb_type.groupby(['tb_type'], as_index= False).agg({'year':'sum'})

    #TB type chart
    colors= {'Extrapulmonary Bact confirm':'blue','Extrapulmonary Clinical':'grey','Pulmonary Bact confirm':'orange',
         'Pulmonary Clinical':'red'}
    fig_tb_type = px.pie(df_tb_type, names= 'tb_type',values='year',labels={'year':'Patients','tb_type':'TB Type'},
                        title='Type of TB',
                  color= 'tb_type',color_discrete_map= colors, hole= 0.2)
    fig_tb_type.update_traces(pull=[0.4, 0.2, 0, 0])
    st.plotly_chart(fig_tb_type, use_container_width= True)

    #bactconfirm df
    df_bact = df.groupby(['bac'], as_index=False).agg({'year':'count'})

    #bactconfirm chart
    colors= {'Bact confirm':'blue','Clinical':'orange'}
    fig_bact = px.pie(df_bact,names= 'bac',values='year',labels='patients',title='Sputum Positivity',
                    color= 'bac',color_discrete_map= colors)
    st.plotly_chart(fig_bact, use_container_width= True)


    #HIV df
    df_hiv= df.groupby(['HIV'],as_index=False).agg({'year':'count'})

    
    #HIV status known df
    df_hiv_known= df.groupby(['HIV'],as_index=False).agg({'year':'count'})
    df_hiv_known['HIV'].replace({'Neg':'Known','Pos':'Known'}, inplace=True)
    df_hiv_known= df_hiv_known.groupby(['HIV'],as_index=True).agg({'year': 'sum'})

    if 'Known' in df_hiv_known.index and 'Unk' in df_hiv_known.index:
        pass
    elif 'Unk' in df_hiv_known.index:
        df_hiv_known.loc['Known']= 0
    else:
        df_hiv_known.loc['Unk']= 0

    count_hiv_known= df_hiv_known.loc['Known']
    count_hiv_unknown= df_hiv_known.loc['Unk']
    percent_hiv_known= count_hiv_known['year']/(count_hiv_known['year'] + count_hiv_unknown['year'])*100


    #HIV status known chart
    fig_hiv_known_percent = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = percent_hiv_known,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "HCT Testing Percent"},
    gauge= {'axis': {'range': [0,100]},
            'threshold':{'line':{'color':"red", 'width': 4}, 'thickness': 0.75, 'value':90}}))

    st.plotly_chart(fig_hiv_known_percent, use_container_width= True)

    

    #HIV chart
    colors= {'Neg':'blue','Unk':'grey','Pos':'red'}
    fig_hiv = px.pie(df_hiv, names= 'HIV',values='year',labels={'year':'Patients'},title='HCT result',
                  color= 'HIV',color_discrete_map= colors)
    st.plotly_chart(fig_hiv, use_container_width= True)


    #art cpt percent
    df_hiv_pos= df.query("HIV=='Pos'")

    count_hiv_pos= df_hiv_pos['HIV'].count()

    count_art= df_hiv_pos['art'].count()

    percent_art= ((count_art/count_hiv_pos)*100)

    count_cpt= df_hiv_pos['cpt'].count()

    percent_cpt= ((count_cpt/count_hiv_pos)*100)

    #art cpt chart
    fig_percent_art = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = percent_art,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "ART receiving Percent"},
    gauge= {'axis': {'range': [0,100]},
            'threshold':{'line':{'color':"red", 'width': 4}, 'thickness': 0.75, 'value':80}}))

    st.plotly_chart(fig_percent_art, use_container_width= True)


    fig_percent_cpt = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = percent_cpt,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "CPT receiving Percent"},
    gauge= {'axis': {'range': [0,100]},
            'threshold':{'line':{'color':"red", 'width': 4}, 'thickness': 0.75, 'value':70}}))

    st.plotly_chart(fig_percent_cpt, use_container_width= True)

    #GXP dfs
    
    df_pul_above8 = df.query("under_8_yrs=='Above 8' and tb_site=='Pulmonary'")
    df_gxp= df_pul_above8.groupby(['Xpert'], as_index = False).agg({'year':'count'})

    df_gxp_test= df_pul_above8.groupby(['Xpert'], as_index = False).agg({'year':'count'})
    df_gxp_test['Xpert'].replace({'I':'Tested','N':'Tested','RR':'Tested', 'T':'Tested', 'TI':'Tested', 'TT':'Tested'}, inplace=True)
    df_gxp_test= df_gxp_test.groupby(['Xpert'],as_index=True).agg({'year': 'sum'})

    if 'Tested' in df_gxp_test.index and 'Not test' in df_gxp_test.index:
        pass
    elif 'Not test' in df_gxp_test.index:
        df_gxp_test.loc['Tested']= 0
    else:
        df_gxp_test.loc['Not test']= 0


    count_gxp_test= df_gxp_test.loc['Tested']
    count_gxp_nottest= df_gxp_test.loc['Not test']
    percent_gxp_test= count_gxp_test['year']/(count_gxp_test['year'] + 
                                              count_gxp_nottest['year'])*100


    #GXP charts
    
    fig_gxp_test_percent = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = percent_gxp_test,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "GXP Testing Percent in GXP Eligible cases"},
    gauge= {'axis': {'range': [0,100]},
            'threshold':{'line':{'color':"red", 'width': 4}, 'thickness': 0.75, 'value':75}}))

    st.plotly_chart(fig_gxp_test_percent, use_container_width= True)



    colors= {'I':'blue','N':'grey','T':'red','Not test':'teal','RR':'orange','TI':'yellow'}
    fig_gxp = px.pie(df_gxp, names= 'Xpert',values='year',labels={'year':'Patients'},title='GXP Results in GXP Eligible cases',
                  color= 'Xpert',color_discrete_map= colors, hole= 0.3)

    fig_gxp.update_traces(pull=[0.3, 0.1, 0, 0.1,0.2,0.5])
    st.plotly_chart(fig_gxp, use_container_width= True)


    #DM dfs
    df_dm_eligible= df.query("dm_eligible==40")

    df_dm= df_dm_eligible.groupby(['dm'], as_index = False).agg({'year':'count'})
    df_dm.sort_values('year', ascending= False, inplace= True)

    df_dm_testing = df_dm_eligible.groupby(['dm'], as_index = False).agg({'year':'count'})
    df_dm_testing['dm'].replace({'No':'Tested','Yes':'Tested'}, inplace=True)
    df_dm_testing = df_dm_testing.groupby(['dm'], as_index= True).agg({'year':'sum'})

    if 'Tested' in df_dm_testing.index and 'Unknown' in df_dm_testing.index:
        pass
    elif 'Unknown' in df_dm_testing.index:
        df_dm_testing.loc['Tested']= 0
    else:
        df_dm_testing.loc['Unknown' ]= 0

    

    count_dm_tested= df_dm_testing.loc['Tested']
    count_dm_unk= df_dm_testing.loc['Unknown']
    percent_dm_tested = (count_dm_tested['year']/(count_dm_tested['year']+count_dm_unk['year']))*100

    #DM charts
    

    fig_dm_tested_percent = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = percent_dm_tested,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "DM screening in 40 yrs and above TB patients"},
    gauge= {'axis': {'range': [0,100]},
            'threshold':{'line':{'color':"red", 'width': 4}, 'thickness': 0.75, 'value':75}}))

    st.plotly_chart(fig_dm_tested_percent, use_container_width= True)



    colors= {'Unknown':'blue','No':'grey', 'Yes':'orange'}
    fig_dm = px.bar(df_dm, y= 'dm',x= 'year',title= 'DM screening in 40 yrs and above TB patients',labels={'year':'Patients','dm':'DM'},
                orientation='h', color= 'dm', 
                color_discrete_map= colors)
    fig_dm.update_layout(showlegend=False, xaxis_title= 'Patients',yaxis_title= 'DM screening')
    
    st.plotly_chart(fig_dm, use_container_width= True)




    #Tx outcome dfs
    df_outcome= df_o8.groupby(['outcome'], as_index =False).agg({'year':'count'})
       

    
    #TSR df
    df_tsr= df_o8.groupby(['outcome'], as_index =False).agg({'year':'count'})
    df_tsr.drop(df_tsr.loc[df_tsr['outcome']=='Moved to second line'].index, inplace= True)
    df_tsr['outcome'].replace({'Cure':'Tx success','Treatment complete':'Tx success', 'Died':'Tx not success', 
                            'Failure':'Tx not success','Loss to follow up':'Tx not success','Not Evaluated':'Tx not success'},
                            inplace=True)
    df_tsr = df_tsr.groupby(['outcome'], as_index =True).agg({'year':'sum'})

    if 'Tx success' in df_tsr.index and 'Tx not success' in df_tsr.index:
        pass
    elif 'Tx success' in df_tsr.index:
        df_tsr.loc['Tx not success']= 0
    else:
        df_tsr.loc['Tx success']= 0

    count_tsr_success = df_tsr.loc['Tx success']
    count_tsr_not_success = df_tsr.loc['Tx not success']

    
    count_tsr_denominator = count_tsr_not_success['year'] + count_tsr_success['year']

    percent_tsr = (count_tsr_success['year']/count_tsr_denominator)*100

    #TSR chart
    fig_tsr_percent = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = percent_tsr,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "TSR Percent"},
    gauge= {'axis': {'range': [0,100]},
            'threshold':{'line':{'color':"red", 'width': 4}, 'thickness': 0.75, 'value':90}}))

    st.plotly_chart(fig_tsr_percent, use_container_width= True)

    

    #Tx outcome chart
    colors= {'Cure':'blue','Died':'teal','Failure':'grey','Loss to follow up':'orange','Moved to second line':'purple',
            'Not Evaluated':'red','Treatment complete':'green'}
    fig_outcome = px.pie(df_outcome, names= 'outcome',values='year',labels={'year':'Patients'},
                            title='Outcome of TB cases from previous year',
                    color= 'outcome',color_discrete_map= colors, hole= 0.4)
    fig_outcome.update_traces(pull=[0,0.2, 0.3, 0.2, 0.2,0.5, 0])
    st.plotly_chart(fig_outcome, use_container_width= True)

    #Bact confirm O8 df
    df_bact_o8= df_o8.query("bac == 'Bact confirm'")

    #Bact confirm Tx outcome df
    df_bact_outcome= df_bact_o8.groupby(['outcome'], 
                                        as_index =False).agg({'year':'count'})

    #Bact confirm TSR df
    df_bact_tsr= df_bact_o8.groupby(['outcome'], as_index =False).agg({'year':'count'})
    df_bact_tsr.drop(df_bact_tsr.loc[df_bact_tsr['outcome']=='Moved to second line'].index, inplace= True)
    df_bact_tsr['outcome'].replace({'Cure':'Tx success','Treatment complete':'Tx success', 'Died':'Tx not success', 
                            'Failure':'Tx not success','Loss to follow up':'Tx not success','Not Evaluated':'Tx not success'},
                            inplace=True)
    df_bact_tsr = df_bact_tsr.groupby(['outcome'], as_index =True).agg({'year':'sum'})

    if 'Tx success' in df_bact_tsr.index and 'Tx not success' in df_bact_tsr.index:
        pass
    elif 'Tx success' in df_bact_tsr.index:
        df_bact_tsr.loc['Tx not success']= 0
    else:
        df_bact_tsr.loc['Tx success']= 0

    count_bact_tsr_success = df_bact_tsr.loc['Tx success']
    count_bact_tsr_not_success= df_bact_tsr.loc['Tx not success']
    
    
    count_bact_tsr_denominator = count_bact_tsr_not_success['year'] + count_bact_tsr_success['year']

    percent_bact_tsr = (count_bact_tsr_success['year']/count_bact_tsr_denominator)*100
    
    
    #Bact confirm TSR chart
    fig_bact_tsr_percent = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = percent_bact_tsr,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "TSR Percent in Bact Confirmed TB"},
    gauge= {'axis': {'range': [0,100]},
            'threshold':{'line':{'color':"red", 'width': 4}, 'thickness': 0.75, 'value':90}}))

    st.plotly_chart(fig_bact_tsr_percent, use_container_width= True)

    #Bact confirm Tx outcome chart
    colors= {'Cure':'blue','Died':'teal','Failure':'grey','Loss to follow up':'orange','Moved to second line':'purple',
            'Not Evaluated':'red','Treatment complete':'green'}
    fig_bact_outcome = px.pie(df_bact_outcome, names= 'outcome',values='year',labels={'year':'Patients'},
                            title='Outcome of Bact Confirmed TB cases from previous year',
                    color= 'outcome',color_discrete_map= colors, hole= 0.4)
    fig_bact_outcome.update_traces(pull=[0,0.2, 0.3, 0.2, 0.2,0.5, 0])
    st.plotly_chart(fig_bact_outcome, use_container_width= True)




