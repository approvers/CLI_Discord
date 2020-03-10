def replace_at(string, start, length, new_text):
    """
    指定した文字列の指定した範囲を、指定した文字列で置きかえる。
    :param string: 置き換え対象の文字列
    :param start: 置き換え開始場所
    :param length: 置き換える長さ
    :param new_text: 置き換え後の文字列

    replace_at("ABXXXCD", 2, 3, "--")
    >>> AB--CD
    """

    left = string[:start]
    right = string[start + length:]
    return left + new_text + right

