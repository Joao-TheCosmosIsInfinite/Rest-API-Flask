def normalize_path_params(cidade=None, csat_min=0, csat_max=5,
                          diaria_min=0, diaria_max=10000,
                          limit=50, offset=0, **dados):
    # Funcao que estabelece os valores default para os parametros da requisicao GET
    if cidade:
        return {
        'csat_min': csat_min,
        'csat_max': csat_max,
        'diaria_min':diaria_min,
        'diaria_max':diaria_max,
        'cidade':cidade,
        'limit':limit,
        'offset':offset}
    return{
        'csat_min': csat_min,
        'csat_max': csat_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset}