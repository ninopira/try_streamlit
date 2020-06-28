"""
$ streamlit run sir_app.py
"""
import random

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def main():
    print('start')
    st.title("SIRモデルのDemo")

    st.header('SIRモデル')

    st.subheader('SIRモデルとは')
    st.text('直接伝播する感染症の数理モデルの中でも最もシンプルなモデル')
    st.text('参考: https://www.ism.ac.jp/editsec/toukei/pdf/54-2-461.pdf')

    st.latex(r'''
        \frac{dS(t)}{dt} = - \beta S(t) I(t)
    ''')
    st.latex(r'''
        \frac{dI(t)}{dt} = \beta S(t) I(t) - \gamma I(t)
    ''')
    st.latex(r'''
        \frac{dR(t)}{dt} = \gamma I(t)
    ''')

    st.markdown('$S$: 感受性宿主で感染する可能性のある人口')
    st.markdown('$I$: 感染して感染性を有する状態')
    st.markdown('$R$: 感染後に回復して免疫を獲得した者または死亡者')
    st.markdown('$beta$: 隔離率')
    st.markdown('$\gamma$: 隔離率')

    st.subheader('マルコフ過程')
    st.latex(r'''
        Pr(d(N(t)=1, dR(t)=0) | S_{t}) \simeq = \beta \bar{S}(t)I(t)dt
    ''')
    st.latex(r'''
        Pr(d(N(t)=0, dR(t)=1) | S_{t}) \simeq = \gamma I(t)
    ''')
    st.latex(r'''
        Pr(d(N(t)=0, dR(t)=0) | S_{t}) \simeq = 1 - \beta \bar{S}(t)I(t)dt - \gamma I(t)
    ''')

    st.latex(r'''
        (N(t) = S(0) - S(t))
    ''')

    st.text('なんのこっちゃだが、極小時間の中で以下の3つの事象のどれかがで起きているイメージ')
    st.markdown('- 一番上: 新規に1人かかり、かつ治る人が0')
    st.markdown('- 真ん中: 新規に0人かかり、かつ治る人が1')
    st.markdown('- 一番下: 新規に0人かかり、かつ治る人が0')

    # デモ
    st.header('Demo')
    beta = st.slider('beta', 0.0, 1.0, 0.05)
    gamma = st.slider('gammma', 0.0, 1.0, 1.0)

    st.sidebar.title("other params")
    # all_step = st.sidebar.slider('all_step', 0, 100000, 50000)
    # s0 = st.sidebar.slider('S0', 0, 10000, 1000)
    # i0 = st.sidebar.slider('I0', 0, 100, 1)
    # dt = st.sidebar.slider('dt', 0.0, 1.0, 0.0002)

    all_step = st.sidebar.number_input('all_step', value=50000)
    s0 = st.sidebar.number_input('S0', value=1000)
    i0 = st.sidebar.number_input('I0', value=1)
    dt = st.sidebar.number_input('dt', 0.0, 1.0, 0.0002, format='%f')


    if st.button('RUN'):
        with st.spinner('Wait for it...'):

            s = [s0]
            i = [i0]
            r = [0]
            for t in range(all_step):
                p_infection = beta * s[t] * i[t] * dt
                p_recover = gamma * i[t] * dt
                # 乱数の生成
                rand = random.random()
                print(p_infection, p_recover, rand)
                if rand < p_infection:
                    s.append(s[t] - 1)
                    i.append(i[t] + 1)
                    r.append(r[t])
                elif rand < (p_infection + p_recover):
                    s.append(s[t])
                    i.append(i[t] - 1)
                    r.append(r[t] + 1)
                else:
                    s.append(s[t])
                    i.append(i[t])
                    r.append(r[t])
                print(t, s[t], i[t], r[t])

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=np.arange(all_step), y=s, mode='lines', name='s'))
            fig.add_trace(go.Scatter(x=np.arange(all_step), y=i, mode='lines', name='i'))
            fig.add_trace(go.Scatter(x=np.arange(all_step), y=r, mode='lines', name='r'))


            fig.update_layout(
                autosize=False,
                width=800,
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.text('SIRの値')
            df = pd.DataFrame({
                's': s,
                'i': i,
                'r': r,
            })
            st.dataframe(df)
        st.success('Done!')
        print(dt)






if __name__ == "__main__":
    main()