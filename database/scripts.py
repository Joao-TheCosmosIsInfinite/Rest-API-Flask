
def consulta_hoteis(str_cidade):
    if str_cidade is None:
        str_aux = " "
    else:
        str_aux = "AND (cidade = ?)"

    consulta = "SELECT * " \
               "FROM hoteis " \
               "WHERE 1=1 " \
               "AND (csat > ? AND csat < ?) " \
               "AND (diaria > ? AND diaria < ?) " \
               + str_aux + \
               "LIMIT ? OFFSET ?"
    return consulta