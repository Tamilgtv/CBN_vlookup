# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 22:25:00 2021

@author: Tamil vannan
"""

import streamlit as st
import streamlit.components as stc
import pandas as pd
import time 
    
def file_read(): #file read_function

    source_file =  st.file_uploader(label = "Upload your source File", key='source_file') #source_file
    
        #intimating status 
    if bool(source_file)==False:
        st.info("kindly upload your Source File")
    else:
        st.success("Source File Uploaded Successfully Now you can Proceed")

    return source_file

def zip_file(): #file read_function

    zipfile =  st.file_uploader(label = "Upload your Zip File", key='zipfile') #source_file
    
        #intimating status 
    if bool(zipfile)==False:
        st.info("kindly upload Zip Source File")
    else:
        st.success("Zip File Uploaded Successfully Now you can Proceed")

    return zipfile

def show_dataset(df):
            
          #select data set by record counts
            
        rows = df.shape[0]
        
        if st.checkbox("Show Dataset",key='show_dataset'):
            number = st.number_input("Number of Records to View",5,rows)
            st.dataframe(df.head(number))
        
            
            #full dataset  
        if st.checkbox("Show Full dataset",key='show_full_dataset'):
            st.dataframe(df)
            
def concatenate(df):
        #variable separation
        try:
            selected_columns1 = st.multiselect("Select column",df.columns)
            #selected_columns2 = st.selectbox("Select 1st column",df.columns)
            user_input = st.text_input("Enter the concating column name",'Full_Name')
            df[user_input]= df[selected_columns1[0]]+" "+df[selected_columns1[1]]
        
        except:
            pass
        
        return df

def Match(df,zipdf,select_col1,select_col2,output_col):
    
    try:
        
        df['Matched_cell_phone'] = float('NaN')
        
        if st.checkbox('If existing phone column present'):
            df.reset_index(drop='index',inplace=True)
            existing_phone_column = st.selectbox('select Existing column',df.columns)
            checkindex = df[(df[existing_phone_column].isna())&(df['Matched_cell_phone'].isna())].index
        
        else:
            df.reset_index(drop='index',inplace=True)
            checkindex = df[df['Matched_cell_phone'].isna()]
    
            
        # select_col1 =  st.selectbox('Select the column that u want to match from source',df.columns)
        
        # select_col2 =  st.selectbox('select the column that u want to match from zip file',zipdf.columns)
        
        # output_col = st.selectbox('Select the target column from zipfile',zipdf.columns)
        
        
        for index_no , column1 in zip(checkindex,df.loc[checkindex,select_col1]):
            for zipindex, column2 in enumerate(zipdf[select_col2]):
                if str(column1).lower() != 'nan':
                    if str(column1).lower() == str(column2).lower():
                        df.loc[index_no,'Matched_cell_phone'] = zipdf.loc[zipindex,output_col]
    except:
        pass
    return df
    
         
        
            
            
def vlookup(source_df): #vlookup 
    
    zip_df = pd.DataFrame([])
    zip_df =  zip_file()

    try:
        
        source_df = pd.read_excel(source_df)
        zip_df = pd.read_excel(zip_df)
        zip_df.reset_index(drop='index',inplace=True)
        
    except:
        pass
    

        
    if st.checkbox("Concate"):
       source_df =  concatenate(source_df)
    
    

    if st.checkbox('vlookup'):
                    
        select_col1 =  st.selectbox('Select the column that u want to match from source',source_df.columns)
        
        select_col2 =  st.selectbox('select the column that u want to match from zip file',zip_df.columns)
        
        output_col = st.selectbox('Select the target column from zipfile',zip_df.columns)
        
        source_df = Match(source_df,zip_df,select_col1,select_col2,output_col)
        
        
        
    if st.checkbox("Show Dataset"):
        file =  st.selectbox('select dataset', ['source_file','zip_file'])
        
        if file == 'source_file':
            show_dataset(source_df)
        if file == 'zip_file':
            show_dataset(zip_df)        
        
      
    
    
def main():
    
    ht_tit = """ <div style=background-color:#3366cc;><center><h1 
    style= color:white; font-size: 50px; font-family: "Times New Roman", 
    Times, serif;>CBN &nbsp TOOL </h1></center></div>"""
    st.markdown(ht_tit,unsafe_allow_html=True)
    
    
    source_df = pd.DataFrame([])


    
    source_df = file_read()
    
 
    cate = st.sidebar.selectbox('select', ['Home','Vlookup','Check Duplicate'])        

    if cate == 'Vlookup':
        vlookup(source_df)
        
        
        
if __name__ == '__main__':
    main()