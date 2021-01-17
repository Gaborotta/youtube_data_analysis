import csv
# %%


def csv_writer(file_name, data, header=[]):
    """csv出力。

    Args:
        file_name (str): ファイル名
        data (list[list]): 出力する値のリスト 1行ごとの値を格納したリスト
        header (list, optional): ヘッダーのリスト 無ければヘッダーなしで出力. Defaults to [].

    Returns:
        bool: True固定
    """
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        if len(header) > 0:
            writer.writerow(header)
        writer.writerows([[x for x in row] for row in data])
    return True


def csvReader(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        row_list = [row for row in reader]
    return row_list
