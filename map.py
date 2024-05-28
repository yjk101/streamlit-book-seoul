# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:28:49 2024

@author: 213
"""

import pandas as pd
import streamlit as st
import geopandas as gpd

import matplotlib.pyplot as plt
import plotly.express as px

import matplotlib.font_manager as fm

def mapMatplotlib(merge_df):
    
    # 한글 폰트 설정
    path = 'C:\Windows\Fonts\H2MJRE.TTF'
    fontprop = fm.FontProperties(fname=path, size=12)
    
    fig, ax = plt.subplots(ncols=2, sharey=True, figsize=(15, 10))
    merge_df[merge_df['month'] == 2].plot(ax=ax[0], column='mean', cmap='Pastel1', legend=False, alpha=0.9, edgecolor='gray')
    merge_df[merge_df['month'] == 3].plot(ax=ax[1], column='mean', cmap='Pastel1', legend=False, alpha=0.9, edgecolor='gray')
   
    patch_col = ax[0].collections[0]
    cb = fig.colorbar(patch_col, ax=ax, shrink=0.5)
    for i, row in merge_df[merge_df['month'] == 2].iterrows() :
        ax[0].annotate(row['SIG_KOR_NM'], xy=(row['lon'], row['lat']), xytext=(-7, 2),
                       textcoords='offset points', fontsize=8, color='black', fontproperties=fontprop)

    for i, row in merge_df[merge_df['month'] == 3].iterrows() :
        ax[1].annotate(row['SIG_KOR_NM'], xy=(row['lon'], row['lat']), xytext=(-7, 2),
                       textcoords='offset points', fontsize=8, color='black', fontproperties=fontprop)

    ax[0].set_title('2024-2월 아파트 평균(만원)', fontproperties=fontprop)
    ax[1].set_title('2024-2월 아파트 평균(만원)', fontproperties=fontprop)
    ax[0].set_axis_off()
    ax[1].set_axis_off()

    st.pyplot(fig)

def showMap(total_df) :
    
    st.markdown("### 병합 데이터 확인 \n" "- 컬럼명 확인")
    seoul_gpd = gpd.read_file("seoul_sig.geojson.gpkg")
    seoul_gpd = seoul_gpd.set_crs(epsg='5178', allow_override=True)
    seoul_gpd['center_point'] = seoul_gpd['geometry'].geometry.centroid
    seoul_gpd['geometry'] = seoul_gpd['geometry'].to_crs(epsg=4326)
    seoul_gpd['center_point'] = seoul_gpd['center_point'].to_crs(epsg=4326)
    seoul_gpd['lon'] = seoul_gpd['center_point'].map(lambda x : x.xy[0][0])
    seoul_gpd['lat'] = seoul_gpd['center_point'].map(lambda x : x.xy[1][0])
    seoul_gpd = seoul_gpd.rename(columns={"SIG_CD" : "SGG_CD"})

    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format="%Y-%m-%d")
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    total_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2, 3]))]
    total_df = total_df[['DEAL_YMD', 'month', 'SGG_CD', 'SGG_NM', 'OBJ_AMT', 'HOUSE_TYPE']].reset_index(drop=True)

    summary_df = total_df.groupby(['SGG_CD', 'month'])['OBJ_AMT'].agg(['mean', 'std', 'size']).reset_index()
    summary_df['SGG_CD'] = summary_df['SGG_CD'].astype(str)

    merge_df = seoul_gpd.merge(summary_df, on='SGG_CD')

    st.markdown("- 일부 데이터만 확인")
    st.write(merge_df[['SIG_KOR_NM', 'geometry', 'mean']].head(3))
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("### Matplotlib Style")
    mapMatplotlib(merge_df)