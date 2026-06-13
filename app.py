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
    
    # 昔のデータが残っていた場合の安全対策
    if 'SNS評価点' not in df.columns:
        df['データスコア'] = df['総合スコア']
        df['SNS評価点'] = 0.0

    # スコア順に並び替え
    df_sorted = df.sort_values(by="総合スコア", ascending=False)
    
    # 更新日時の表示
    file_time = os.path.getmtime(DATA_FILE)
    update_time = datetime.datetime.fromtimestamp(file_time).strftime('%Y/%m/%d %H:%M')
    st.info(f"🔄 最終データ自動更新日時: **{update_time}** (毎週金・土・日 朝5時に自動更新)")
    
    # メイン画面の表示
    st.subheader("📊 本日のデータ×SNS 統合予想ランキング")
    
    # 表の表示（総合スコアが一番高いところを赤、SNS評価点が一番高いところを青に光らせます）
    st.dataframe(
        df_sorted.style.highlight_max(axis=0, subset=['総合スコア'], color='#ff4b4b')
                      .highlight_max(axis=0, subset=['SNS評価点'], color='#4bebff')
    )
    
    # 買い目自動生成
    st.markdown("---")
    st.header("🎯 AIおすすめ買い目予想")
    
    top_horses = df_sorted["馬番"].tolist()
    top_names = df_sorted["馬名"].tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎫 馬連（上位4頭ボックス）")
        box_horses = top_horses[:4]
        combinations = list(itertools.combinations(box_horses, 2))
        for combo in combinations:
            name1 = df[df["馬番"] == combo[0]]["馬名"].values[0]
            name2 = df[df["馬番"] == combo[1]]["馬名"].values[0]
            st.write(f"・ **{combo[0]} - {combo[1]}** （{name1} × {name2}）")
        st.info(f"計 {len(combinations)} 点")
        
    with col2:
        st.subheader("🔥 3連単（1着固定フォーメーション）")
        jiku = top_horses[0]
        aite = top_horses[1:4]
        st.write(f"【1着】 軸馬： **{jiku}** （{top_names[0]}）")
        st.write(f"【2・3着】 相手： **{', '.join(map(str, aite))}**")
        
        sanrentan_tickets = list(itertools.permutations(aite, 2))
        st.markdown("**【買い目一覧】**")
        for p in sanrentan_tickets:
            st.write(f"・ **{jiku} → {p[0]} → {p[1]}**")
        st.info(f"計 {len(sanrentan_tickets)} 点")
else:
    st.warning("現在データ収集中です。金・土・日の朝5時に自動で更新されます。")
