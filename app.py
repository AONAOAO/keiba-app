import streamlit as st
import pandas as pd
import os

st.title("🏇 AI競馬予想システム（完全リアルデータ版）")
st.write("前走成績・枠順・プロの印・騎手・オッズを総合的に分析したガチ予想です。")

csv_path = "latest_prediction.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    
    # 馬番をきれいな整数にする
    df['馬番'] = df['馬番'].astype(int)
    
    # 総合スコア順に並び替え
    df = df.sort_values(by='総合スコア', ascending=False).reset_index(drop=True)
    
    # 画面にランキング表を表示（SNSの列はもう表示しない）
    st.subheader("📊 本日のAI推奨ランキング")
    st.dataframe(df[['馬番', '馬名', '騎手', 'オッズ', '総合スコア']], use_container_width=True)

    if len(df) >= 4:
        st.subheader("🎯 AI自動生成の買い目")
        
        top4_nums = df['馬番'].head(4).tolist()
        
        st.write("### 【堅実】馬連ボックス（6点）")
        st.info(f"上位4頭のボックス: {top4_nums[0]}, {top4_nums[1]}, {top4_nums[2]}, {top4_nums[3]}")
        
        st.write("### 【一撃】3連単フォーメーション（6点）")
        st.success(f"1着固定: {top4_nums[0]}\n\n2・3着: {top4_nums[1]}, {top4_nums[2]}, {top4_nums[3]}")
else:
    st.error("まだ予測データが作成されていません。朝5時以降に確認するか、Actionsで手動実行してください。")
