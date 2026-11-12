import pandas as pd

# 1. CSV 파일 불러오기
df = pd.read_csv('E-commerce_Delivery_Shipping_Data_2026.csv')

# 2. 불필요한 식별자 열 삭제
df_clean = df.drop(columns=['order_id', 'customer_id'], errors='ignore')

# 3. 결측치(빈칸) 제거 및 이상치 처리
df_clean = df_clean.dropna()

# 4. 범주형(텍스트) 데이터 원-핫 인코딩 (수치화 변환)
df_clean = pd.get_dummies(df_clean, drop_first=True)

# 5. 전처리 완료된 파일 저장
df_clean.to_csv('processed_delivery_data.csv', index=False)
print("전처리 완료!")