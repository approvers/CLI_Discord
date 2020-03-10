def replace_at(string, start, length, new_text):
    """
    指定した文字列の指定した範囲を消して、指定した文字列で置きかえる。
    :param string: 操作対象の文字列
    :param start: 削除する部分の開始場所
    :param length: 削除する部分の長さ
    :param new_text: 置き換えする文字列

    replace_at("ABXXXCD", 2, 3, "--")
    >>> AB--CD
    """

    left = string[:start]
    right = string[start + length:]
    return left + new_text + right

