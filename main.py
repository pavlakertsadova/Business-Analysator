import pandas as pd
import ollama

# 1. Зареждане на данните
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Грешка: Файлът '{file_path}' не беше намерен!")
        return None

# 2. Функция, която пита ИЗКУСТВЕНИЯ ИНТЕЛЕКТ (Ollama)
def get_ai_analysis(row):
    prompt = f"""
    Вие сте финансов експерт. Анализирайте следните данни:
    - Компания: {row['Company']}
    - Ръст: {row['Revenue_Growth']}
    - Дълг/Капитал: {row['Debt_to_Equity']}
    - Марж: {row['Profit_Margin']}
    - Контекст: {row['Market_Sentiment']}

    Вземете решение: 'Инвестирай', 'Изчакай' или 'Продай'. 
    Дайте оценка на риска от 1 до 10 и се обосновете кратко.
    """
    
    # ТУК Е МАГИЯТА: Изпращаме данните към модела gemma3:1b
    try:
        response = ollama.chat(model='llama3:latest', messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    except Exception as e:
        return f"Грешка при връзка с Ollama: {e}"

# --- ГЛАВНА ПРОГРАМА ---
print("--- СТАРТИРАНЕ НА АВТОНОМНИЯ БИЗНЕС АНАЛИЗАТОР ---")

data = load_data('company_data.csv')

if data is not None:
    for index, row in data.iterrows():
        print(f"\n[АНАЛИЗИРАНЕ НА {row['Company']}...]")
        
        # Викаме ИИ за анализ
        final_analysis = get_ai_analysis(row)
        
        print(f"--- РЕЗУЛТАТ ОТ ИЗКУСТВЕНИЯ ИНТЕЛЕКТ ---")
        print(final_analysis)
        print("="*50)