import streamlit as st
import pandas as pd
import itertools
import os
import datetime

st.set_page_config(page_title="週末自動更新・競馬予想AI", layout="wide")
st.title("🏇 【週末自動更新】 総合競馬予想システム")

# 自動生成されたデータファイルのパス
DATA_FILE = "latest_prediction.csv"

st.markdown("---")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df_sorted = df.sort_values(by="総合スコア", ascending=False)
    
    file_time = os.path.getmtime(DATA_FILE)
    update_time = datetime.datetime.fromtimestamp(file_time).strftime('%Y/%m/%d %H:%M')
    st.info(f"🔄 最終データ自動更新日時: **{update_time}**")
    
    st.subheader("📊 本日の自動予想ランキング")
    st.dataframe(df_sorted.style.highlight_max(axis=0, subset=['総合スコア'], color='#ff4b4b'))
    
    st.markdown("---")
    st.header("🎯 AIおすすめ買い目予想")
    
    top_horses = df_sorted["馬番"].tolist()
    top_names = df_sorted["馬名"].tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎫 馬連（上位4頭ボックス）")
        box_horses = top_horses[:4]
        for combo in list(itertools.combinations(box_horses, 2)):
            st.write(f"・ **{combo[0]} - {combo[1]}**")
        
    with col2:
        st.subheader("🔥 3連単（1着固定フォーメーション）")
        st.write(f"【1着】 軸馬： **{top_horses[0]}**")
        st.write(f"【2・3着】 相手： **{', '.join(map(str, top_horses[1:4]))}**")
        for p in list(itertools.permutations(top_horses[1:4], 2)):
            st.write(f"・ **{top_horses[0]} → {p[0]} → {p[1]}**")
else:
    st.warning("現在データ収集中です。金・土・日の朝5時に自動で更新されます。")
