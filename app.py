import streamlit as st

from data_processor import read_csv
from chart_processor import portfolio_chart, radar_chart


st.set_page_config(
    page_title="Developer's career path", 
    page_icon='💻', 
    layout='wide', 
    menu_items={
        'Get Help': None, 
        'Report a bug': None, 
        'About': None, 
    }, 
)

params = st.experimental_get_query_params()
df = read_csv('data/category.csv')
df2 = read_csv('data/positions.csv')

st.write(f"## {params.get('name', ['開発者'])[0]}のキャリアパス")

col_left, col_right = st.columns((7, 5), gap='large')
with col_left:
    portfolio = st.empty()
    cat_x = st.selectbox(
        '横軸', 
        df.CATEGORY.values, 
        index=0, 
        format_func=lambda op: df.CATEGORY_LABEL[op], 
    )
    cat_y = st.selectbox(
        '縦軸', 
        df.CATEGORY.values, 
        index=2, 
        format_func=lambda op: df.CATEGORY_LABEL[op], 
    )

    portfolio.plotly_chart(
        portfolio_chart(cat_x, cat_y), 
        use_container_width=True, 
        config={
            'displayModeBar': False, 
        }, 
    )

with col_right:
    st.write('**アーキテクト**')
    st.write('''
    - プロダクト＆その周辺も含めて俯瞰する立場
    - 開発者が開発しやすくする仕組みを提供する
    - 開発に関連する管理全般を通じてＰＪに関わる
    - [ＤＸ](https://developerexperience.io/articles/good-developer-experience)の向上とユーザの要望をバランスする姿勢が求められる
    ''')
    st.write('**基盤**')
    st.write('''
    - プロダクトの基盤を開発する立場
    - プログラマ＆コーダが開発で利用する部品を提供する
    - アプリ基盤・ＤＢ基盤などの開発を通じてＰＪに関わる
    - ＤＸの向上を考える姿勢が求められる
    ''')
    st.write('**プログラマ**')
    st.write('''
    - プロダクトを開発する立場
    - 最終的にユーザが利用する機能群を提供する
    - 設計・開発の両方を通じてＰＪに関わる
    - 開発にあたり**自発的・能動的な姿勢**が求められる
    ''')
    st.write('**コーダ**')
    st.write('''
    - プロダクトを開発する立場
    - 最終的にユーザが利用する機能群を提供する
    - 開発を通じてＰＪに関わる
    - 開発にあたり**指示に従って動くこと**が求められる
    ''')
    st.write('**テスタ**')
    st.write('''
    - プロダクトを開発する立場
    - 開発された機能群に対するテストを実施する
    - テストを通じてＰＪに関わる
    - テストにあたり指示に従って動くことが求められる
    ''')

st.write('---')
st.write('## スキルセット')
st.write('')

types = list(df2.TYPE.unique())
pins = {}
st.caption('比較するキャリアパスを選択')
for i, (col, _type) in enumerate(zip(st.columns(len(types)), types)):
    pins = {**pins, _type: col.checkbox(_type)}
    col.image(f"images/{_type}.png", 
              width=200 if i < 2 else 100 if i == 2 else 50)  # HACK
st.write('')

for tab, _type in zip(st.tabs(types), types):
    with tab:
        st.subheader(_type)
        st.write('')
        col_table, col_chart = st.columns((4, 6), gap='large')
        with col_table:
            df = read_csv('data/skillset.csv')
            for cat, sub in (df.query(f"TYPE == '{_type}'")
                               .groupby('CATEGORY', sort=False)):
                st.write(f"**{cat}**")
                st.dataframe(sub.set_index('TOPIC')
                                .loc[:, ['LEVEL', 'NOTE']]
                                .fillna('')
                                .astype(str)
                                .rename(columns={'LEVEL': 'レベル', 'NOTE': '理由'}), 
                             use_container_width=True)

        with col_chart:
            radar = st.empty()
            st.plotly_chart(
                radar_chart({**pins, _type: True}), 
                use_container_width=True, 
                config={
                    'displayModeBar': False, 
                }, 
            )
            st.write('')
            st.caption('レーダーチャートの見方')
            st.caption('０点：求められない 〜 ５点：強く求められる')
            st.write('')
            st.caption('左表の見方')
            st.caption('''
            - １点：初級 プログラミング言語で言えば、構文を知っているレベル
            - ２点：中級 プログラミング言語で言えば、代表的なＦＷ・パッケージに触れたことがあるレベル
            - ３点：上級 プログラミング言語で言えば、言語仕様に精通している・基盤開発ができるレベル
            ''')
