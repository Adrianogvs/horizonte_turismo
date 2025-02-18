import pandas as pd
from io import BytesIO

def to_excel_bytes(df):
    """
    Converte um DataFrame em bytes de um arquivo Excel (XLSX),
    pronto para uso em st.download_button.
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Viagens')
    writer.close()
    processed_data = output.getvalue()
    return processed_data
