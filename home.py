# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:40:26 2024

@author: 213
"""

import pandas as pd
import streamlit as st
from millify import prettify

def run_home(total_df):
    st.markdown("## 대시보드 개요 \n"
                "본 프로젝트는 서울시 부동산 실거래가를 알려주는 대시보드 입니다.")
    
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format="%Y-%m-%d")
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    total_df['year'] = total_df['DEAL_YMD'].dt.year
    
    total_df = total_df.loc[total_df['HOUSE_TYPE'] == '아파트', :]
    
    # st.dataframe(total_df)
    
    sgg_nm = st.sidebar.selectbox("자치구", total_df['SGG_NM'].unique())
    
    acc_year = st.sidebar.selectbox("년도", [2023, 2024])
    
    month_dic = {'1월' : 1, '2월' : 2, '3월' : 3, '4월' : 4, '5월' : 5, '6월' : 6,
                 '7월' : 7, '8월' : 8, '9월' : 9, '10월' : 10, '11월' : 11, '12월' : 12
                 }
    
    selected_month = st.sidebar.radio("확인하고 싶은 월을 선택하시오.", list(month_dic.keys()))
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f'{sgg_nm} {acc_year}년 {selected_month} 아파트 가격 개요')
    st.markdown('자치구와 월을 클릭하면 자동으로 각 지역구에서 거래된 **최소가격**, **최대가격**을 확인할 수 있습니다')

    col1, col2, col3 = st.columns(3)

    filtered_month = total_df[total_df['month'] == month_dic[selected_month]]
    filtered_month = filtered_month[filtered_month['year'] == acc_year]
    filtered_month = filtered_month[filtered_month['SGG_NM'] == sgg_nm]

    filtered_month['OBJ_AMT'] = pd.to_numeric(filtered_month['OBJ_AMT'], errors='coerce')

    march_min_price = filtered_month['OBJ_AMT'].min()
    march_max_price = filtered_month['OBJ_AMT'].max()
    march_number = filtered_month.shape[0]
    top_3 = filtered_month.nlargest(3, 'OBJ_AMT')
    bottom_3 = filtered_month.nsmallest(3, 'OBJ_AMT')


    with col1:
        st.metric(label = f'{sgg_nm} 최소가격(만원)', value = prettify(march_min_price))

    with col2:
        st.metric(label = f'{sgg_nm} 최대가격(만원)', value = prettify(march_max_price))
            
    with col3:
        st.metric(label = f'{sgg_nm} 거래건수(건)', value = prettify(march_number))
        
    st.subheader(f'{sgg_nm} {acc_year}년 {selected_month} 상위 3개 아파트 거래')
    st.table(top_3[['SGG_NM', 'BJDONG_NM', 'BLDG_NM', 'BLDG_AREA', 'OBJ_AMT']].sort_values(by='OBJ_AMT', ascending=False))
    
    st.subheader(f'{sgg_nm} {acc_year}년 {selected_month} 하위 3개 아파트 거래')
    st.table(bottom_3[['SGG_NM', 'BJDONG_NM', 'BLDG_NM', 'BLDG_AREA', 'OBJ_AMT']].sort_values(by='OBJ_AMT'))
    
