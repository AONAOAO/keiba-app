import streamlit as st
import pandas as pd
import os

# 画面全体のレイアウトを広くスタイリッシュに
st.set_page_config(page_title="AI競馬予想", layout="wide")

st.title("🏇 ADVANCED AI KEIBA PREDICTION SYSTEM")
st.markdown("---")

csv_path = "latest_prediction.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df['馬番'] = df['馬番'].astype(int)
    df = df.sort_values(by='総合スコア', ascending=False).reset_index(drop=True)
    
    # 画面を左（グラフとランキング）と右（買い目）に綺麗に分割！
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📊 AI推奨度グラフ")
        # スコアを視覚化
        st.bar_chart(df.set_index('馬名')['総合スコア'].head(8), color="#1f77b4")
        
        st.subheader("📋 本日のデータ分析ランキング")
        # 1位の行を目立たせる色付けスタイルの適用
        def highlight_top(s):
            return ['background-color: #fff3cd' if s.name == 0 else '' for _ in s]
        
        styled_df = df[['馬番', '馬名', '騎手', 'オッズ', '総合スコア']].style.apply(highlight_top, axis=1)
        st.dataframe(styled_df, use_container_width=True)

    with col_right:
        if len(df) >= 4:
            st.subheader("🎯 厳選買い目フォーメーション")
            top4 = df.head(4)
            
            # 1着固定（軸馬）をド派手な指標カードで表示！
            st.metric(label="👑 本命・軸馬 (総合1位)", value=f"【{top4.iloc[0]['馬番']}】 {top4.iloc[0]['馬名']}", delta=f"Score: {top4.iloc[0]['総合スコア']}")
            
            st.markdown("---")
            st.write("### 【堅実】馬連ボックス（6点）")
            nums_str = " - ".join([str(n) for n in top4['馬番'].tolist()])
            st.info(f"✨ [ {nums_str} ] Box")
            
            st.write("### 【一撃】3連単フォーメーション（6点）")
            opponents = ", ".join([str(n) for n in top4['馬番'].tail(3).tolist()])
            st.success(f"1着： {top4.iloc[0]['馬番']}\n\n2・3着： {opponents}")
