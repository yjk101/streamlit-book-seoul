# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:29:06 2024

@author: 213
"""

### statistic.py(2)
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from pingouin import ttest
import pingouin as pg

import matplotlib.font_manager as fm

def twoMeans(total_df, sgg_nm) :

    st.markdown('### 서울시 2월, 3월 아파트 평균 가격 차이 검증')

    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2, 3]))]

    dec_df = apt_df[apt_df['month'] == 2]
    nov_df = apt_df[apt_df['month'] == 3]


    st.markdown(f"2월 아파트 평균 가격 : {dec_df['OBJ_AMT'].mean().round(0)} 만원")
    st.markdown(f"3월 아파트 평균 가격 : { nov_df['OBJ_AMT'].mean().round(0)} 만원")
    
    result = ttest(dec_df['OBJ_AMT'], nov_df['OBJ_AMT'], paired=False)
    st.dataframe(result, use_container_width=True)

    if result['p-val'].values[0] > 0.05:
        st.markdown('p-val 값이 0.05 초과로 서울시 2월, 3월 아파트 평균 가격 차이는 없다.')
    else :
        st.markdown('p-val 값이 0.05 미만으로 서울시 2월, 3월 아파트 평균 가격 차이가 있다.')
        
    st.markdown(f'### 서울시 {sgg_nm} 2월, 3월 아파트 평균 가격 차이 검증')
    
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2, 3]))]
            
    sgg_df = apt_df[apt_df['SGG_NM'] == sgg_nm]
    
    sgg_dec_df = sgg_df[sgg_df['month'] == 2]
    sgg_nov_df = sgg_df[sgg_df['month'] == 3]

    st.markdown(f"{sgg_nm} 2월 아파트 평균 가격 : {dec_df['OBJ_AMT'].mean().round(0)} 만원")
    st.markdown(f"{sgg_nm} 3월 아파트 평균 가격 : {nov_df['OBJ_AMT'].mean().round(0)} 만원")

    result = ttest(dec_df['OBJ_AMT'], nov_df['OBJ_AMT'], paired=False)
    st.dataframe(result, use_container_width=True)

    if result['p-val'].values[0] > 0.05:
        st.markdown(f'p-val 값이 0.05 초과로 {sgg_nm} 2월, 3월 아파트 평균 가격 차이는 없다.')
    else :
        st.markdown(f'p-val 값이 0.05 미만으로 {sgg_nm} 2월, 3월 아파트 평균 가격 차이가 있다.')
        
    st.markdown(f'### 서울시 {sgg_nm} 2월, 3월 아파트 평균 가격 차이 검증')
    
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2, 3]))]

    sgg_df = apt_df[apt_df['SGG_NM'] == sgg_nm]

    sgg_dec_df = sgg_df[sgg_df['month'] == 2]
    sgg_nov_df = sgg_df[sgg_df['month'] == 3]

    st.markdown(f"{sgg_nm} 2월 아파트 평균 가격 : {sgg_dec_df['OBJ_AMT'].mean().round(0)} 만원")
    st.markdown(f"{sgg_nm} 3월 아파트 평균 가격 : {sgg_nov_df['OBJ_AMT'].mean().round(0)} 만원")

    sgg_result = ttest(sgg_dec_df['OBJ_AMT'], sgg_nov_df['OBJ_AMT'], paired=False)
    st.dataframe(sgg_result, use_container_width=True)

    if sgg_result['p-val'].values[0] > 0.05:
        st.markdown(f'p-val 값이 0.05 초과로 {sgg_nm} 2월, 3월 아파트 평균 가격 차이는 없다.')
    else :
        st.markdown(f'p-val 값이 0.05 미만으로 {sgg_nm} 2월, 3월 아파트 평균 가격 차이가 있다.')
    
def corrRealtion(total_df, sgg_nm):
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE']  == '아파트') & (total_df['month'].isin([2, 3]))] 
                                                            
    st.markdown('### 상관관계 분석 데이터 학인 \n'
                '- 건물면적과 거래금액의 상관관계 분석\n'
                '- 먼저 추출한 데이터 확인')

    corr_df = apt_df[['DEAL_YMD', 'OBJ_AMT', 'BLDG_AREA', 'SGG_NM', 'month']].reset_index(drop=True)
    st.dataframe(corr_df.head())

    st.markdown('### 서울시 상관관계 분석 시각화 \n'
                '- 서울시 2월 ~ 3월 산포도 그리기 \n')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='BLDG_AREA', y='OBJ_AMT', data=corr_df, ax=ax)
    st.pyplot(fig)
    
    st.markdown('### 서울시 상관관계 계수 및 검정 \n'
                '- 상관관계 계수를 확인 \n')
    st.dataframe(pg.corr(corr_df['BLDG_AREA'], corr_df['OBJ_AMT']).round(3), use_container_width=False)
    corr_r = pg.corr(corr_df['BLDG_AREA'], corr_df['OBJ_AMT']).round(3)['r']
    
    st.write(corr_r.item())
    
    if (corr_r.item() > 0.5) :
        st.markdown(f'상관계수는 {corr_r.item()}이며, 건물 면적이 증가할 수록 물건 금액도 증가하는 경향성을 가진다')
    elif (corr_r.item() < -0.5) :
        st.markdown(f'상관계수는 {corr_r.item()}이며, 건물 면적이 증가할 수록 물건 금액은 감소하는 경향성을 가진다')
    else :
        st.markdown(f'상관계수는 {corr_r.item()}이며, 건물 면적과 물건 금액과의 관계성은 비교적 작다')

### 서울시 구별 상관계수 시각화
    st.markdown(f'### 서울시 {sgg_nm} 2월, 3월 아파트 가격 ~ 건물면적 상관관계 분석 \n')
    sgg_df = corr_df[corr_df['SGG_NM'] == sgg_nm]
    corr_coef = pg.corr(sgg_df['BLDG_AREA'], sgg_df['OBJ_AMT'])
    st.dataframe(corr_coef, use_container_width=False)

# 한글 폰트 설정
    path = 'C:\Windows\Fonts\H2MJRE.TTF'
    fontprop = fm.FontProperties(fname=path, size=12)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='BLDG_AREA', y='OBJ_AMT', data=sgg_df)
    ax.text(0.95, 0.05, f"Pearson Correlation : {corr_coef['r'].values[0]:.2f}",
                                                    transform=ax.transAxes, ha='right', fontsize=12)
    ax.set_title(f'{sgg_nm} 피어슨 상관계수', fontproperties=fontprop)
    st.pyplot(fig)
    
    # 서울시 구별 거래 건수와 아파트 가격 상관관계 분석
    st.markdown(f'### 서울시 {sgg_nm} 구별 거래 건수(2월-3월)와 아파트 가격 상관관게 분석')
    
    # 그룹핑
    mean_size = sgg_df.groupby('DEAL_YMD')['OBJ_AMT'].agg(['mean', 'size'])
    st.dataframe(mean_size)
    
    # 상관관계 분석
    corr_coef_size = pg.corr(mean_size['mean'], mean_size['size'])
    st.dataframe(corr_coef_size)
    
    if corr_coef_size['p-val'].values[0] < 0.05:
        st.markdown(f'p-val 값이 0.05 미만으로 {sgg_nm} 구별 거래 건수와 아파트 가격 상관관계가 유의미하다.')
    else:
        st.markdown(f'p-val 값이 0.05 이상으로 {sgg_nm} 구별 거래 건수와 아파트 가격 상관관계가 유의미하지 않다.')
        
    # 피어슨 상관계수 그래프
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x=mean_size['mean'], y=mean_size['size'], ax=ax)
    ax.set_xlabel('Average Price of Apartments')
    ax.set_ylabel('Number of Transactions')
    ax.set_title(f'Correlation between Average Price and Transaction Count of Apartments in {sgg_nm}', fontproperties=fontprop)
    st.pyplot(fig)

def showStat(total_df) :
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format='%Y-%m-%d')

    analisys_nm = st.sidebar.selectbox('분석매뉴', ['두 집단간 차이 검정', '상관분석'])
    sgg_nm = st.sidebar.selectbox('자치구명', total_df['SGG_NM'].unique())

    if analisys_nm == '두 집단간 차이 검정' :
        twoMeans(total_df, sgg_nm)
    elif analisys_nm == '상관분석' :
        corrRealtion(total_df, sgg_nm)
    else :
        st.warning("Error")