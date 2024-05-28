# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:44:40 2024

@author: 213
"""

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

import matplotlib.pyplot as plt
from prophet import Prophet
import numpy as np
from prophet.plot import plot_plotly
import matplotlib.font_manager as fm

def home() :
    st.markdown("### 기계학습 예측 개요 \n"
                "- 가구당 평균 가격 예측 그래프 추세 \n"
                "- 자치구별 평균 가격 예측 그래프 추세 \n"
                "- 사용한 알고리즘 : metad의 prophet \n")
    
def predictType(total_df) :
    
    # 한글 폰트 설정
    path = '/NanumGothic-Bold.ttf'
    fontprop = fm.FontProperties(fname=path, size=12)
    
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format='%Y-%m-%d')
    types = list(total_df['HOUSE_TYPE'].unique())
    
    periods = int(st.number_input('향후 예측 기간을 지정하세요(1일 ~ 30일)',
                                  min_value=1, max_value=30, step=1))
    fig, ax = plt.subplots(figsize=(10, 6), sharex=True, ncols=2, nrows=2)
    for i in range(0, len(types)):
        # 프로핏 모델 객체 인스턴스 만들기
        model = Prophet()
        
        # 훈련 데이터(데이터프레임) 만들기
        # 반드시 두개의 변수(컬럼) ds, y를 가지고 있어야 함
        # (ds (DateStamp column), y (예측하려는 측정 값 (숫자 유형이어야 함))
        total_df2 = total_df.loc[total_df['HOUSE_TYPE'] == types[i], ['DEAL_YMD', 'OBJ_AMT']]
        summary_df = total_df2.groupby('DEAL_YMD')['OBJ_AMT'].agg('mean').reset_index()
        summary_df = summary_df.rename(columns = {'DEAL_YMD' : 'ds', 'OBJ_AMT' : 'y'})
        
        # 훈련 데이터(데이터프레임)로 학습(피팅)하여 prophet 모델 만들기
        model.fit(summary_df)
        
        # 예측결과를 저장할 데이터프레임 준비하기
        # 여기서는 앞으로 28일을 예측하고, 예측 데이터를 담을 데이터프레임(ds 컬럼만 존재) 준비
        future1 = model.make_future_dataframe(periods=periods)
        
        # prodict() 함수를 활용하여 28일치의 데이터를 예측하기
        forcast1 = model.predict(future1)
        
        x = i // 2
        y = i % 2
        
        # 주거 유형별 예측치 시각화
        fig = model.plot(forcast1, uncertainty=True, ax=ax[x, y])
        ax[x, y].set_title(f'서울시 {types[i]} 평균 가격 예측 시나리오 {periods}일간',
                           fontproperties=fontprop)
        ax[x, y].set_xlabel(f'날짜', fontproperties=fontprop)
        ax[x, y].set_ylabel(f'평균가격(만원)', fontproperties=fontprop)
        for tick in ax[x, y].get_xticklabels():
            tick.set_rotation(30)

    plt.tight_layout()
    st.pyplot(fig)

def predictDistrict(total_df) :
    # 한글 폰트 설정
    path = '/NanumGothic-Bold.ttf'
    fontprop = fm.FontProperties(fname=path, size=12)

    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format='%Y-%m-%d')
    
    total_df = total_df[total_df['HOUSE_TYPE'] == '아파트']

    sgg_nms = list(total_df['SGG_NM'].unique())
    print(sgg_nms)
    
    # 자치구 이름 sgg_nms에서 nan 제거
    sgg_nms = [x for x in sgg_nms if x is not np.nan]
    print(sgg_nms)

    periods = int(st.number_input('향후 예측 기간을 지정하세요(1일 ~ 30일)',
                                  min_value=1, max_value=30, step=1))

    fig, ax = plt.subplots(figsize=(20, 10), sharex=True, sharey=False, ncols=5, nrows=5)

    loop = 0
    for sgg_nm in sgg_nms :
        # 프로핏 모델 객체 인스턴스 만들기
        model = Prophet()
        
        total_df2 = total_df.loc[total_df['SGG_NM'] == sgg_nm, ['DEAL_YMD', 'OBJ_AMT']]

        summary_df = total_df2.groupby('DEAL_YMD')['OBJ_AMT'].agg('mean').reset_index()
        summary_df = summary_df.rename(columns = {'DEAL_YMD' : 'ds', 'OBJ_AMT' : 'y'})
        print(sgg_nm)
    
        # 훈련 데이터(데이터프레임)로 학습(피팅)하여 prophet 모델 만들기
        model.fit(summary_df)
        
        # 예측결과를 저장할 데이터프레임 준비하기
        future = model.make_future_dataframe(periods=periods)
        
        # prodict() 함수를 활용하여 25개 자치구별 28일치의 데이터를 예측하기
        forcast = model.predict(future)
        
        x = loop // 5
        y = loop % 5
        loop = loop + 1
        
        # 주거 유형별 예측치 시각화
        fig = model.plot(forcast, uncertainty=True, ax=ax[x, y])
        ax[x, y].set_title(f'서울시 {sgg_nm} 평균 가격 예측 시나리오 {periods}일간',
                           fontproperties=fontprop)
        ax[x, y].set_xlabel(f'날짜', fontproperties=fontprop)
        ax[x, y].set_ylabel(f'평균가격(만원)', fontproperties=fontprop)
        for tick in ax[x, y].get_xticklabels():
            tick.set_rotation(30)
        
    plt.tight_layout()
    st.pyplot(fig)

def reportMain(total_df) :
    sgg_nm = st.sidebar.selectbox('자치구', total_df['SGG_NM'].unique())
    periods = int(st.number_input('향후 예측 기간을 지정하세요(1일 ~ 30일)',
                                  min_value=1, max_value=30, step=1))

    model = Prophet()
    
    total_df2 = total_df.loc[total_df['SGG_NM'] == sgg_nm, ['DEAL_YMD', 'OBJ_AMT']]
    
    summary_df = total_df2.groupby('DEAL_YMD')['OBJ_AMT'].agg('mean').reset_index()
    summary_df = summary_df.rename(columns = {'DEAL_YMD' : 'ds', 'OBJ_AMT' : 'y'})

    # 훈련 데이터(데이터프레임)로 학습(피팅)하여 prophet 모델 만들기
    model.fit(summary_df)
    
    # 예측결과를 저장할 데이터프레임 준비하기
    future = model.make_future_dataframe(periods=periods)
    
    # prodict() 함수를 활용하여 선택한 자치구 28일치의 데이터를 예측하기
    forcast = model.predict(future)
    
    csv = forcast.to_csv(index=False).encode('utf-8')
    
    st.sidebar.download_button('결과 다운로드(CSV)', csv,
                               f'{sgg_nm}_아파트 평균 예측 {periods}일간.csv', 'text/csv', key='download-csv')
    
    fig = plot_plotly(model, forcast)
    fig.update_layout(
        title=dict(text=f'{sgg_nm} 아파트 평균값 예측 {periods} 일간',
                   font=dict(size=20),
                   yref='paper'),
        xaxis_title='날짜',
        yaxis_title='아파트 평균값(만원)',
        autosize=False,
        width=700,
        height=800,
    )
    fig.update_yaxes(tickformat='000')
    st.plotly_chart(fig)
def run_ml_home(total_df) :
    st.markdown("### 기계학습 예측 개요 \n"
                "기계학습 예측 페이지 입니다."
                "사용한 알고리즘 : metad의 prophet")

    selected = option_menu(None, ['Home', '주거형태별', '자치구역별', '보고서'],
                           icons=['house', 'bar-chart', 'file-spreadsheet', 'map'],
                           menu_icon='cast', default_index=0, orientation='horizontal',
                           styles={
                               'container' : {
                                               'padding' : '0!important',
                                               'background-color' : '#808080'},
                               'icon' :      {
                                               'color' : 'orange',
                                               'font-size' : '25px'},
                               'nav-link' :  {
                                               'font-size' : '15px',
                                               'text-align' : 'left',
                                               'margin' : '0px',
                                               '--hover-color' : '#eee'},
                               'nav-link-selected' : {
                                               'background-color' : 'green'}
                              })
    
    if selected == 'Home' :
        home()
    elif selected == '주거형태별' :
        predictType(total_df)
    elif selected == '자치구역별' :
        predictDistrict(total_df)
    elif selected == '보고서' :
        reportMain(total_df)
    else:
        st.warning('Wrong')
