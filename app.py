import streamlit as st
import pandas as pd
import os

# 【プロ仕様】画面の横幅をフルに使い、タイトルを設定
st.set_page_config(page_title="AI競馬予想ダッシュボード", layout="wide")

st.title("🏇 ADVANCED AI KEIBA PREDICTION SYSTEM")
st.caption("前走成績・枠順・プロの印・リアルタイムオッズを多角的に分析した次世代ガチ予想")
st.markdown("---")

csv_path = "latest_prediction.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    
    # データの綺麗に整形
    df['馬番'] = df['馬番'].astype(int)
    df = df.sort_values(by='総合スコア', ascending=False).reset_index(drop=True)
    
    # ----------------------------------------------------
    # 画面を左（2割）と右（1割）の比率で2分割する
    # ----------------------------------------------------
    col_left, col_right = st.columns([2, 1])
    
    # === 左側：視覚的データ分析エリア ===
    with col_left:
        st.subheader("📊 AI推奨度（上位8頭）")
        # 上位8頭のスコアを美しい横棒グラフで可視化
        chart_data = df.head(8).set_index('馬名')['総合スコア']
        st.bar_chart(chart_data, color="#1f77b4")
        
        st.subheader("📋 本日のスクリーニングデータ")
        
        # 総合スコア1位（本命馬）の行を薄い黄色でハイライトする特殊な装飾
        def highlight_top_horse(row):
            return ['background-color: #fff3cd' if row.name == 0 else '' for _ in row]
            
        styled_df = df[['馬番', '馬名', '騎手', 'オッズ', '総合スコア']].style.apply(highlight_top_horse, axis=1)
        
        # 画面幅いっぱいにインタラクティブな表を表示（クリックで並び替え可能）
        st.dataframe(styled_df, use_container_width=True)

    # === 右側：買い目・結論エリア ===
    with col_right:
        if len(df) >= 4:
            st.subheader("🎯 厳選買い目フォーメーション")
            top4 = df.head(4)
            
            # 最も期待度が高い軸馬をド派手な「指標カード」で表示
            st.metric(
                label="👑 本命・不動の軸馬", 
                value=f"【{top4.iloc[0]['馬番']}】 {top4.iloc[0]['馬名']}", 
                delta=f"総合スコア: {top4.iloc[0]['総合スコア']}点"
            )
            
            st.markdown("---")
            
            # 視覚的に見やすいボックスデザインで買い目を表示
            st.write("### 🔹 【堅実】馬連ボックス（6点）")
            box_nums = " - ".join([str(n) for n in top4['馬番'].tolist()])
            st.info(f"✨ 該当馬番: [ {box_nums} ]")
            
            st.write("### 🔸 【一撃】3連単フォーメーション（6点）")
            opponents = ", ".join([str(n) for n in top4['馬番'].tail(3).tolist()])
            st.success(f"1着固定： 【{top4.iloc[0]['馬番']}】\n\n2・3着： {opponents}")
        else:
            st.warning("買い目を生成するにはデータが4頭以上必要です。")
else:
    st.error("まだ予測データが作成されていません。GitHub Actionsで手動実行するか、次回の自動更新をお待ちください。")
