import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def main():
    print('start')
    st.title("Demo")

    st.header('データ')
    st.text('signateの【練習問題】お弁当の需要予測のtrain.csvを利用 \nデータは各自でダウンロードしてください')
    st.text('https://signate.jp/competitions/24')

    df = load_data()
    print(df.shape)
    st.header('データ確認')

    st.subheader('dataframe確認')
    # colsから任意のcolを選んで表示
    cols = list(df.columns)
    print(cols)
    selected_cols = st.multiselect('select cols', cols, default='y')
    df_chose = df[selected_cols]
    st.dataframe(df_chose)

    # groupbyしてmeanの表示
    st.subheader('groupby_mean_barplot')
    value_col = st.selectbox('select value cols', cols, index=1)
    groupby_col = st.selectbox('select groupby cols', cols, index=2)

    fig = create_fig_bar_plot(df, groupby_col, value_col)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader('特定nameの時系列ごとの売上')
    x_elms = st.multiselect('select groupby elm', df['name'].unique())
    fig = plot_datetime(df, x_elms)
    st.plotly_chart(fig, use_container_width=True)


@st.cache
def load_data():
    df = pd.read_csv('./train.csv')
    return df

@st.cache
def create_fig_bar_plot(df, xcol, ycol):
    df_tmp = df.groupby(xcol)[ycol].mean().reset_index()
    st.dataframe(df_tmp)
    fig = go.Figure(data=[
        go.Bar(x=df_tmp[xcol], y=df_tmp[ycol], marker=dict(color='#0099ff'), name=xcol)])
    return fig


def plot_datetime(df, x_elms):
    df_x_elms = df[df['name'].isin(x_elms)].sort_values('datetime', ascending=True)
    st.dataframe(df_x_elms)
    df_x_elms['datetime'] = pd.to_datetime(df_x_elms['datetime'], format='%Y-%m-%d')
    fig = go.Figure()
    for elm in x_elms:
        df_tmp = df_x_elms[df_x_elms['name'] == elm]
        fig.add_trace(go.Scatter(x=df_tmp['datetime'], y=df_tmp['y'],
                     mode='lines',
                     name=elm))
    titile = st.text_input("input figure titile")
    st.write(titile)

    if len(titile) < 1:
        titile = str(x_elms)

    fig.update_layout(
        title=titile,
        xaxis_title="date",
        yaxis_title="sales")

    return fig


if __name__ == "__main__":
    main()