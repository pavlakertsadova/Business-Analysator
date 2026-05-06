import streamlit as st
import pandas as pd
import ollama
import plotly.express as px

st.set_page_config(page_title="Advanced AI Financial Suite", layout="wide")


with st.sidebar:
    st.header("📊 Контролен панел")
    mode = st.radio("Режим на работа", ["Единичен анализ", "Batch (Kaggle)"])
    
    if mode == "Единичен анализ":
        company = st.text_input("Компания", "TechNova")
        growth = st.slider("Ръст (%)", -50, 100, 25)
        debt = st.number_input("Дълг/Капитал", 0.0, 5.0, 0.4)
        margin = st.slider("Марж (%)", -20, 50, 15)
        sentiment = st.selectbox("Контекст", ["Positive", "Neutral", "Negative"])
    else:
        uploaded_file = st.file_path = st.file_uploader("Качете CSV файл (Kaggle dataset)")

#sends a request to the ollama local server and receives a response
def get_agent_response(model, role_prompt, data_summary):
    full_prompt = f"{role_prompt}\nДанни: {data_summary}"
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': full_prompt}])
    return response['message']['content']

#main interface
st.title("🏛️ Интелигентна Система за Инвестиционни Решения")

if mode == "Единичен анализ":
    if st.button("Стартирай Мулти-агентен анализ"):
        data_summary = f"Компания: {company}, Ръст: {growth}%, Дълг: {debt}, Марж: {margin}%, Контекст: {sentiment}"
        
        
        st.subheader("🔍 Проверка на фактите (Guardrails)")
        #the facts of the python code: 
        if debt > 2.0:
            st.warning(f"ВНИМАНИЕ: Високо ниво на дълг ({debt}). AI трябва да отчете това като риск.")
        else:
            st.success("Данните са консистентни и проверени.")

        #argument between agents - Llama3 and Gemma: 
        col1, col2 = st.columns(2)
        #optimistic
        with col1:
            st.info("🐂 Агент 'Бик' (Llama 3)")
            bull_resp = get_agent_response('llama3:latest', "Ти си оптимистичен анализатор. Намери силните страни.", data_summary)
            st.write(bull_resp)
        #pesimistic    
        with col2:
            st.error("🐻 Агент 'Мечка' (Gemma)")
            bear_resp = get_agent_response('gemma:2b', "Ти си песимистичен анализатор. Намери рисковете и скритите дефекти.", data_summary)
            st.write(bear_resp)

        # XAI
        st.subheader("🌡️ Топлинна карта на влиянието (XAI)")
        # matching the colors according to the weight of the arguments: 
        xai_cols = st.columns(3)
        xai_cols[0].metric("Влияние на Ръста", f"{growth}%", delta="Високо", delta_color="normal" if growth > 10 else "inverse")
        xai_cols[1].metric("Тежест на Дълга", debt, delta="Критично" if debt > 1.5 else "Ниско", delta_color="inverse" if debt > 1.5 else "normal")
        xai_cols[2].metric("Влияние на Маржа", f"{margin}%", delta="Стабилно" if margin > 10 else "Слабо")

        #agent judge 
        st.divider()
        st.subheader("⚖️ Финално решение (Агент-Съдия)")
        debate_context = f"Оптимист: {bull_resp}\nПесимист: {bear_resp}"
        judge_resp = get_agent_response('llama3:latest', "Ти си върховен съдия. Обобщи спора и дай финална присъда: Инвестирай/Продай.", debate_context)
        st.success(judge_resp)

elif mode == "Batch (Kaggle)":
    uploaded_file = st.file_uploader("Качете Kaggle файл", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        
        df['Margin'] = (df['Net Income'] / (df['Total Assets'] * 0.5)) * 100  
        df['Debt_Ratio'] = df['Total Liabilities'] / df['Total Assets']
        
        st.write(" 📈 Анализирани данни от Kaggle (NYSE)")
        st.dataframe(df[['Ticker', 'Net Income', 'Margin', 'Debt_Ratio']].style.highlight_max(axis=0, color='#023020'))

        if st.button("AI Ранкинг на всички компании"):
            with st.spinner("Агентите сравняват компаниите..."):
                all_data = ""
                for i, row in df.iterrows():
                    all_data += f"{row['Ticker']}: Марж {row['Margin']:.1f}%, Дълг {row['Debt_Ratio']:.2f}; "
                
                # sending everything to the judge agent for a summary
                rank_prompt = f"Ето данни за няколко компании: {all_data}. Класирай ги от най-добра към най-лоша инвестиция и се обоснови."
                ranking = ollama.chat(model='llama3:latest', messages=[{'role': 'user', 'content': rank_prompt}])
                
                st.success(" 🏆 Финална класация на AI Агента")
                st.write(ranking['message']['content'])