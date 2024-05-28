# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:15:53 2024

@author: 213
"""

import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib as plt

def meanChart(total_df, sgg_nm):
    st.markdown('## 가구별 평균 가격 추세 \n')
    
    filtered_df = total_df[total_df['SGG_NM'] == sgg_nm]
    filtered_df = filtered_df[filtered_df['DEAL_YMD'].between('2023-11-01', '2023-12-31')]
    result = filtered_df.groupby(['DEAL_YMD', 'HOUSE_TYPE'])['OBJ_AMT'].agg('mean').reset_index()
    
    df1 = result[result['HOUSE_TYPE'] == '아파트']
    df2 = result[result['HOUSE_TYPE'] == '단독다가구']
    df3 = result[result['HOUSE_TYPE'] == '오피스텔']
    df4 = result[result['HOUSE_TYPE'] == '연립다세대']
    
    fig = make_subplots(rows=2, cols=2,
                        shared_xaxes=True,
                        subplot_titles=('아파트', '단독다가구', '오피스텔', '연립다세대'),
                        horizontal_spacing=0.15)
    fig.add_trace(px.line(df1, x='DEAL_YMD', y='OBJ_AMT',
                          title='아파트 실거래가 평균', markers=True).data[0], row=1, col=1)
    fig.add_trace(px.line(df2, x='DEAL_YMD', y='OBJ_AMT',
                          title='단독다가구 실거래가 평균', markers=True).data[0], row=1, col=2)
    fig.add_trace(px.line(df3, x='DEAL_YMD', y='OBJ_AMT',
                          title='오피스텔 실거래가 평균', markers=True).data[0], row=2, col=1)
    fig.add_trace(px.line(df4, x='DEAL_YMD', y='OBJ_AMT',
                          title='연립다세대 실거래가 평균', markers=True).data[0], row=2, col=2)
    
    fig.update_yaxes(tickformat='.0f',
                     title_text='물건가격(원)',
                     range=[result['OBJ_AMT'].min(), result['OBJ_AMT'].max()])
    fig.update_layout(
        title = '가구별 평균값 추세 그래프',
        width=800, height=600,
        showlegend=True, template='plotly_white')
    st.plotly_chart(fig)
    
    
def numChart(total_df, sgg_nm):

    st.markdown('## 가구별 거래 건수 \n')

    filtered_df = total_df[total_df['SGG_NM'] == sgg_nm]
    filtered_df = filtered_df[filtered_df['DEAL_YMD'].between('2023-11-01', '2023-12-31')]
    result = filtered_df.groupby(['DEAL_YMD', 'HOUSE_TYPE']).size().reset_index(name='거래 건수')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label = f'아파트 거래 건수(건)', value = result[result['HOUSE_TYPE'] == '아파트']['거래 건수'].values[0])
        st.metric(label = f'단독다가구 거래 건수(건)', value = result[result['HOUSE_TYPE'] == '단독다가구']['거래 건수'].values[0])

    with col2:
        st.metric(label = f'오피스텔 거래 건수(건)', value = result[result['HOUSE_TYPE'] == '오피스텔']['거래 건수'].values[0])
        st.metric(label = f'연립다세대 거래 건수(건)', value = result[result['HOUSE_TYPE'] == '연립다세대']['거래 건수'].values[0])
        
def regionChart(total_df):
    st.markdown('## 지역별 평균 가격 막대 그래프')
    
    month = st.selectbox('월을 선택하세요', total_df['DEAL_YMD'].dt.strftime('%Y-%m').unique())
    house_type = st.selectbox('가구 유형을 선택하세요', total_df['HOUSE_TYPE'].unique())
    filtered_df = total_df[(total_df['DEAL_YMD'].dt.strftime('%Y-%m') == month) & (total_df['HOUSE_TYPE'] == house_type)]
    
    mean_prices = filtered_df.groupby('SGG_NM')['OBJ_AMT'].mean()
    
    fig = px.bar(x=mean_prices.index, y=mean_prices.values,
                 labels={'x':'자치구 명', 'y':'평균 가격'},
                 title='지역별 평균 가격')
    
    st.plotly_chart(fig)

    st.markdown('## 지역별 거래 건수 그래프')
   
    count_df = filtered_df.groupby('SGG_NM')['OBJ_AMT'].count()
    
    fig = px.bar(x=count_df.index, y=count_df.values,
                 labels={'x':'자치구 명', 'y':'거래 건수'},
                 title='지역별 거래 건수')
    
    st.plotly_chart(fig)

def showViz(total_df) :
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format='%Y-%m-%d')

    sgg_nm = st.sidebar.selectbox('자치구명', (total_df['SGG_NM'].unique()))
    selected = st.sidebar.radio('차트메뉴',
                                ['가구당 평균 가격 추세', '가구당 거래 건수', '지역별 평균 가격 막대 그래프'])

    if selected == '가구당 평균 가격 추세' :
        meanChart(total_df, sgg_nm)
    elif selected == '가구당 거래 건수' :
        numChart(total_df, sgg_nm)
    elif selected == '지역별 평균 가격 막대 그래프' :
        regionChart(total_df)
    else :
        st.warning("Error")
