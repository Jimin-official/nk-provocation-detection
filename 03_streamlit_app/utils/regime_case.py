import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.icon import case_color_map
import matplotlib.ticker as ticker 

def draw_regime_type_chart(df, regime_type='북한', attack_type='미사일'):
    if regime_type == '북한':
        regime_col = 'n_gov'
        regime_order = ['임시정부', '김일성', '김정일', '김정은'][::-1]
    else:
        regime_col = 's_gov'
        regime_order = ['임시정부', '이승만', '윤보선', '박정희', '최규하', '전두환', '노태우', '김영삼',
                        '김대중', '노무현', '이명박', '박근혜', '문재인', '윤석열'][::-1]

    m_icon_color = case_color_map(attack_type)

    df[regime_col] = pd.Categorical(df[regime_col], categories=regime_order, ordered=True)
    grouped = df.groupby([regime_col, 'type'], observed=False).size().unstack(fill_value=0)
    grouped = grouped[grouped.sum(axis=1) > 0]
    grouped = grouped.reindex([idx for idx in regime_order if idx in grouped.index])

    fig, ax = plt.subplots(figsize=(5, 4), facecolor='none')
    grouped.plot(kind='barh', stacked=True, ax=ax, color=m_icon_color)
    ax.set_xlabel('사건 수', color='white')
    ax.set_ylabel('', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    legend = ax.legend(title='도발 유형', facecolor='none', edgecolor='white', labelcolor='white')
    legend.get_title().set_color('white')
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', color='white')
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.yaxis.grid(False)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    st.pyplot(fig)


# 도발 유형 스택 바 차트를 그리는 공통 함수
def draw_regime_main_chart(df, regime_col, regime_order, title):
    countries = ['피습 사건', '미사일','오물풍선', '핵실험']
    color_map = {
        '피습 사건': '#FF6B6B',
        '핵실험': '#F0AD4E',
        '오물풍선': '#3CB371',
        '미사일': '#5BC0DE',
    }
    df[regime_col] = pd.Categorical(df[regime_col], categories=regime_order[::-1], ordered=True)
    grouped = df.groupby([regime_col, 'type'], observed=False).size().unstack(fill_value=0)

    cols_in_order = [c for c in countries if c in grouped.columns]
    grouped = grouped[cols_in_order]

    fig, ax = plt.subplots(figsize=(4.5, 1.8), facecolor='none')
    grouped.plot(
        kind='barh',
        stacked=True,
        ax=ax,
        color=[color_map.get(col, '#333333') for col in grouped.columns]
    )
    ax.set_xlabel('도발 수', color='white', fontsize=7)
    ax.set_ylabel('', color='white')
    ax.tick_params(axis='x', colors='white', labelsize=6)
    ax.tick_params(axis='y', colors='white', labelsize=6)
    legend = ax.legend(fontsize=6, title_fontsize=7, frameon=False)
    for text in legend.get_texts():
        text.set_color('white')
    ax.xaxis.grid(True, linestyle='--', alpha=0.4)
    ax.yaxis.grid(False)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    fig.tight_layout(pad=0.5)
    st.pyplot(fig)